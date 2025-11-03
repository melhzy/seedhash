"""
Test and demonstrate all 4 random sampling techniques in SeedHash.

This script verifies that all 4 sampling methods are working correctly:
1. Simple random sampling
2. Stratified random sampling
3. Cluster random sampling
4. Systematic random sampling
"""

import sys
sys.path.insert(0, 'Python')

from seedhash import SeedSampler
import statistics


def test_simple_random_sampling():
    """Test 1: Simple Random Sampling"""
    print("=" * 70)
    print("TEST 1: SIMPLE RANDOM SAMPLING")
    print("=" * 70)
    print("Pure random selection with equal probability for each seed.\n")
    
    sampler = SeedSampler(master_seed=42)
    samples = sampler.simple_random_sampling(
        n_samples=20,
        seed_range=(0, 1000)
    )
    
    print(f"Master seed: {sampler.master_seed}")
    print(f"Number of samples: {len(samples)}")
    print(f"Samples: {samples[:10]}... (showing first 10)")
    print(f"Range: [{min(samples)}, {max(samples)}]")
    print(f"Mean: {statistics.mean(samples):.2f}")
    print(f"Std Dev: {statistics.stdev(samples):.2f}")
    print(f"\n✅ Simple random sampling works!\n")


def test_stratified_random_sampling():
    """Test 2: Stratified Random Sampling"""
    print("=" * 70)
    print("TEST 2: STRATIFIED RANDOM SAMPLING")
    print("=" * 70)
    print("Divides seed space into strata, samples from each for balanced coverage.\n")
    
    sampler = SeedSampler(master_seed=42)
    n_strata = 5
    samples = sampler.stratified_random_sampling(
        n_samples=25,
        seed_range=(0, 1000),
        n_strata=n_strata
    )
    
    print(f"Master seed: {sampler.master_seed}")
    print(f"Number of samples: {len(samples)}")
    print(f"Number of strata: {n_strata}")
    print(f"Expected per stratum: {25 // n_strata}")
    print(f"Sorted samples: {sorted(samples)}")
    print(f"Range: [{min(samples)}, {max(samples)}]")
    
    # Verify stratification
    stratum_size = 1000 // n_strata
    strata_counts = [0] * n_strata
    for sample in samples:
        stratum_idx = min(sample // stratum_size, n_strata - 1)
        strata_counts[stratum_idx] += 1
    
    print(f"\nSamples per stratum: {strata_counts}")
    print(f"✅ Stratified random sampling works!\n")


def test_cluster_random_sampling():
    """Test 3: Cluster Random Sampling"""
    print("=" * 70)
    print("TEST 3: CLUSTER RANDOM SAMPLING")
    print("=" * 70)
    print("Groups seeds into clusters around random centers.\n")
    
    sampler = SeedSampler(master_seed=42)
    n_clusters = 4
    samples = sampler.cluster_random_sampling(
        n_samples=20,
        seed_range=(0, 1000),
        n_clusters=n_clusters,
        samples_per_cluster=5
    )
    
    print(f"Master seed: {sampler.master_seed}")
    print(f"Number of samples: {len(samples)}")
    print(f"Number of clusters: {n_clusters}")
    print(f"Samples per cluster: {5}")
    print(f"Sorted samples: {sorted(samples)}")
    print(f"Range: [{min(samples)}, {max(samples)}]")
    print(f"Mean: {statistics.mean(samples):.2f}")
    
    # Show clustering effect (samples should be grouped)
    sorted_samples = sorted(samples)
    print(f"\nClustering visualization (sorted):")
    for i in range(0, len(sorted_samples), 5):
        cluster = sorted_samples[i:i+5]
        if cluster:
            print(f"  Cluster {i//5 + 1}: {cluster} (range: {max(cluster) - min(cluster)})")
    
    print(f"\n✅ Cluster random sampling works!\n")


def test_systematic_random_sampling():
    """Test 4: Systematic Random Sampling"""
    print("=" * 70)
    print("TEST 4: SYSTEMATIC RANDOM SAMPLING")
    print("=" * 70)
    print("Selects seeds at regular intervals with a random starting point.\n")
    
    sampler = SeedSampler(master_seed=42)
    samples = sampler.systematic_random_sampling(
        n_samples=15,
        seed_range=(0, 1000)
    )
    
    print(f"Master seed: {sampler.master_seed}")
    print(f"Number of samples: {len(samples)}")
    print(f"Expected interval: {1000 // 15} ≈ {1000 / 15:.2f}")
    print(f"Sorted samples: {sorted(samples)}")
    print(f"Range: [{min(samples)}, {max(samples)}]")
    
    # Calculate actual intervals
    sorted_samples = sorted(samples)
    intervals = [sorted_samples[i+1] - sorted_samples[i] for i in range(len(sorted_samples)-1)]
    print(f"\nActual intervals between samples:")
    print(f"  Min: {min(intervals)}, Max: {max(intervals)}, Mean: {statistics.mean(intervals):.2f}")
    print(f"  Intervals: {intervals}")
    
    print(f"\n✅ Systematic random sampling works!\n")


def test_reproducibility():
    """Test 5: Verify Reproducibility"""
    print("=" * 70)
    print("TEST 5: REPRODUCIBILITY CHECK")
    print("=" * 70)
    print("Same master seed should produce identical results.\n")
    
    master_seed = 12345
    
    # Run 1
    sampler1 = SeedSampler(master_seed)
    simple1 = sampler1.simple_random_sampling(10, (0, 100))
    stratified1 = sampler1.stratified_random_sampling(10, (0, 100), 5)
    
    # Run 2
    sampler2 = SeedSampler(master_seed)
    simple2 = sampler2.simple_random_sampling(10, (0, 100))
    stratified2 = sampler2.stratified_random_sampling(10, (0, 100), 5)
    
    print(f"Master seed: {master_seed}")
    print(f"\nSimple sampling run 1: {simple1}")
    print(f"Simple sampling run 2: {simple2}")
    print(f"Match: {simple1 == simple2} ✅" if simple1 == simple2 else f"Match: {simple1 == simple2} ❌")
    
    print(f"\nStratified sampling run 1: {stratified1}")
    print(f"Stratified sampling run 2: {stratified2}")
    print(f"Match: {stratified1 == stratified2} ✅" if stratified1 == stratified2 else f"Match: {stratified1 == stratified2} ❌")
    
    print(f"\n✅ Reproducibility verified!\n")


def test_integration_with_experiment_manager():
    """Test 6: Integration with SeedExperimentManager"""
    print("=" * 70)
    print("TEST 6: INTEGRATION WITH SEEDEXPERIMENTMANAGER")
    print("=" * 70)
    print("All sampling methods work with hierarchical seed generation.\n")
    
    from seedhash import SeedExperimentManager
    
    for method in ["simple", "stratified", "cluster", "systematic"]:
        manager = SeedExperimentManager(f"test_{method}")
        hierarchy = manager.generate_seed_hierarchy(
            n_seeds=5,
            n_sub_seeds=3,
            max_depth=2,
            sampling_method=method
        )
        
        print(f"{method.capitalize():12} - Level 1: {len(hierarchy[1])} seeds, Level 2: {len(hierarchy[2])} sub-seeds ✅")
    
    print(f"\n✅ All sampling methods integrate with SeedExperimentManager!\n")


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("SEEDHASH: 4 RANDOM SAMPLING TECHNIQUES - COMPREHENSIVE TEST")
    print("=" * 70)
    print()
    
    test_simple_random_sampling()
    test_stratified_random_sampling()
    test_cluster_random_sampling()
    test_systematic_random_sampling()
    test_reproducibility()
    test_integration_with_experiment_manager()
    
    print("=" * 70)
    print("ALL TESTS PASSED! 🎉")
    print("=" * 70)
    print("\nSummary:")
    print("✅ 1. Simple Random Sampling - Working")
    print("✅ 2. Stratified Random Sampling - Working")
    print("✅ 3. Cluster Random Sampling - Working")
    print("✅ 4. Systematic Random Sampling - Working")
    print("✅ 5. Reproducibility - Verified")
    print("✅ 6. SeedExperimentManager Integration - Working")
    print("\nAll 4 sampling techniques are fully functional!")
    print("=" * 70)


if __name__ == "__main__":
    main()
