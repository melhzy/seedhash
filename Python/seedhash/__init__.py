"""SeedHash: Deterministic seed generation from string inputs using MD5 hashing.

This library provides a simple way to generate reproducible random seeds
from string inputs, useful for reproducible experiments and simulations.

Features:
- Generate deterministic seeds from string inputs
- Deep learning framework support (PyTorch, TensorFlow, NumPy)
- Seeding for single-GPU, multi-GPU and multi-node PyTorch jobs
- Hierarchical seed management for systematic experiments
- Multiple sampling methods (simple, stratified, cluster, systematic)
- ML experiment tracking with pandas DataFrame output
"""

from .core import SeedHashGenerator, get_global_rank
from .experiment import (
    SeedExperimentManager,
    SeedSampler,
    MLMetrics,
    ExperimentResult
)

__version__ = "0.3.0"
__author__ = "melhzy"
__all__ = [
    "SeedHashGenerator",
    "get_global_rank",
    "SeedExperimentManager",
    "SeedSampler",
    "MLMetrics",
    "ExperimentResult"
]
