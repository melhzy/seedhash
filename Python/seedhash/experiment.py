"""Experimental seed management with hierarchical sampling and ML evaluation tracking."""

from __future__ import annotations

import random
from typing import List, Dict, Optional, Literal, Union, Any
from dataclasses import dataclass, field
from datetime import datetime
import warnings

# pandas is only needed for DataFrame output; methods that need it warn or
# raise when called, so a core-only install imports without warnings
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

from .core import SeedHashGenerator


SamplingMethod = Literal["simple", "stratified", "cluster", "systematic"]
MLTask = Literal["regression", "classification", "unsupervised", "supervised", 
                 "semi_supervised", "reinforcement", "federated"]


@dataclass
class ExperimentResult:
    """Store results from a single experiment run."""
    
    experiment_id: str
    seed_hierarchy: List[int]  # [master_seed, seed, sub_seed, ...]
    seed_level: int  # Depth in hierarchy (0=master, 1=seed, 2=sub_seed, etc.)
    sampling_method: str
    ml_task: Optional[str] = None
    metrics: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for DataFrame."""
        result = {
            'experiment_id': self.experiment_id,
            'seed_level': self.seed_level,
            'master_seed': self.seed_hierarchy[0] if self.seed_hierarchy else None,
            'seed': self.seed_hierarchy[1] if len(self.seed_hierarchy) > 1 else None,
            'sub_seed': self.seed_hierarchy[2] if len(self.seed_hierarchy) > 2 else None,
            'current_seed': self.seed_hierarchy[-1] if self.seed_hierarchy else None,
            'sampling_method': self.sampling_method,
            'ml_task': self.ml_task,
            'timestamp': self.timestamp,
        }
        
        # Add metrics as separate columns
        for metric_name, metric_value in self.metrics.items():
            result[f'metric_{metric_name}'] = metric_value
        
        # Add metadata as separate columns
        for meta_key, meta_value in self.metadata.items():
            result[f'meta_{meta_key}'] = meta_value
        
        return result


class SeedSampler:
    """Generate seeds using different sampling methods."""
    
    def __init__(self, master_seed: int):
        """Initialize with a master seed.
        
        Args:
            master_seed: The root seed for all sampling operations.
        """
        self.master_seed = master_seed
        self.rng = random.Random(master_seed)
    
    def simple_random_sampling(
        self, 
        n_samples: int,
        seed_range: tuple = (0, 2**31 - 1)
    ) -> List[int]:
        """Simple random sampling: Each seed has equal probability.
        
        Pure random selection without any structure or stratification.
        Best for: Unbiased random exploration of seed space.
        
        Args:
            n_samples: Number of seeds to generate.
            seed_range: (min, max) range for generated seeds.
        
        Returns:
            List of randomly generated seeds.
        """
        self.rng.seed(self.master_seed)
        return [self.rng.randint(*seed_range) for _ in range(n_samples)]
    
    def stratified_random_sampling(
        self,
        n_samples: int,
        seed_range: tuple = (0, 2**31 - 1),
        n_strata: int = 4
    ) -> List[int]:
        """Stratified random sampling: Divide seed space into strata, sample from each.
        
        Ensures coverage across different regions of the seed space.
        Best for: Ensuring representation across the entire seed range.
        
        Args:
            n_samples: Total number of seeds to generate.
            seed_range: (min, max) range for generated seeds.
            n_strata: Number of strata (divisions) in the seed space.
        
        Returns:
            List of stratified seeds with balanced coverage. When n_samples is
            not a multiple of n_strata, the extra samples go to the lowest strata.
            Strata are (max - min) // n_strata wide, so the few values left over
            at the top of the range are never drawn; changing that would change
            the seeds this method has always produced.
        
        Raises:
            ValueError: If max - min of seed_range is less than n_strata.
        """
        self.rng.seed(self.master_seed)
        
        min_seed, max_seed = seed_range
        if max_seed - min_seed < n_strata:
            raise ValueError(
                f"seed_range {seed_range} is too narrow for n_strata={n_strata}; "
                f"max - min must be at least n_strata"
            )
        stratum_size = (max_seed - min_seed) // n_strata
        samples_per_stratum = n_samples // n_strata
        remainder = n_samples % n_strata
        
        seeds = []
        for stratum_idx in range(n_strata):
            stratum_min = min_seed + (stratum_idx * stratum_size)
            stratum_max = stratum_min + stratum_size - 1
            
            # Add extra sample to first strata if there's a remainder
            n_samples_this_stratum = samples_per_stratum + (1 if stratum_idx < remainder else 0)
            
            for _ in range(n_samples_this_stratum):
                seeds.append(self.rng.randint(stratum_min, stratum_max))
        
        return seeds
    
    def cluster_random_sampling(
        self,
        n_samples: int,
        seed_range: tuple = (0, 2**31 - 1),
        n_clusters: int = 5,
        samples_per_cluster: Optional[int] = None
    ) -> List[int]:
        """Cluster random sampling: Group seeds into clusters, sample entire clusters.
        
        Selects random cluster centers, then generates seeds around each center.
        Best for: Testing groups of related seeds together.
        
        Args:
            n_samples: Total number of seeds to generate.
            seed_range: (min, max) range for generated seeds.
            n_clusters: Number of clusters to create.
            samples_per_cluster: Seeds per cluster (auto-calculated if None).
        
        Returns:
            List of clustered seeds grouped around random centers.
        """
        self.rng.seed(self.master_seed)
        
        if samples_per_cluster is None:
            samples_per_cluster = max(1, n_samples // n_clusters)
        
        min_seed, max_seed = seed_range
        cluster_radius = (max_seed - min_seed) // (n_clusters * 10)
        
        seeds = []
        samples_remaining = n_samples
        
        for cluster_idx in range(n_clusters):
            # Generate cluster center
            center = self.rng.randint(min_seed + cluster_radius, max_seed - cluster_radius)
            
            # Calculate samples for this cluster (ensure we reach exactly n_samples)
            if cluster_idx == n_clusters - 1:
                # Last cluster gets all remaining samples
                samples_this_cluster = samples_remaining
            else:
                samples_this_cluster = min(samples_per_cluster, samples_remaining)
            
            # Generate seeds around the center
            for _ in range(samples_this_cluster):
                offset = self.rng.randint(-cluster_radius, cluster_radius)
                seed = max(min_seed, min(max_seed, center + offset))
                seeds.append(seed)
                samples_remaining -= 1
                
                if samples_remaining == 0:
                    return seeds
        
        return seeds
    
    def systematic_random_sampling(
        self,
        n_samples: int,
        seed_range: tuple = (0, 2**31 - 1)
    ) -> List[int]:
        """Systematic random sampling: Select seeds at regular intervals.
        
        Picks a random starting point, then selects every k-th seed.
        Best for: Evenly distributed seed coverage with periodic sampling.
        
        Args:
            n_samples: Number of seeds to generate.
            seed_range: (min, max) range for generated seeds.
        
        Returns:
            List of systematically sampled seeds at regular intervals.
        
        Raises:
            ValueError: If n_samples is less than 1 or greater than max - min
                of seed_range (the interval would be 0, repeating one seed).
        """
        self.rng.seed(self.master_seed)
        
        min_seed, max_seed = seed_range
        if not 1 <= n_samples <= max_seed - min_seed:
            raise ValueError(
                f"n_samples must be between 1 and max - min of seed_range "
                f"({max_seed - min_seed}), got {n_samples}"
            )
        interval = (max_seed - min_seed) // n_samples
        
        # Random starting point within first interval. The last seed is at
        # most min_seed + n_samples * interval <= max_seed, so none wrap.
        start = self.rng.randint(min_seed, min(min_seed + interval, max_seed))
        
        return [start + (i * interval) for i in range(n_samples)]


class SeedExperimentManager:
    """Manage hierarchical seed experiments with multiple sampling methods and ML task tracking.
    
    This class provides a systematic way to:
    1. Generate hierarchical seeds (master → seeds → sub-seeds → ...)
    2. Apply different sampling methods (simple, stratified, cluster, systematic)
    3. Track experiments across different ML tasks
    4. Store and organize results in a pandas DataFrame
    
    Example:
        >>> manager = SeedExperimentManager("project_alpha")
        >>> manager.generate_seed_hierarchy(
        ...     n_seeds=10,
        ...     n_sub_seeds=5,
        ...     sampling_method="stratified"
        ... )
        >>> df = manager.get_results_dataframe()
    """
    
    def __init__(
        self,
        experiment_name: str,
        master_seed: Optional[int] = None
    ):
        """Initialize the experiment manager.
        
        Args:
            experiment_name: Name of the experiment (used to generate master seed).
            master_seed: Optional master seed (generated from name if not provided).
        """
        self.experiment_name = experiment_name
        
        if master_seed is None:
            # Generate master seed from experiment name
            gen = SeedHashGenerator(experiment_name)
            self.master_seed = gen.seed_number
        else:
            self.master_seed = master_seed
        
        self.sampler = SeedSampler(self.master_seed)
        self.results: List[ExperimentResult] = []
        self._seed_hierarchy: Dict[int, Dict] = {}
    
    def generate_seed_hierarchy(
        self,
        n_seeds: int = 10,
        n_sub_seeds: int = 5,
        max_depth: int = 2,
        sampling_method: SamplingMethod = "simple",
        seed_range: tuple = (0, 2**31 - 1)
    ) -> Dict[int, List[int]]:
        """Generate hierarchical seed structure: master → seeds → sub_seeds → ...
        
        Args:
            n_seeds: Number of seeds to generate from master seed.
            n_sub_seeds: Number of sub-seeds to generate from each seed.
            max_depth: Maximum depth of hierarchy (1=seeds only, 2=sub_seeds, etc.).
            sampling_method: Which sampling method to use.
            seed_range: (min, max) range for generated seeds.
        
        Returns:
            Dictionary mapping level to list of seeds at that level.
        """
        sampling_func = getattr(self.sampler, f"{sampling_method}_random_sampling")
        
        hierarchy = {0: [self.master_seed]}
        
        for depth in range(1, max_depth + 1):
            current_level_seeds = []
            n_samples = n_seeds if depth == 1 else n_sub_seeds
            
            for parent_seed in hierarchy[depth - 1]:
                # Create new sampler for this parent
                sampler = SeedSampler(parent_seed)
                sampling_func_local = getattr(sampler, f"{sampling_method}_random_sampling")
                
                # Generate child seeds
                child_seeds = sampling_func_local(n_samples, seed_range)
                current_level_seeds.extend(child_seeds)
                
                # Track hierarchy. Nodes are keyed by seed value, so a seed that
                # occurs more than once keeps the record from its first
                # occurrence; overwriting it would rewrite its parent and could
                # make a seed its own ancestor.
                parent_node = self._seed_hierarchy.setdefault(
                    parent_seed, {'children': [], 'level': depth - 1}
                )
                parent_node['children'].extend(child_seeds)
                
                for child in child_seeds:
                    self._seed_hierarchy.setdefault(
                        child, {'parent': parent_seed, 'children': [], 'level': depth}
                    )
            
            hierarchy[depth] = current_level_seeds
        
        return hierarchy
    
    def add_experiment_result(
        self,
        seed: int,
        ml_task: MLTask,
        metrics: Dict[str, float],
        sampling_method: SamplingMethod,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add an experiment result to the tracking system.
        
        Args:
            seed: The seed used for this experiment.
            ml_task: Type of ML task (regression, classification, etc.).
            metrics: Dictionary of metric names and values.
            sampling_method: Sampling method used to generate this seed.
            metadata: Optional additional information.
        """
        # Reconstruct seed hierarchy, stopping if a seed repeats so that a
        # cyclic parent chain cannot loop forever
        hierarchy = [seed]
        visited = {seed}
        current = seed
        while current in self._seed_hierarchy and 'parent' in self._seed_hierarchy[current]:
            parent = self._seed_hierarchy[current]['parent']
            if parent in visited:
                break
            visited.add(parent)
            hierarchy.insert(0, parent)
            current = parent
        
        # Add master seed if not present
        if not hierarchy or hierarchy[0] != self.master_seed:
            hierarchy.insert(0, self.master_seed)
        
        seed_level = len(hierarchy) - 1
        experiment_id = f"{self.experiment_name}_{ml_task}_seed{seed}"
        
        result = ExperimentResult(
            experiment_id=experiment_id,
            seed_hierarchy=hierarchy,
            seed_level=seed_level,
            sampling_method=sampling_method,
            ml_task=ml_task,
            # Copy so later changes to the caller's dicts don't alter this result
            metrics=dict(metrics),
            metadata=dict(metadata or {})
        )
        
        self.results.append(result)
    
    def get_results_dataframe(self) -> Union[pd.DataFrame, None]:
        """Get all experiment results as a pandas DataFrame.
        
        Returns:
            DataFrame with experiment results, or None if pandas not available.
        """
        if not PANDAS_AVAILABLE:
            warnings.warn("pandas is not installed. Cannot create DataFrame.")
            return None
        
        if not self.results:
            warnings.warn("No results to convert to DataFrame.")
            return pd.DataFrame()
        
        data = [result.to_dict() for result in self.results]
        df = pd.DataFrame(data)
        
        # Reorder columns for better readability
        priority_cols = [
            'experiment_id', 'seed_level', 'master_seed', 'seed', 'sub_seed',
            'current_seed', 'sampling_method', 'ml_task'
        ]
        
        existing_priority = [col for col in priority_cols if col in df.columns]
        metric_cols = sorted([col for col in df.columns if col.startswith('metric_')])
        meta_cols = sorted([col for col in df.columns if col.startswith('meta_')])
        other_cols = [col for col in df.columns if col not in existing_priority + metric_cols + meta_cols]
        
        df = df[existing_priority + metric_cols + meta_cols + other_cols]
        
        return df
    
    def get_summary_statistics(self) -> Dict:
        """Get summary statistics of all experiments.
        
        Returns:
            Dictionary with summary statistics.
        """
        if not PANDAS_AVAILABLE or not self.results:
            return {}
        
        df = self.get_results_dataframe()
        
        summary = {
            'total_experiments': len(self.results),
            'ml_tasks': df['ml_task'].value_counts().to_dict() if 'ml_task' in df else {},
            'sampling_methods': df['sampling_method'].value_counts().to_dict(),
            'seed_levels': df['seed_level'].value_counts().to_dict(),
        }
        
        # Calculate metric statistics
        metric_cols = [col for col in df.columns if col.startswith('metric_')]
        if metric_cols:
            summary['metric_statistics'] = {}
            for col in metric_cols:
                metric_name = col.replace('metric_', '')
                summary['metric_statistics'][metric_name] = {
                    'mean': float(df[col].mean()),
                    'std': float(df[col].std()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max())
                }
        
        return summary
    
    def export_results(self, filepath: str, format: str = 'csv') -> None:
        """Export results to a file.
        
        Args:
            filepath: Path to save the results.
            format: File format ('csv', 'json', 'excel').
        """
        if not PANDAS_AVAILABLE:
            raise ImportError("pandas is required for exporting results")
        
        df = self.get_results_dataframe()
        
        if format == 'csv':
            df.to_csv(filepath, index=False)
        elif format == 'json':
            df.to_json(filepath, orient='records', indent=2)
        elif format == 'excel':
            df.to_excel(filepath, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")


def _paired_arrays(y_true, y_pred):
    """Flatten y_true and y_pred, raising if they hold different numbers of values.
    
    Without this, shapes such as (n,) and (n, 1) broadcast to an (n, n) array
    and every metric is silently computed over all cross pairs.
    """
    y_true = np.ravel(np.asarray(y_true))
    y_pred = np.ravel(np.asarray(y_pred))
    if y_true.shape != y_pred.shape:
        raise ValueError(
            f"y_true and y_pred must have the same number of values, "
            f"got {y_true.size} and {y_pred.size}"
        )
    return y_true, y_pred


class MLMetrics:
    """Common ML evaluation metrics for different task types."""
    
    @staticmethod
    def regression_metrics(y_true, y_pred) -> Dict[str, float]:
        """Calculate regression metrics.
        
        Args:
            y_true: True values.
            y_pred: Predicted values.
        
        Returns:
            Dictionary with RMSE, MAE, R2, MAPE.
        """
        if not NUMPY_AVAILABLE:
            raise ImportError("numpy is required for metric calculation")
        
        y_true, y_pred = _paired_arrays(y_true, y_pred)
        
        mse = np.mean((y_true - y_pred) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(y_true - y_pred))
        
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        # Mean Absolute Percentage Error (avoid division by zero)
        mask = y_true != 0
        mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100 if np.any(mask) else 0
        
        return {
            'rmse': float(rmse),
            'mae': float(mae),
            'r2': float(r2),
            'mape': float(mape)
        }
    
    @staticmethod
    def classification_metrics(y_true, y_pred, y_prob=None, pos_label=None) -> Dict[str, float]:
        """Calculate classification metrics.
        
        Args:
            y_true: True labels.
            y_pred: Predicted labels.
            y_prob: Predicted probabilities (optional, for AUC).
            pos_label: Positive class for binary tasks. Defaults to 1 when it is
                one of the two labels, otherwise to the larger label.
        
        Returns:
            Dictionary with accuracy, precision, recall, F1. Multi-class tasks
            use macro averages (F1 is the mean of the per-class F1 scores).
        """
        if not NUMPY_AVAILABLE:
            raise ImportError("numpy is required for metric calculation")
        
        y_true, y_pred = _paired_arrays(y_true, y_pred)
        
        # Accuracy
        accuracy = np.mean(y_true == y_pred)
        
        classes = np.unique(y_true)
        
        # For binary classification
        if len(classes) == 2:
            if pos_label is None:
                pos_label = 1 if 1 in classes.tolist() else classes[-1]
            tp = np.sum((y_true == pos_label) & (y_pred == pos_label))
            fp = np.sum((y_true != pos_label) & (y_pred == pos_label))
            fn = np.sum((y_true == pos_label) & (y_pred != pos_label))
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        else:
            # Multi-class: use macro average
            precisions, recalls, f1s = [], [], []
            
            for cls in classes:
                tp = np.sum((y_true == cls) & (y_pred == cls))
                fp = np.sum((y_true != cls) & (y_pred == cls))
                fn = np.sum((y_true == cls) & (y_pred != cls))
                
                prec = tp / (tp + fp) if (tp + fp) > 0 else 0
                rec = tp / (tp + fn) if (tp + fn) > 0 else 0
                
                precisions.append(prec)
                recalls.append(rec)
                f1s.append(2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0)
            
            precision = np.mean(precisions)
            recall = np.mean(recalls)
            f1 = np.mean(f1s)
        
        return {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1': float(f1)
        }
    
    @staticmethod
    def clustering_metrics(X, labels) -> Dict[str, float]:
        """Calculate clustering/unsupervised learning metrics.
        
        Args:
            X: Feature matrix.
            labels: Cluster labels.
        
        Returns:
            Dictionary with silhouette score, number of clusters and number of
            samples. The silhouette is 0.0 unless there are between 2 and
            n_samples - 1 clusters.
        """
        if not NUMPY_AVAILABLE:
            raise ImportError("numpy is required for metric calculation")
        
        X = np.asarray(X, dtype=float)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        labels = np.ravel(np.asarray(labels))
        if len(labels) != len(X):
            raise ValueError(
                f"X and labels must have the same number of samples, "
                f"got {len(X)} and {len(labels)}"
            )
        
        clusters = np.unique(labels)
        n_clusters = len(clusters)
        metrics = {
            'silhouette': 0.0,
            'n_clusters': int(n_clusters),
            'n_samples': int(len(X))
        }
        if n_clusters < 2 or n_clusters >= len(X):
            return metrics
        
        scores = []
        for i in range(len(X)):
            distances = np.linalg.norm(X - X[i], axis=1)
            
            # Exclude the point itself by index, not by value, so identical
            # points in the same cluster still count
            same_cluster = labels == labels[i]
            same_cluster[i] = False
            if not same_cluster.any():
                # A point alone in its cluster scores 0 (as in sklearn)
                scores.append(0.0)
                continue
            
            a = distances[same_cluster].mean()
            b = min(distances[labels == c].mean() for c in clusters if c != labels[i])
            scores.append((b - a) / max(a, b) if max(a, b) > 0 else 0.0)
        
        metrics['silhouette'] = float(np.mean(scores))
        return metrics
    
    @staticmethod
    def semi_supervised_metrics(
        y_labeled_true,
        y_labeled_pred,
        y_unlabeled_pseudo,
        pseudo_confidence=None,
        consistency_scores=None
    ) -> Dict[str, float]:
        """Calculate semi-supervised learning metrics.
        
        Args:
            y_labeled_true: True labels for labeled data.
            y_labeled_pred: Predictions for labeled data.
            y_unlabeled_pseudo: Pseudo-labels for unlabeled data.
            pseudo_confidence: Confidence scores for pseudo-labels (optional).
            consistency_scores: Consistency scores across augmentations (optional).
        
        Returns:
            Dictionary with labeled accuracy, pseudo-label quality, consistency, etc.
        """
        if not NUMPY_AVAILABLE:
            raise ImportError("numpy is required for metric calculation")
        
        y_labeled_true = np.array(y_labeled_true)
        y_labeled_pred = np.array(y_labeled_pred)
        y_unlabeled_pseudo = np.array(y_unlabeled_pseudo)
        
        # Labeled data accuracy
        labeled_accuracy = np.mean(y_labeled_true == y_labeled_pred)
        
        # Pseudo-label statistics
        n_labeled = len(y_labeled_true)
        n_unlabeled = len(y_unlabeled_pseudo)
        label_ratio = n_labeled / (n_labeled + n_unlabeled) if (n_labeled + n_unlabeled) > 0 else 0
        
        metrics = {
            'labeled_accuracy': float(labeled_accuracy),
            'n_labeled': int(n_labeled),
            'n_unlabeled': int(n_unlabeled),
            'label_ratio': float(label_ratio),
            'pseudo_label_diversity': float(len(np.unique(y_unlabeled_pseudo)) / max(1, len(np.unique(y_labeled_true))))
        }
        
        # Pseudo-label confidence (if provided)
        if pseudo_confidence is not None:
            pseudo_confidence = np.array(pseudo_confidence)
            metrics['avg_pseudo_confidence'] = float(np.mean(pseudo_confidence))
            metrics['high_confidence_ratio'] = float(np.mean(pseudo_confidence > 0.9))
        
        # Consistency score (if provided)
        if consistency_scores is not None:
            consistency_scores = np.array(consistency_scores)
            metrics['avg_consistency'] = float(np.mean(consistency_scores))
            metrics['consistency_std'] = float(np.std(consistency_scores))
        
        return metrics
    
    @staticmethod
    def reinforcement_learning_metrics(
        episode_rewards: List[float],
        episode_lengths: List[int],
        success_flags: Optional[List[bool]] = None,
        q_values: Optional[List[float]] = None
    ) -> Dict[str, float]:
        """Calculate reinforcement learning metrics.
        
        Args:
            episode_rewards: List of cumulative rewards per episode.
            episode_lengths: List of episode lengths (steps).
            success_flags: Binary success indicators per episode (optional).
            q_values: Q-values or value estimates (optional).
        
        Returns:
            Dictionary with episode metrics, success rate, convergence indicators.
        """
        if not NUMPY_AVAILABLE:
            raise ImportError("numpy is required for metric calculation")
        
        episode_rewards = np.array(episode_rewards)
        episode_lengths = np.array(episode_lengths)
        
        metrics = {
            'mean_reward': float(np.mean(episode_rewards)),
            'std_reward': float(np.std(episode_rewards)),
            'max_reward': float(np.max(episode_rewards)),
            'min_reward': float(np.min(episode_rewards)),
            'mean_episode_length': float(np.mean(episode_lengths)),
            'std_episode_length': float(np.std(episode_lengths)),
            'n_episodes': int(len(episode_rewards))
        }
        
        # Success rate (if provided)
        if success_flags is not None:
            success_flags = np.array(success_flags)
            metrics['success_rate'] = float(np.mean(success_flags))
            metrics['n_successes'] = int(np.sum(success_flags))
        
        # Q-value statistics (if provided)
        if q_values is not None:
            q_values = np.array(q_values)
            metrics['mean_q_value'] = float(np.mean(q_values))
            metrics['std_q_value'] = float(np.std(q_values))
            metrics['max_q_value'] = float(np.max(q_values))
        
        # Convergence indicators
        if len(episode_rewards) >= 10:
            # Recent performance (last 20%, at least 10 episodes), capped at
            # half the episodes so the early and recent windows never overlap
            recent_window = min(max(10, len(episode_rewards) // 5), len(episode_rewards) // 2)
            recent_rewards = episode_rewards[-recent_window:]
            early_mean = np.mean(episode_rewards[:recent_window])
            metrics['recent_mean_reward'] = float(np.mean(recent_rewards))
            # Divide by the magnitude so that rising negative rewards
            # (e.g. -100 to -50) count as improvement
            metrics['improvement_rate'] = float(
                (np.mean(recent_rewards) - early_mean) / (abs(early_mean) + 1e-8)
            )
        
        return metrics
    
    @staticmethod
    def federated_learning_metrics(
        client_accuracies: List[float],
        communication_rounds: int,
        client_losses: Optional[List[float]] = None,
        model_divergences: Optional[List[float]] = None,
        participation_rates: Optional[List[float]] = None
    ) -> Dict[str, float]:
        """Calculate federated learning metrics.
        
        Args:
            client_accuracies: List of accuracy values per client.
            communication_rounds: Number of communication rounds completed.
            client_losses: Loss values per client (optional).
            model_divergences: Model divergence from global model per client (optional).
            participation_rates: Client participation rates (optional).
        
        Returns:
            Dictionary with federation metrics, fairness, convergence indicators.
        """
        if not NUMPY_AVAILABLE:
            raise ImportError("numpy is required for metric calculation")
        
        client_accuracies = np.array(client_accuracies)
        
        metrics = {
            'global_accuracy': float(np.mean(client_accuracies)),
            'accuracy_std': float(np.std(client_accuracies)),
            'min_client_accuracy': float(np.min(client_accuracies)),
            'max_client_accuracy': float(np.max(client_accuracies)),
            'accuracy_variance': float(np.var(client_accuracies)),
            'n_clients': int(len(client_accuracies)),
            'communication_rounds': int(communication_rounds)
        }
        
        # Fairness metrics (coefficient of variation)
        if np.mean(client_accuracies) > 0:
            metrics['fairness_cv'] = float(np.std(client_accuracies) / np.mean(client_accuracies))
        else:
            metrics['fairness_cv'] = float('inf')
        
        # Client losses (if provided)
        if client_losses is not None:
            client_losses = np.array(client_losses)
            metrics['global_loss'] = float(np.mean(client_losses))
            metrics['loss_std'] = float(np.std(client_losses))
        
        # Model divergence (if provided)
        if model_divergences is not None:
            model_divergences = np.array(model_divergences)
            metrics['avg_model_divergence'] = float(np.mean(model_divergences))
            metrics['max_model_divergence'] = float(np.max(model_divergences))
        
        # Participation metrics (if provided)
        if participation_rates is not None:
            participation_rates = np.array(participation_rates)
            metrics['avg_participation_rate'] = float(np.mean(participation_rates))
            metrics['min_participation_rate'] = float(np.min(participation_rates))
        
        # Convergence indicator (accuracy range)
        metrics['convergence_indicator'] = float(
            1.0 - (np.max(client_accuracies) - np.min(client_accuracies))
        )
        
        return metrics
