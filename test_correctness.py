"""
Regression tests for correctness fixes in the Python package.
"""

import sys

sys.path.insert(0, 'Python')

from seedhash import SeedExperimentManager


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
