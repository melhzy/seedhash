"""
Seed PyTorch on one GPU, several GPUs on one node, or GPUs on several nodes.

The seeding code is the same in all three cases; only the launch changes.
Without GPUs the script runs on the CPU with the gloo backend.

    # One GPU (or the CPU) on one node
    python distributed_seeding.py

    # Four GPUs on one node
    torchrun --standalone --nproc-per-node=4 distributed_seeding.py

    # Two nodes with four GPUs each: run this on every node with its own
    # --node-rank (0 and 1), pointing at node 0's address
    torchrun --nnodes=2 --nproc-per-node=4 --node-rank=0 \\
        --master-addr=<node 0 address> --master-port=29500 distributed_seeding.py

    # SLURM: start one torchrun per node, as above, with srun
"""

import os

import torch
import torch.distributed as dist
from torch.utils.data import DataLoader, TensorDataset
from torch.utils.data.distributed import DistributedSampler

from seedhash import SeedHashGenerator, get_global_rank


def main():
    distributed = "WORLD_SIZE" in os.environ  # set by torchrun
    if torch.cuda.is_available():
        device = torch.device("cuda", int(os.environ.get("LOCAL_RANK", 0)))
        torch.cuda.set_device(device)
    else:
        device = torch.device("cpu")
    if distributed:
        dist.init_process_group("nccl" if device.type == "cuda" else "gloo")

    gen = SeedHashGenerator("resnet50_imagenet_run1")
    rank = get_global_rank()

    # Same seed in every process: every rank draws the same numbers
    gen.set_seed("torch")
    shared = torch.rand(2, device=device)

    # One seed per process, so ranks get different augmentations and
    # dropout masks. Rank 0 keeps gen.seed_number.
    gen.set_seed("torch", per_rank=True)
    own = torch.rand(2, device=device)

    # DistributedSampler must shuffle the same way on every rank so that the
    # ranks split the data without overlap: give it the shared seed
    dataset = TensorDataset(torch.arange(16))
    sampler = DistributedSampler(dataset, seed=gen.seed_number) if distributed else None
    loader = DataLoader(dataset, batch_size=4, sampler=sampler, shuffle=sampler is None)
    first_batch = next(iter(loader))[0].tolist()

    print(
        f"rank {rank} on {device}: "
        f"shared seed {gen.seed_number} -> {shared.tolist()}, "
        f"rank seed {gen.rank_seed()} -> {own.tolist()}, "
        f"first batch {first_batch}"
    )

    if distributed:
        dist.destroy_process_group()


if __name__ == "__main__":
    main()
