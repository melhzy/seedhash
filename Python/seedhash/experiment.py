"""Experimental seed management with hierarchical sampling and ML evaluation tracking."""

import random
from typing import List, Dict, Optional, Literal, Union, Any
from dataclasses import dataclass, field
from datetime import datetime
import warnings

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    warnings.warn(
        "pandas is not installed. Install with: pip install pandas\n"
        "Experiment tracking requires pandas for DataFrame output."
    )

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

from .core import SeedHashGenerator


SamplingMethod = Literal["simple", "stratified", "cluster", "systematic"]
MLTask = Literal["regression", "classification", "unsupervised", "supervised"]


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
            List of stratified seeds with balanced coverage.
        """
        self.rng.seed(self.master_seed)
        
        min_seed, max_seed = seed_range
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
        for _ in range(n_clusters):
            # Generate cluster center
            center = self.rng.randint(min_seed + cluster_radius, max_seed - cluster_radius)
            
            # Generate seeds around the center
            for _ in range(samples_per_cluster):
                offset = self.rng.randint(-cluster_radius, cluster_radius)
                seed = max(min_seed, min(max_seed, center + offset))
                seeds.append(seed)
                
                if len(seeds) >= n_samples:
                    return seeds[:n_samples]
        
        return seeds[:n_samples]
    
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
        """
        self.rng.seed(self.master_seed)
        
        min_seed, max_seed = seed_range
        interval = (max_seed - min_seed) // n_samples
        
        # Random starting point within first interval
        start = self.rng.randint(min_seed, min(min_seed + interval, max_seed))
        
        seeds = []
        for i in range(n_samples):
            seed = start + (i * interval)
            if seed <= max_seed:
                seeds.append(seed)
            else:
                # Wrap around if needed
                seeds.append(min_seed + (seed - max_seed))
        
        return seeds


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
                
                # Track hierarchy
                if parent_seed not in self._seed_hierarchy:
                    self._seed_hierarchy[parent_seed] = {'children': [], 'level': depth - 1}
                
                # Ensure 'children' key exists
                if 'children' not in self._seed_hierarchy[parent_seed]:
                    self._seed_hierarchy[parent_seed]['children'] = []
                    
                self._seed_hierarchy[parent_seed]['children'].extend(child_seeds)
                
                for child in child_seeds:
                    self._seed_hierarchy[child] = {'parent': parent_seed, 'level': depth}
            
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
        # Reconstruct seed hierarchy
        hierarchy = [seed]
        current = seed
        while current in self._seed_hierarchy and 'parent' in self._seed_hierarchy[current]:
            parent = self._seed_hierarchy[current]['parent']
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
            metrics=metrics,
            metadata=metadata or {}
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
        
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        
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
    def classification_metrics(y_true, y_pred, y_prob=None) -> Dict[str, float]:
        """Calculate classification metrics.
        
        Args:
            y_true: True labels.
            y_pred: Predicted labels.
            y_prob: Predicted probabilities (optional, for AUC).
        
        Returns:
            Dictionary with accuracy, precision, recall, F1.
        """
        if not NUMPY_AVAILABLE:
            raise ImportError("numpy is required for metric calculation")
        
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        
        # Accuracy
        accuracy = np.mean(y_true == y_pred)
        
        # For binary classification
        if len(np.unique(y_true)) == 2:
            tp = np.sum((y_true == 1) & (y_pred == 1))
            fp = np.sum((y_true == 0) & (y_pred == 1))
            fn = np.sum((y_true == 1) & (y_pred == 0))
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        else:
            # Multi-class: use macro average
            classes = np.unique(y_true)
            precisions, recalls = [], []
            
            for cls in classes:
                tp = np.sum((y_true == cls) & (y_pred == cls))
                fp = np.sum((y_true != cls) & (y_pred == cls))
                fn = np.sum((y_true == cls) & (y_pred != cls))
                
                prec = tp / (tp + fp) if (tp + fp) > 0 else 0
                rec = tp / (tp + fn) if (tp + fn) > 0 else 0
                
                precisions.append(prec)
                recalls.append(rec)
            
            precision = np.mean(precisions)
            recall = np.mean(recalls)
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
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
            Dictionary with silhouette score and Davies-Bouldin index.
        """
        if not NUMPY_AVAILABLE:
            raise ImportError("numpy is required for metric calculation")
        
        X = np.array(X)
        labels = np.array(labels)
        
        # Simplified silhouette score calculation
        n_clusters = len(np.unique(labels))
        if n_clusters < 2 or n_clusters >= len(X):
            return {'silhouette': 0.0, 'davies_bouldin': float('inf')}
        
        # Calculate intra-cluster distances (a)
        a_values = []
        for i in range(len(X)):
            same_cluster = X[labels == labels[i]]
            if len(same_cluster) > 1:
                a = np.mean([np.linalg.norm(X[i] - x) for x in same_cluster if not np.array_equal(X[i], x)])
            else:
                a = 0
            a_values.append(a)
        
        # Calculate nearest-cluster distances (b)
        b_values = []
        for i in range(len(X)):
            min_b = float('inf')
            for cluster in np.unique(labels):
                if cluster != labels[i]:
                    other_cluster = X[labels == cluster]
                    b = np.mean([np.linalg.norm(X[i] - x) for x in other_cluster])
                    min_b = min(min_b, b)
            b_values.append(min_b)
        
        # Silhouette score
        silhouette = np.mean([
            (b - a) / max(a, b) if max(a, b) > 0 else 0
            for a, b in zip(a_values, b_values)
        ])
        
        return {
            'silhouette': float(silhouette),
            'n_clusters': int(n_clusters),
            'n_samples': int(len(X))
        }
