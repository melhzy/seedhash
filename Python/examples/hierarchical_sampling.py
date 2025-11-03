"""
Comprehensive examples demonstrating hierarchical seed sampling with ML experiments.

This script shows:
1. All 4 sampling methods (simple, stratified, cluster, systematic)
2. Different ML tasks (regression, classification, unsupervised)
3. Hierarchical seed management (master → seeds → sub-seeds)
4. Experiment tracking with pandas DataFrame
"""

import sys
sys.path.insert(0, 'Python')

from seedhash import SeedHashGenerator, SeedExperimentManager, MLMetrics
import random


def example_simple_random_sampling():
    """Example 1: Simple Random Sampling for Regression Tasks."""
    print("=" * 70)
    print("Example 1: Simple Random Sampling - Regression")
    print("=" * 70)
    
    # Initialize experiment manager
    manager = SeedExperimentManager("regression_baseline")
    
    print(f"Experiment: {manager.experiment_name}")
    print(f"Master Seed: {manager.master_seed}\n")
    
    # Generate seed hierarchy: master → 5 seeds → 3 sub-seeds each
    hierarchy = manager.generate_seed_hierarchy(
        n_seeds=5,
        n_sub_seeds=3,
        max_depth=2,
        sampling_method="simple"
    )
    
    print("Seed Hierarchy (Simple Random Sampling):")
    print(f"  Level 0 (Master): {hierarchy[0]}")
    print(f"  Level 1 (Seeds): {len(hierarchy[1])} seeds")
    print(f"  Level 2 (Sub-seeds): {len(hierarchy[2])} sub-seeds\n")
    
    # Simulate regression experiments with different seeds
    print("Running regression experiments...")
    for seed in hierarchy[2][:5]:  # Use first 5 sub-seeds
        # Simulate a regression model run
        random.seed(seed)
        
        # Simulated predictions vs true values
        y_true = [random.uniform(0, 100) for _ in range(50)]
        y_pred = [val + random.uniform(-10, 10) for val in y_true]
        
        # Calculate metrics
        metrics = MLMetrics.regression_metrics(y_true, y_pred)
        
        # Record experiment
        manager.add_experiment_result(
            seed=seed,
            ml_task="regression",
            metrics=metrics,
            sampling_method="simple",
            metadata={"model": "linear_regression", "n_samples": 50}
        )
        
        print(f"  Seed {seed}: RMSE={metrics['rmse']:.2f}, R²={metrics['r2']:.3f}")
    
    print("\n✓ Simple random sampling completed\n")
    return manager


def example_stratified_sampling():
    """Example 2: Stratified Random Sampling for Classification Tasks."""
    print("=" * 70)
    print("Example 2: Stratified Random Sampling - Classification")
    print("=" * 70)
    
    manager = SeedExperimentManager("classification_balanced")
    
    print(f"Experiment: {manager.experiment_name}")
    print(f"Master Seed: {manager.master_seed}\n")
    
    # Generate stratified hierarchy
    hierarchy = manager.generate_seed_hierarchy(
        n_seeds=8,
        n_sub_seeds=4,
        max_depth=2,
        sampling_method="stratified"
    )
    
    print("Seed Hierarchy (Stratified Sampling):")
    print(f"  Ensures balanced coverage across seed space")
    print(f"  Level 1: {len(hierarchy[1])} seeds")
    print(f"  Level 2: {len(hierarchy[2])} sub-seeds\n")
    
    # Simulate classification experiments
    print("Running classification experiments...")
    for seed in hierarchy[2][:6]:
        random.seed(seed)
        
        # Simulated binary classification
        y_true = [random.randint(0, 1) for _ in range(100)]
        y_pred = [val if random.random() > 0.15 else 1 - val for val in y_true]
        
        metrics = MLMetrics.classification_metrics(y_true, y_pred)
        
        manager.add_experiment_result(
            seed=seed,
            ml_task="classification",
            metrics=metrics,
            sampling_method="stratified",
            metadata={"model": "random_forest", "n_classes": 2, "n_samples": 100}
        )
        
        print(f"  Seed {seed}: Accuracy={metrics['accuracy']:.3f}, F1={metrics['f1']:.3f}")
    
    print("\n✓ Stratified sampling completed\n")
    return manager


def example_cluster_sampling():
    """Example 3: Cluster Random Sampling for Unsupervised Learning."""
    print("=" * 70)
    print("Example 3: Cluster Random Sampling - Unsupervised Learning")
    print("=" * 70)
    
    manager = SeedExperimentManager("clustering_analysis")
    
    print(f"Experiment: {manager.experiment_name}")
    print(f"Master Seed: {manager.master_seed}\n")
    
    # Generate cluster-based hierarchy
    hierarchy = manager.generate_seed_hierarchy(
        n_seeds=10,
        n_sub_seeds=3,
        max_depth=2,
        sampling_method="cluster"
    )
    
    print("Seed Hierarchy (Cluster Sampling):")
    print(f"  Groups related seeds together")
    print(f"  Level 1: {len(hierarchy[1])} seeds in clusters")
    print(f"  Level 2: {len(hierarchy[2])} sub-seeds\n")
    
    # Simulate clustering experiments
    print("Running clustering experiments...")
    try:
        import numpy as np
        
        for seed in hierarchy[2][:5]:
            np.random.seed(seed)
            
            # Simulated clustering data
            n_samples = 150
            X = np.random.randn(n_samples, 2)
            
            # Simulated cluster labels
            labels = np.random.randint(0, 3, n_samples)
            
            metrics = MLMetrics.clustering_metrics(X, labels)
            
            manager.add_experiment_result(
                seed=seed,
                ml_task="unsupervised",
                metrics=metrics,
                sampling_method="cluster",
                metadata={"algorithm": "kmeans", "n_clusters": 3, "n_samples": n_samples}
            )
            
            print(f"  Seed {seed}: Silhouette={metrics['silhouette']:.3f}, Clusters={metrics['n_clusters']}")
    
    except ImportError:
        print("  NumPy not available - skipping clustering example")
    
    print("\n✓ Cluster sampling completed\n")
    return manager


def example_systematic_sampling():
    """Example 4: Systematic Random Sampling for Mixed Tasks."""
    print("=" * 70)
    print("Example 4: Systematic Random Sampling - Mixed ML Tasks")
    print("=" * 70)
    
    manager = SeedExperimentManager("mixed_tasks_systematic")
    
    print(f"Experiment: {manager.experiment_name}")
    print(f"Master Seed: {manager.master_seed}\n")
    
    # Generate systematic hierarchy
    hierarchy = manager.generate_seed_hierarchy(
        n_seeds=6,
        n_sub_seeds=4,
        max_depth=2,
        sampling_method="systematic"
    )
    
    print("Seed Hierarchy (Systematic Sampling):")
    print(f"  Evenly distributed with regular intervals")
    print(f"  Level 1: {len(hierarchy[1])} seeds")
    print(f"  Level 2: {len(hierarchy[2])} sub-seeds\n")
    
    # Run mixed ML tasks
    print("Running mixed ML tasks...")
    seeds = hierarchy[2][:8]
    
    for i, seed in enumerate(seeds):
        random.seed(seed)
        
        # Alternate between regression and classification
        if i % 2 == 0:
            # Regression
            y_true = [random.uniform(0, 100) for _ in range(30)]
            y_pred = [val + random.uniform(-5, 5) for val in y_true]
            metrics = MLMetrics.regression_metrics(y_true, y_pred)
            task = "regression"
            print(f"  Seed {seed} [Regression]: RMSE={metrics['rmse']:.2f}")
        else:
            # Classification
            y_true = [random.randint(0, 1) for _ in range(30)]
            y_pred = [val if random.random() > 0.1 else 1 - val for val in y_true]
            metrics = MLMetrics.classification_metrics(y_true, y_pred)
            task = "classification"
            print(f"  Seed {seed} [Classification]: Accuracy={metrics['accuracy']:.3f}")
        
        manager.add_experiment_result(
            seed=seed,
            ml_task=task,
            metrics=metrics,
            sampling_method="systematic",
            metadata={"batch": i // 2}
        )
    
    print("\n✓ Systematic sampling completed\n")
    return manager


def example_deep_hierarchy():
    """Example 5: Deep Hierarchy with 3+ Levels."""
    print("=" * 70)
    print("Example 5: Deep Seed Hierarchy (Master → Seeds → Sub-seeds → Sub-sub-seeds)")
    print("=" * 70)
    
    manager = SeedExperimentManager("deep_hierarchy_test")
    
    print(f"Master Seed: {manager.master_seed}\n")
    
    # Generate deep hierarchy
    hierarchy = manager.generate_seed_hierarchy(
        n_seeds=4,
        n_sub_seeds=3,
        max_depth=3,  # 3 levels deep!
        sampling_method="simple"
    )
    
    print("Deep Hierarchy Structure:")
    for level, seeds in hierarchy.items():
        level_names = ["Master", "Seeds", "Sub-seeds", "Sub-sub-seeds"]
        print(f"  Level {level} ({level_names[level]}): {len(seeds)} seeds")
    
    print(f"\nTotal seeds generated: {sum(len(seeds) for seeds in hierarchy.values())}")
    print("✓ Deep hierarchy generated\n")
    
    return manager


def example_comparison_all_methods():
    """Example 6: Compare All Sampling Methods."""
    print("=" * 70)
    print("Example 6: Comparing All Sampling Methods")
    print("=" * 70)
    
    methods = ["simple", "stratified", "cluster", "systematic"]
    results = {}
    
    for method in methods:
        manager = SeedExperimentManager(f"compare_{method}")
        
        hierarchy = manager.generate_seed_hierarchy(
            n_seeds=10,
            n_sub_seeds=5,
            max_depth=2,
            sampling_method=method
        )
        
        results[method] = {
            'master_seed': manager.master_seed,
            'total_seeds': len(hierarchy[1]) + len(hierarchy[2]),
            'level_1': len(hierarchy[1]),
            'level_2': len(hierarchy[2])
        }
    
    print("\nSampling Method Comparison:")
    print("-" * 70)
    for method, stats in results.items():
        print(f"{method.capitalize():15} | Master: {stats['master_seed']:10} | "
              f"Level 1: {stats['level_1']:3} | Level 2: {stats['level_2']:3}")
    
    print("\n✓ All methods compared\n")


def example_export_results():
    """Example 7: Export Results to DataFrame and Files."""
    print("=" * 70)
    print("Example 7: Exporting Results to DataFrame")
    print("=" * 70)
    
    try:
        import pandas as pd
        
        # Run experiments
        manager = example_simple_random_sampling()
        
        # Get DataFrame
        df = manager.get_results_dataframe()
        
        print("\nExperiment Results DataFrame:")
        print("-" * 70)
        print(df.to_string(index=False))
        
        print("\n\nDataFrame Info:")
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {list(df.columns)}")
        
        # Get summary statistics
        summary = manager.get_summary_statistics()
        print("\n\nSummary Statistics:")
        print("-" * 70)
        for key, value in summary.items():
            print(f"  {key}: {value}")
        
        # Export to CSV
        manager.export_results('experiment_results.csv', format='csv')
        print("\n✓ Results exported to 'experiment_results.csv'")
        
        # Export to JSON
        manager.export_results('experiment_results.json', format='json')
        print("✓ Results exported to 'experiment_results.json'\n")
        
    except ImportError:
        print("  pandas not available - skipping DataFrame export\n")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("SEEDHASH: Hierarchical Sampling & ML Experiment Tracking")
    print("=" * 70 + "\n")
    
    # Run all examples
    example_simple_random_sampling()
    example_stratified_sampling()
    example_cluster_sampling()
    example_systematic_sampling()
    example_deep_hierarchy()
    example_comparison_all_methods()
    example_export_results()
    
    print("=" * 70)
    print("ALL EXAMPLES COMPLETED ✅")
    print("=" * 70)
    print("\nKey Features Demonstrated:")
    print("  • 4 Sampling Methods: simple, stratified, cluster, systematic")
    print("  • Hierarchical Seeds: master → seeds → sub-seeds → ...")
    print("  • ML Tasks: regression, classification, unsupervised")
    print("  • Metrics: RMSE, R², accuracy, F1, silhouette score")
    print("  • DataFrame Export: CSV, JSON formats")
    print("  • Summary Statistics: aggregated across all experiments")
    print("=" * 70 + "\n")
