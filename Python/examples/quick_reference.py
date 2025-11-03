"""
Quick reference guide for hierarchical seed sampling and experiment management.

This is a condensed guide showing the most common use cases.
"""

import sys
sys.path.insert(0, 'Python')

from seedhash import SeedExperimentManager, MLMetrics


# ============================================================================
# USE CASE 1: Quick Start - Simple Experiments
# ============================================================================

def quick_start():
    """Simplest way to get started."""
    
    # Create manager
    manager = SeedExperimentManager("my_project")
    
    # Generate seeds
    hierarchy = manager.generate_seed_hierarchy(
        n_seeds=5,
        n_sub_seeds=3,
        sampling_method="simple"
    )
    
    print(f"Master seed: {manager.master_seed}")
    print(f"Generated {len(hierarchy[2])} sub-seeds")
    return manager


# ============================================================================
# USE CASE 2: ML Workflow - Complete Pipeline
# ============================================================================

def ml_workflow_example():
    """Complete ML experiment workflow."""
    
    import random
    
    # Initialize
    manager = SeedExperimentManager("regression_benchmark")
    
    # Generate stratified seeds for better coverage
    hierarchy = manager.generate_seed_hierarchy(
        n_seeds=10,
        n_sub_seeds=5,
        max_depth=2,
        sampling_method="stratified"
    )
    
    # Run experiments
    for seed in hierarchy[2][:20]:  # Use 20 seeds
        random.seed(seed)
        
        # Simulated model training
        y_true = [random.uniform(0, 100) for _ in range(100)]
        y_pred = [val + random.uniform(-5, 5) for val in y_true]
        
        # Calculate metrics
        metrics = MLMetrics.regression_metrics(y_true, y_pred)
        
        # Track result
        manager.add_experiment_result(
            seed=seed,
            ml_task="regression",
            metrics=metrics,
            sampling_method="stratified",
            metadata={"model": "LinearRegression", "samples": 100}
        )
    
    # Analyze
    df = manager.get_results_dataframe()
    print(f"\nExperiments run: {len(df)}")
    print(f"Average RMSE: {df['metric_rmse'].mean():.3f}")
    print(f"Average R²: {df['metric_r2'].mean():.3f}")
    
    # Export
    manager.export_results('ml_results.csv')
    print("✓ Results exported to ml_results.csv")
    
    return manager


# ============================================================================
# USE CASE 3: Comparing Sampling Methods
# ============================================================================

def compare_sampling_methods():
    """Compare different sampling methods."""
    
    methods = ["simple", "stratified", "cluster", "systematic"]
    
    print("\n" + "="*70)
    print("Comparing Sampling Methods")
    print("="*70 + "\n")
    
    for method in methods:
        manager = SeedExperimentManager(f"test_{method}")
        hierarchy = manager.generate_seed_hierarchy(
            n_seeds=10,
            sampling_method=method
        )
        
        print(f"{method.capitalize():12} | Master: {manager.master_seed:11} | "
              f"Seeds: {len(hierarchy[1]):3}")


# ============================================================================
# USE CASE 4: Deep Hierarchy for Complex Experiments
# ============================================================================

def deep_hierarchy_example():
    """Create deep hierarchies for complex experiment structures."""
    
    manager = SeedExperimentManager("deep_experiment")
    
    # Create 4-level hierarchy
    hierarchy = manager.generate_seed_hierarchy(
        n_seeds=3,
        n_sub_seeds=2,
        max_depth=3,  # Master → Seeds → Sub-seeds → Sub-sub-seeds
        sampling_method="systematic"
    )
    
    print("\n" + "="*70)
    print("Deep Hierarchy Structure")
    print("="*70)
    
    level_names = ["Master", "Seeds", "Sub-seeds", "Sub-sub-seeds"]
    for level, seeds in hierarchy.items():
        print(f"Level {level} ({level_names[level]:13}): {len(seeds):3} seeds")
    
    total = sum(len(seeds) for seeds in hierarchy.values())
    print(f"\nTotal seeds in hierarchy: {total}")


# ============================================================================
# USE CASE 5: DataFrame Analysis
# ============================================================================

def dataframe_analysis():
    """Analyze results using DataFrame."""
    
    try:
        import pandas as pd
        
        manager = ml_workflow_example()
        df = manager.get_results_dataframe()
        
        print("\n" + "="*70)
        print("DataFrame Analysis")
        print("="*70 + "\n")
        
        # Basic stats
        print("Metric Statistics:")
        print(df[['metric_rmse', 'metric_mae', 'metric_r2']].describe())
        
        # Summary
        summary = manager.get_summary_statistics()
        print("\nExperiment Summary:")
        for key, value in summary.items():
            if key != 'metric_statistics':
                print(f"  {key}: {value}")
        
    except ImportError:
        print("pandas not available for analysis")


# ============================================================================
# CHEAT SHEET
# ============================================================================

def print_cheat_sheet():
    """Print quick reference cheat sheet."""
    
    cheat_sheet = """
╔══════════════════════════════════════════════════════════════════════╗
║                   SEEDHASH - QUICK REFERENCE                         ║
╚══════════════════════════════════════════════════════════════════════╝

1. CREATE MANAGER
   ────────────────────────────────────────────────────────────────────
   from seedhash import SeedExperimentManager
   
   manager = SeedExperimentManager("project_name")

2. GENERATE SEEDS
   ────────────────────────────────────────────────────────────────────
   hierarchy = manager.generate_seed_hierarchy(
       n_seeds=10,              # Number of seeds from master
       n_sub_seeds=5,           # Number of sub-seeds from each seed
       max_depth=2,             # Hierarchy depth
       sampling_method="simple" # simple|stratified|cluster|systematic
   )

3. SAMPLING METHODS
   ────────────────────────────────────────────────────────────────────
   • simple:      Pure random, unbiased exploration
   • stratified:  Balanced coverage across seed space
   • cluster:     Grouped seeds, test related seeds together
   • systematic:  Regular intervals, evenly distributed

4. TRACK EXPERIMENTS
   ────────────────────────────────────────────────────────────────────
   from seedhash import MLMetrics
   
   metrics = MLMetrics.regression_metrics(y_true, y_pred)
   # or MLMetrics.classification_metrics(y_true, y_pred)
   # or MLMetrics.clustering_metrics(X, labels)
   
   manager.add_experiment_result(
       seed=seed,
       ml_task="regression",  # regression|classification|unsupervised
       metrics=metrics,
       sampling_method="simple",
       metadata={"model": "RF", "n_estimators": 100}
   )

5. EXPORT RESULTS
   ────────────────────────────────────────────────────────────────────
   df = manager.get_results_dataframe()
   manager.export_results('results.csv', format='csv')
   manager.export_results('results.json', format='json')

6. ANALYZE
   ────────────────────────────────────────────────────────────────────
   summary = manager.get_summary_statistics()
   print(df['metric_rmse'].mean())
   print(df.groupby('sampling_method')['metric_r2'].mean())

7. INSTALLATION
   ────────────────────────────────────────────────────────────────────
   pip install "git+...#subdirectory=Python[all]"
   # Includes: pandas, numpy, torch, tensorflow

╚══════════════════════════════════════════════════════════════════════╝
"""
    print(cheat_sheet)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("SEEDHASH - Quick Reference Examples")
    print("="*70 + "\n")
    
    print_cheat_sheet()
    
    print("\n" + "="*70)
    print("Running Examples...")
    print("="*70 + "\n")
    
    print("Example 1: Quick Start")
    print("-" * 70)
    quick_start()
    
    print("\n\nExample 2: ML Workflow")
    print("-" * 70)
    ml_workflow_example()
    
    print("\n\nExample 3: Comparing Sampling Methods")
    compare_sampling_methods()
    
    print("\n\nExample 4: Deep Hierarchy")
    deep_hierarchy_example()
    
    print("\n\nExample 5: DataFrame Analysis")
    dataframe_analysis()
    
    print("\n" + "="*70)
    print("All examples completed! ✅")
    print("="*70 + "\n")
