"""
Examples demonstrating advanced ML paradigms with hierarchical seed sampling.

This script demonstrates:
1. Semi-supervised learning experiments
2. Reinforcement learning experiments
3. Federated learning experiments
"""

import sys
sys.path.insert(0, 'Python')

from seedhash import SeedExperimentManager, MLMetrics
import random


def example_semi_supervised_learning():
    """Example 1: Semi-Supervised Learning Experiments."""
    print("=" * 70)
    print("Example 1: Semi-Supervised Learning")
    print("=" * 70)
    
    manager = SeedExperimentManager("semi_supervised_study")
    
    print(f"Experiment: {manager.experiment_name}")
    print(f"Master Seed: {manager.master_seed}\n")
    
    # Generate seeds with stratified sampling
    hierarchy = manager.generate_seed_hierarchy(
        n_seeds=5,
        n_sub_seeds=4,
        max_depth=2,
        sampling_method="stratified"
    )
    
    print(f"Generated {len(hierarchy[2])} seeds for experiments\n")
    
    # Simulate semi-supervised learning experiments
    print("Running semi-supervised learning experiments...")
    print("(Simulating label propagation with 10% labeled data)\n")
    
    for i, seed in enumerate(hierarchy[2][:8]):
        random.seed(seed)
        
        # Simulate labeled data (10% of dataset)
        n_labeled = 100
        n_unlabeled = 900
        
        # Labeled data predictions
        y_labeled_true = [random.randint(0, 2) for _ in range(n_labeled)]
        y_labeled_pred = [
            val if random.random() > 0.15 else random.randint(0, 2) 
            for val in y_labeled_true
        ]
        
        # Pseudo-labels for unlabeled data
        y_unlabeled_pseudo = [random.randint(0, 2) for _ in range(n_unlabeled)]
        pseudo_confidence = [random.uniform(0.6, 0.99) for _ in range(n_unlabeled)]
        consistency_scores = [random.uniform(0.7, 0.95) for _ in range(n_unlabeled)]
        
        # Calculate semi-supervised metrics
        metrics = MLMetrics.semi_supervised_metrics(
            y_labeled_true,
            y_labeled_pred,
            y_unlabeled_pseudo,
            pseudo_confidence,
            consistency_scores
        )
        
        # Track experiment
        manager.add_experiment_result(
            seed=seed,
            ml_task="semi_supervised",
            metrics=metrics,
            sampling_method="stratified",
            metadata={
                "algorithm": "pseudo_labeling",
                "label_ratio": 0.1,
                "confidence_threshold": 0.9
            }
        )
        
        print(f"  Seed {seed}:")
        print(f"    Labeled accuracy: {metrics['labeled_accuracy']:.3f}")
        print(f"    Pseudo confidence: {metrics['avg_pseudo_confidence']:.3f}")
        print(f"    Consistency: {metrics['avg_consistency']:.3f}")
        print(f"    Label ratio: {metrics['label_ratio']:.1%}")
    
    # Get results
    df = manager.get_results_dataframe()
    print(f"\n✓ Semi-supervised experiments completed")
    print(f"  Average labeled accuracy: {df['metric_labeled_accuracy'].mean():.3f}")
    print(f"  Average pseudo confidence: {df['metric_avg_pseudo_confidence'].mean():.3f}\n")
    
    return manager


def example_reinforcement_learning():
    """Example 2: Reinforcement Learning Experiments."""
    print("=" * 70)
    print("Example 2: Reinforcement Learning")
    print("=" * 70)
    
    manager = SeedExperimentManager("rl_cartpole_study")
    
    print(f"Experiment: {manager.experiment_name}")
    print(f"Master Seed: {manager.master_seed}\n")
    
    # Generate seeds with systematic sampling
    hierarchy = manager.generate_seed_hierarchy(
        n_seeds=6,
        n_sub_seeds=3,
        max_depth=2,
        sampling_method="systematic"
    )
    
    print(f"Generated {len(hierarchy[2])} seeds for RL training\n")
    
    # Simulate RL training experiments
    print("Running RL training experiments...")
    print("(Simulating CartPole environment)\n")
    
    for i, seed in enumerate(hierarchy[2][:10]):
        random.seed(seed)
        
        # Simulate episode rewards (improving over episodes)
        n_episodes = 100
        episode_rewards = []
        episode_lengths = []
        success_flags = []
        q_values = []
        
        for ep in range(n_episodes):
            # Simulate learning progress
            base_reward = 50 + (ep / n_episodes) * 150
            noise = random.uniform(-30, 30)
            reward = max(10, base_reward + noise)
            
            episode_rewards.append(reward)
            episode_lengths.append(int(random.uniform(50, 200)))
            success_flags.append(reward > 195)  # CartPole success threshold
            q_values.append(random.uniform(10, reward))
        
        # Calculate RL metrics
        metrics = MLMetrics.reinforcement_learning_metrics(
            episode_rewards,
            episode_lengths,
            success_flags,
            q_values
        )
        
        # Track experiment
        manager.add_experiment_result(
            seed=seed,
            ml_task="reinforcement",
            metrics=metrics,
            sampling_method="systematic",
            metadata={
                "environment": "CartPole-v1",
                "algorithm": "DQN",
                "n_episodes": n_episodes,
                "learning_rate": 0.001
            }
        )
        
        print(f"  Seed {seed}:")
        print(f"    Mean reward: {metrics['mean_reward']:.1f}")
        print(f"    Success rate: {metrics['success_rate']:.1%}")
        print(f"    Episode length: {metrics['mean_episode_length']:.1f}")
        print(f"    Improvement rate: {metrics.get('improvement_rate', 0):.2%}")
    
    # Get results
    df = manager.get_results_dataframe()
    print(f"\n✓ RL experiments completed")
    print(f"  Average mean reward: {df['metric_mean_reward'].mean():.1f}")
    print(f"  Average success rate: {df['metric_success_rate'].mean():.1%}")
    print(f"  Best mean reward: {df['metric_mean_reward'].max():.1f}\n")
    
    return manager


def example_federated_learning():
    """Example 3: Federated Learning Experiments."""
    print("=" * 70)
    print("Example 3: Federated Learning")
    print("=" * 70)
    
    manager = SeedExperimentManager("federated_mnist_study")
    
    print(f"Experiment: {manager.experiment_name}")
    print(f"Master Seed: {manager.master_seed}\n")
    
    # Generate seeds with cluster sampling (for client groups)
    hierarchy = manager.generate_seed_hierarchy(
        n_seeds=5,
        n_sub_seeds=4,
        max_depth=2,
        sampling_method="cluster"
    )
    
    print(f"Generated {len(hierarchy[2])} seeds for FL rounds\n")
    
    # Simulate federated learning experiments
    print("Running federated learning experiments...")
    print("(Simulating 10 clients with IID data)\n")
    
    for i, seed in enumerate(hierarchy[2][:8]):
        random.seed(seed)
        
        # Simulate federated learning setup
        n_clients = 10
        communication_rounds = 50
        
        # Client accuracies (heterogeneous)
        base_accuracy = 0.85
        client_accuracies = [
            max(0.5, min(0.99, base_accuracy + random.uniform(-0.15, 0.15)))
            for _ in range(n_clients)
        ]
        
        # Client losses
        client_losses = [
            (1.0 - acc) * random.uniform(0.8, 1.2)
            for acc in client_accuracies
        ]
        
        # Model divergences (how far client models drift from global)
        model_divergences = [random.uniform(0.01, 0.1) for _ in range(n_clients)]
        
        # Participation rates
        participation_rates = [random.uniform(0.7, 1.0) for _ in range(n_clients)]
        
        # Calculate federated learning metrics
        metrics = MLMetrics.federated_learning_metrics(
            client_accuracies,
            communication_rounds,
            client_losses,
            model_divergences,
            participation_rates
        )
        
        # Track experiment
        manager.add_experiment_result(
            seed=seed,
            ml_task="federated",
            metrics=metrics,
            sampling_method="cluster",
            metadata={
                "dataset": "MNIST",
                "aggregation": "FedAvg",
                "n_clients": n_clients,
                "client_epochs": 5,
                "data_distribution": "IID"
            }
        )
        
        print(f"  Seed {seed}:")
        print(f"    Global accuracy: {metrics['global_accuracy']:.3f}")
        print(f"    Accuracy variance: {metrics['accuracy_variance']:.4f}")
        print(f"    Fairness (CV): {metrics['fairness_cv']:.3f}")
        print(f"    Convergence: {metrics['convergence_indicator']:.3f}")
    
    # Get results
    df = manager.get_results_dataframe()
    print(f"\n✓ Federated learning experiments completed")
    print(f"  Average global accuracy: {df['metric_global_accuracy'].mean():.3f}")
    print(f"  Average fairness CV: {df['metric_fairness_cv'].mean():.3f}")
    print(f"  Best convergence: {df['metric_convergence_indicator'].max():.3f}\n")
    
    return manager


def example_mixed_advanced_paradigms():
    """Example 4: Mixed Advanced ML Paradigms."""
    print("=" * 70)
    print("Example 4: Mixed Advanced ML Paradigms")
    print("=" * 70)
    
    manager = SeedExperimentManager("mixed_advanced_ml")
    
    # Generate seeds
    hierarchy = manager.generate_seed_hierarchy(
        n_seeds=4,
        n_sub_seeds=3,
        max_depth=2,
        sampling_method="simple"
    )
    
    print(f"Running mixed experiments across all paradigms...\n")
    
    seeds = hierarchy[2][:9]
    paradigms = ["semi_supervised", "reinforcement", "federated"] * 3
    
    for seed, paradigm in zip(seeds, paradigms):
        random.seed(seed)
        
        if paradigm == "semi_supervised":
            # Quick semi-supervised experiment
            y_labeled_true = [random.randint(0, 1) for _ in range(50)]
            y_labeled_pred = [val if random.random() > 0.1 else 1-val for val in y_labeled_true]
            y_unlabeled_pseudo = [random.randint(0, 1) for _ in range(450)]
            
            metrics = MLMetrics.semi_supervised_metrics(
                y_labeled_true, y_labeled_pred, y_unlabeled_pseudo
            )
            
        elif paradigm == "reinforcement":
            # Quick RL experiment
            episode_rewards = [random.uniform(50, 200) for _ in range(50)]
            episode_lengths = [random.randint(50, 200) for _ in range(50)]
            success_flags = [r > 150 for r in episode_rewards]
            
            metrics = MLMetrics.reinforcement_learning_metrics(
                episode_rewards, episode_lengths, success_flags
            )
            
        else:  # federated
            # Quick FL experiment
            client_accuracies = [random.uniform(0.7, 0.95) for _ in range(5)]
            communication_rounds = 20
            
            metrics = MLMetrics.federated_learning_metrics(
                client_accuracies, communication_rounds
            )
        
        manager.add_experiment_result(
            seed=seed,
            ml_task=paradigm,
            metrics=metrics,
            sampling_method="simple",
            metadata={"paradigm": paradigm}
        )
        
        print(f"  {paradigm:20} | Seed: {seed}")
    
    # Analysis
    df = manager.get_results_dataframe()
    print(f"\n✓ Mixed paradigm experiments completed")
    print(f"  Total experiments: {len(df)}")
    print(f"  Paradigm distribution:")
    for paradigm, count in df['ml_task'].value_counts().items():
        print(f"    {paradigm}: {count}")
    print()
    
    return manager


def example_export_and_analysis():
    """Example 5: Export and Analyze Advanced ML Results."""
    print("=" * 70)
    print("Example 5: Export & Analysis")
    print("=" * 70)
    
    # Run all experiments
    manager_ssl = example_semi_supervised_learning()
    
    # Export results
    try:
        manager_ssl.export_results('advanced_ml_results.csv', format='csv')
        manager_ssl.export_results('advanced_ml_results.json', format='json')
        
        print("✓ Results exported to:")
        print("  - advanced_ml_results.csv")
        print("  - advanced_ml_results.json\n")
        
        # Get summary
        summary = manager_ssl.get_summary_statistics()
        
        print("Summary Statistics:")
        print("-" * 70)
        print(f"  Total experiments: {summary['total_experiments']}")
        print(f"  ML tasks: {summary['ml_tasks']}")
        print(f"  Sampling methods: {summary['sampling_methods']}")
        
        if 'metric_statistics' in summary:
            print("\n  Key Metrics:")
            for metric, stats in list(summary['metric_statistics'].items())[:5]:
                print(f"    {metric}:")
                print(f"      Mean: {stats['mean']:.4f}")
                print(f"      Std:  {stats['std']:.4f}")
        
    except Exception as e:
        print(f"Error exporting: {e}")
    
    print()


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("SEEDHASH: Advanced ML Paradigms Examples")
    print("=" * 70 + "\n")
    
    try:
        import numpy as np
        print("✓ NumPy available - all examples will run\n")
    except ImportError:
        print("✗ NumPy not available - install with: pip install numpy\n")
        exit(1)
    
    example_semi_supervised_learning()
    print()
    
    example_reinforcement_learning()
    print()
    
    example_federated_learning()
    print()
    
    example_mixed_advanced_paradigms()
    print()
    
    example_export_and_analysis()
    
    print("=" * 70)
    print("ALL ADVANCED ML EXAMPLES COMPLETED ✅")
    print("=" * 70)
    print("\nKey Features Demonstrated:")
    print("  • Semi-Supervised Learning: label propagation, pseudo-labeling")
    print("  • Reinforcement Learning: episode rewards, success rates, Q-values")
    print("  • Federated Learning: client accuracy, fairness, convergence")
    print("  • Mixed Paradigms: combining multiple learning approaches")
    print("  • Comprehensive Metrics: specialized for each paradigm")
    print("=" * 70 + "\n")
