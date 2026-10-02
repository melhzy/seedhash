"""
Regression tests for correctness fixes in the Python package.

Covers cross-language seed values, reproducibility of existing outputs,
side effects on global state, hierarchy tracking and the ML metrics.
"""

import os
import random
import subprocess
import sys
import textwrap

import numpy as np
import pytest

sys.path.insert(0, 'Python')

from seedhash import MLMetrics, SeedExperimentManager, SeedHashGenerator, SeedSampler


# --- Seeds and reproducibility ---------------------------------------------

def test_seed_number_matches_r_package():
    """The R package's tests pin the same values."""
    expected = {
        "experiment_1": 1603554058,
        "test": 640136438,
        "Shalini": 52639232,
        "café": 1930968482,
    }
    for text, seed in expected.items():
        assert SeedHashGenerator(text).seed_number == seed, text


def test_generate_seeds_output_is_pinned():
    assert SeedHashGenerator("experiment_1").generate_seeds(5) == [
        179576649, 1611871093, 1351360959, 1045713345, 1687315778
    ]
    assert SeedHashGenerator("test", 1, 100).generate_seeds(5) == [75, 27, 2, 28, 34]


def test_sampling_output_is_pinned():
    def sampler():
        return SeedSampler(12345)

    assert sampler().simple_random_sampling(3, (0, 1000)) == [426, 750, 10]
    assert sampler().stratified_random_sampling(10, (0, 1000)) == [
        106, 187, 2, 459, 461, 455, 576, 718, 844, 988
    ]
    assert sampler().cluster_random_sampling(10, (0, 1000)) == [
        426, 445, 898, 887, 312, 303, 188, 172, 922, 911
    ]
    assert sampler().systematic_random_sampling(10, (0, 1000)) == [
        53, 153, 253, 353, 453, 553, 653, 753, 853, 953
    ]


def test_generate_seeds_leaves_global_random_alone():
    random.seed(42)
    expected = [random.random() for _ in range(3)]

    random.seed(42)
    first = random.random()
    SeedHashGenerator("test").generate_seeds(3)
    assert [first, random.random(), random.random()] == expected


# --- Imports -----------------------------------------------------------------

def _run_python(code, extra_path=None):
    env = dict(os.environ)
    if extra_path:
        env["PYTHONPATH"] = os.pathsep.join([extra_path, env.get("PYTHONPATH", "")])
    return subprocess.run(
        [sys.executable, "-c", textwrap.dedent(code)],
        capture_output=True, text=True, env=env,
    )


def test_import_without_pandas_does_not_warn():
    result = _run_python("""
        import sys, warnings
        sys.path.insert(0, 'Python')
        sys.modules['pandas'] = None  # makes `import pandas` raise ImportError
        warnings.simplefilter('error')
        from seedhash import SeedHashGenerator
    """)
    assert result.returncode == 0, result.stderr


def test_broken_tensorflow_does_not_break_import(tmp_path):
    fake = tmp_path / "tensorflow"
    fake.mkdir()
    (fake / "__init__.py").write_text(
        "raise TypeError('Descriptors cannot be created directly')\n"
    )
    result = _run_python("""
        import sys
        sys.path.insert(0, 'Python')
        from seedhash import core
        assert not core.TF_AVAILABLE
    """, extra_path=str(tmp_path))
    assert result.returncode == 0, result.stderr


# --- Sampling input validation ---------------------------------------------

def test_stratified_rejects_range_narrower_than_strata():
    with pytest.raises(ValueError, match="too narrow"):
        SeedSampler(0).stratified_random_sampling(4, (0, 2), n_strata=4)
    with pytest.raises(ValueError, match="too narrow"):
        SeedSampler(0).stratified_random_sampling(4, (0, 3), n_strata=4)
    assert len(SeedSampler(0).stratified_random_sampling(4, (0, 4), n_strata=4)) == 4


def test_systematic_rejects_invalid_sample_counts():
    with pytest.raises(ValueError, match="n_samples"):
        SeedSampler(0).systematic_random_sampling(0, (0, 100))
    with pytest.raises(ValueError, match="n_samples"):
        SeedSampler(0).systematic_random_sampling(5, (0, 3))

    seeds = SeedSampler(0).systematic_random_sampling(10, (0, 10))
    assert len(set(seeds)) == 10
    assert all(0 <= s <= 10 for s in seeds)


# --- Experiment manager ----------------------------------------------------

def _run_with_timeout(func, seconds=10):
    """Fail instead of hanging forever if func loops."""
    import threading

    error = []

    def target():
        try:
            func()
        except Exception as exc:  # pragma: no cover - reported below
            error.append(exc)

    thread = threading.Thread(target=target, daemon=True)
    thread.start()
    thread.join(seconds)
    assert not thread.is_alive(), "call did not finish (infinite loop?)"
    if error:
        raise error[0]


def test_seed_collisions_do_not_hang_or_rewrite_lineage():
    manager = SeedExperimentManager("x", master_seed=0)
    hierarchy = manager.generate_seed_hierarchy(
        n_seeds=10, n_sub_seeds=5, seed_range=(0, 100)
    )

    for seed in hierarchy[1] + hierarchy[2]:
        _run_with_timeout(lambda: manager.add_experiment_result(
            seed, "classification", {"acc": 1.0}, "simple"
        ))

    # Level-1 seeds keep the master as their parent even when they
    # reappear as sub-seeds further down the hierarchy
    for seed in hierarchy[1]:
        assert manager._seed_hierarchy[seed]["parent"] == 0

    first = manager.results[0]
    assert first.seed_hierarchy == [0, hierarchy[1][0]]
    assert first.seed_level == 1


def test_results_do_not_share_callers_dicts():
    manager = SeedExperimentManager("x")
    metrics = {}
    for accuracy in (0.1, 0.9):
        metrics["accuracy"] = accuracy
        manager.add_experiment_result(1, "classification", metrics, "simple")

    assert [r.metrics["accuracy"] for r in manager.results] == [0.1, 0.9]


# --- Metrics -----------------------------------------------------------------

def test_binary_metrics_with_non_01_labels():
    metrics = MLMetrics.classification_metrics([-1, 1, -1, 1], [1, 1, 1, -1])
    assert metrics["accuracy"] == 0.25
    assert metrics["precision"] == pytest.approx(1 / 3)
    assert metrics["recall"] == pytest.approx(0.5)
    assert metrics["f1"] == pytest.approx(0.4)

    metrics = MLMetrics.classification_metrics(["cat", "dog", "dog"], ["cat", "dog", "dog"])
    assert metrics["precision"] == metrics["recall"] == metrics["f1"] == 1.0


def test_multiclass_f1_is_mean_of_per_class_f1():
    # Per-class F1: class 0 = 0.8, class 1 = 0.5, class 2 = 0.0. The F1 of
    # the macro precision and recall would be about 0.494 instead.
    metrics = MLMetrics.classification_metrics([0, 0, 0, 1, 2], [0, 0, 1, 1, 1])
    assert metrics["f1"] == pytest.approx((0.8 + 0.5 + 0.0) / 3)


def test_metrics_reject_or_flatten_mismatched_shapes():
    y = np.arange(100.0)
    assert MLMetrics.regression_metrics(y, y.reshape(-1, 1))["rmse"] == 0.0
    assert MLMetrics.classification_metrics(y, y.reshape(-1, 1))["accuracy"] == 1.0

    with pytest.raises(ValueError, match="same number of values"):
        MLMetrics.regression_metrics([1, 2, 3], [1, 2])


def test_silhouette_handles_singletons_and_identical_points():
    # Value from sklearn.metrics.silhouette_score for the same input
    metrics = MLMetrics.clustering_metrics([[0], [0], [10], [11], [30]], [0, 0, 1, 1, 2])
    assert metrics["silhouette"] == pytest.approx(0.7618181818181818)
    assert metrics["n_clusters"] == 3

    degenerate = MLMetrics.clustering_metrics([[0], [1]], [0, 0])
    assert degenerate == {"silhouette": 0.0, "n_clusters": 1, "n_samples": 2}


def test_improvement_rate_sign_with_negative_rewards():
    rewards = list(np.linspace(-100, -50, 50))
    metrics = MLMetrics.reinforcement_learning_metrics(rewards, [1] * 50)
    assert metrics["improvement_rate"] > 0

    # With 10 episodes the early and recent windows must not be the same data
    metrics = MLMetrics.reinforcement_learning_metrics(list(range(1, 11)), [1] * 10)
    assert metrics["improvement_rate"] == pytest.approx((8 - 3) / 3)
