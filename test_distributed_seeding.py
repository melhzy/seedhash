"""
Tests for seeding PyTorch on one GPU, several GPUs on one node, and GPUs
across several nodes.

The unit tests need no PyTorch. The launcher tests start real multi-process
jobs with torchrun and torch.multiprocessing.spawn on the CPU (gloo backend)
and are skipped when PyTorch is not installed.
"""

import json
import os
import random
import socket
import subprocess
import sys
import textwrap
from pathlib import Path
from types import SimpleNamespace

import pytest

PYTHON_DIR = Path(__file__).resolve().parent / "Python"
sys.path.insert(0, str(PYTHON_DIR))

import seedhash.core as core
from seedhash import SeedHashGenerator, get_global_rank

try:
    import torch
    import torch.distributed as dist
    HAVE_GLOO = dist.is_available() and dist.is_gloo_available()
except Exception:
    HAVE_GLOO = False

requires_gloo = pytest.mark.skipif(not HAVE_GLOO, reason="needs PyTorch with the gloo backend")

LAUNCHER_ENV_VARS = core.RANK_ENV_VARS + ("LOCAL_RANK", "WORLD_SIZE", "LOCAL_WORLD_SIZE")


@pytest.fixture(autouse=True)
def no_launcher_env(monkeypatch):
    """Start every test outside any distributed job."""
    for name in LAUNCHER_ENV_VARS:
        monkeypatch.delenv(name, raising=False)


# --- Rank detection ---------------------------------------------------------

def test_rank_is_zero_outside_a_distributed_job():
    assert get_global_rank() == 0


@pytest.mark.parametrize("name", core.RANK_ENV_VARS)
def test_rank_is_read_from_each_launcher(monkeypatch, name):
    monkeypatch.setenv(name, "5")
    assert get_global_rank() == 5


def test_torchrun_rank_wins_over_slurm(monkeypatch):
    # torchrun under SLURM: SLURM_PROCID numbers the node's task, RANK the process
    monkeypatch.setenv("SLURM_PROCID", "1")
    monkeypatch.setenv("RANK", "6")
    assert get_global_rank() == 6


def test_local_rank_alone_is_not_used(monkeypatch):
    # LOCAL_RANK repeats on every node, so it cannot give unique seeds
    monkeypatch.setenv("LOCAL_RANK", "3")
    assert get_global_rank() == 0


@pytest.mark.parametrize("value", ["-1", "abc", "1.5"])
def test_invalid_rank_variable_raises(monkeypatch, value):
    monkeypatch.setenv("RANK", value)
    with pytest.raises(ValueError, match="RANK"):
        get_global_rank()


def _fake_torch(calls, initialized=False, rank=0):
    """Just enough of torch for set_seed() and get_global_rank()."""
    return SimpleNamespace(
        manual_seed=lambda seed: calls.append(("manual_seed", seed)),
        cuda=SimpleNamespace(
            is_available=lambda: True,
            manual_seed_all=lambda seed: calls.append(("cuda.manual_seed_all", seed)),
        ),
        distributed=SimpleNamespace(
            is_available=lambda: True,
            is_initialized=lambda: initialized,
            get_rank=lambda: rank,
        ),
    )


def test_initialized_process_group_wins_over_environment(monkeypatch):
    monkeypatch.setattr(core, "torch", _fake_torch([], initialized=True, rank=7), raising=False)
    monkeypatch.setattr(core, "TORCH_AVAILABLE", True)
    monkeypatch.setenv("RANK", "2")
    assert get_global_rank() == 7


# --- Seeds ------------------------------------------------------------------

def test_rank_seed_offsets_seed_number_by_rank():
    gen = SeedHashGenerator("distributed_test")
    assert gen.rank_seed(0) == gen.seed_number
    assert gen.rank_seed(3) == (gen.seed_number + 3) % 2**32
    assert len({gen.rank_seed(r) for r in range(64)}) == 64


def test_rank_seed_wraps_to_32_bits():
    gen = SeedHashGenerator("Bob")  # seed_number 3214761019
    assert gen.rank_seed(2**32 - gen.seed_number) == 0


def test_rank_seed_detects_rank(monkeypatch):
    gen = SeedHashGenerator("distributed_test")
    monkeypatch.setenv("RANK", "4")
    assert gen.rank_seed() == gen.rank_seed(4)


@pytest.mark.parametrize("rank, error", [(-1, ValueError), (1.0, TypeError), (True, TypeError)])
def test_rank_seed_validates_rank(rank, error):
    with pytest.raises(error):
        SeedHashGenerator("x").rank_seed(rank)


def test_set_seed_uses_seed_number_on_every_rank_by_default(monkeypatch):
    gen = SeedHashGenerator("distributed_test")
    monkeypatch.setenv("RANK", "3")
    gen.set_seed("python")
    assert random.random() == random.Random(gen.seed_number).random()


def test_set_seed_per_rank_uses_rank_seed(monkeypatch):
    gen = SeedHashGenerator("distributed_test")
    monkeypatch.setenv("RANK", "3")
    gen.set_seed("python", per_rank=True)
    assert random.random() == random.Random(gen.rank_seed(3)).random()

    gen.set_seed("python", per_rank=True, rank=5)
    assert random.random() == random.Random(gen.rank_seed(5)).random()


def test_rank_without_per_rank_raises():
    with pytest.raises(ValueError, match="per_rank"):
        SeedHashGenerator("x").set_seed("python", rank=1)


def test_set_seed_seeds_cpu_and_all_gpus_with_rank_seed(monkeypatch):
    calls = []
    monkeypatch.setattr(core, "torch", _fake_torch(calls), raising=False)
    monkeypatch.setattr(core, "TORCH_AVAILABLE", True)
    gen = SeedHashGenerator("distributed_test")

    gen.set_seed("torch", deterministic=False, per_rank=True, rank=2)
    assert calls == [
        ("manual_seed", gen.rank_seed(2)),
        ("cuda.manual_seed_all", gen.rank_seed(2)),
    ]

    calls.clear()
    gen.seed_all(deterministic=False, per_rank=True, rank=2)
    assert ("manual_seed", gen.rank_seed(2)) in calls


# --- Real multi-process jobs -------------------------------------------------

WORKER = textwrap.dedent("""
    import json, os, sys
    import torch
    import torch.distributed as dist
    import torch.multiprocessing as mp

    sys.path.insert(0, sys.argv[1])
    from seedhash import SeedHashGenerator, get_global_rank


    def run(rank, world_size, init_method, out_path):
        gen = SeedHashGenerator("distributed_test")
        rank_before_init = get_global_rank()
        dist.init_process_group("gloo", init_method=init_method,
                                rank=rank, world_size=world_size)
        record = {
            "rank": dist.get_rank(),
            "local_rank": int(os.environ.get("LOCAL_RANK", rank)),
            "rank_before_init": rank_before_init,
            "rank_after_init": get_global_rank(),
        }
        gen.set_seed("torch")
        record["shared"] = torch.rand(3).tolist()
        if init_method == "env://":
            gen.set_seed("torch", per_rank=True)
        else:
            gen.set_seed("torch", per_rank=True, rank=rank)
        record["per_rank_seed"] = gen.rank_seed(dist.get_rank())
        record["per_rank"] = torch.rand(3).tolist()

        records = [None] * dist.get_world_size()
        dist.all_gather_object(records, record)
        if dist.get_rank() == 0:
            with open(out_path, "w") as f:
                json.dump(records, f)
        dist.destroy_process_group()


    if __name__ == "__main__":
        out_path = sys.argv[2]
        if sys.argv[3] == "spawn":
            port = sys.argv[4]
            mp.spawn(run, nprocs=2, args=(2, f"tcp://127.0.0.1:{port}", out_path))
        else:
            run(int(os.environ["RANK"]), int(os.environ["WORLD_SIZE"]), "env://", out_path)
""")


def _free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def _launcher_env():
    env = {k: v for k, v in os.environ.items() if k not in LAUNCHER_ENV_VARS}
    env["OMP_NUM_THREADS"] = "1"
    return env


def _torchrun(tmp_path, *args):
    return [sys.executable, "-m", "torch.distributed.run", *args,
            str(tmp_path / "worker.py"), str(PYTHON_DIR), str(tmp_path / "out.json"), "torchrun"]


def _check_records(tmp_path, world_size, launched_by_env):
    records = sorted(json.loads((tmp_path / "out.json").read_text()), key=lambda r: r["rank"])
    gen = SeedHashGenerator("distributed_test")

    assert [r["rank"] for r in records] == list(range(world_size))
    for r in records:
        assert r["rank_after_init"] == r["rank"]
        # Without launcher variables (mp.spawn) the rank must be passed explicitly
        assert r["rank_before_init"] == (r["rank"] if launched_by_env else 0)

    # Default: every rank draws the same numbers
    torch.manual_seed(gen.seed_number)
    expected_shared = torch.rand(3).tolist()
    assert all(r["shared"] == expected_shared for r in records)

    # per_rank: each rank gets its own seed and reproducible numbers
    assert len({r["per_rank_seed"] for r in records}) == world_size
    for r in records:
        assert r["per_rank_seed"] == gen.rank_seed(r["rank"])
        torch.manual_seed(r["per_rank_seed"])
        assert r["per_rank"] == torch.rand(3).tolist()
    return records


@requires_gloo
def test_torchrun_several_processes_on_one_node(tmp_path):
    (tmp_path / "worker.py").write_text(WORKER)
    subprocess.run(
        _torchrun(tmp_path, "--standalone", "--nproc-per-node=4"),
        env=_launcher_env(), check=True, timeout=120, capture_output=True,
    )
    _check_records(tmp_path, world_size=4, launched_by_env=True)


@requires_gloo
def test_torchrun_several_nodes(tmp_path):
    """Two nodes with two processes each, simulated on localhost."""
    (tmp_path / "worker.py").write_text(WORKER)
    port = _free_port()
    nodes = [
        subprocess.Popen(
            _torchrun(tmp_path, "--nnodes=2", "--nproc-per-node=2", f"--node-rank={node}",
                      "--master-addr=127.0.0.1", f"--master-port={port}"),
            env=_launcher_env(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        for node in (0, 1)
    ]
    for proc in nodes:
        output, _ = proc.communicate(timeout=120)
        assert proc.returncode == 0, output.decode()

    records = _check_records(tmp_path, world_size=4, launched_by_env=True)
    # Local ranks repeat on each node, but the seeds are still all different
    assert [r["local_rank"] for r in records] == [0, 1, 0, 1]


@requires_gloo
def test_multiprocessing_spawn_with_explicit_rank(tmp_path):
    (tmp_path / "worker.py").write_text(WORKER)
    subprocess.run(
        [sys.executable, str(tmp_path / "worker.py"), str(PYTHON_DIR),
         str(tmp_path / "out.json"), "spawn", str(_free_port())],
        env=_launcher_env(), check=True, timeout=120, capture_output=True,
    )
    _check_records(tmp_path, world_size=2, launched_by_env=False)
