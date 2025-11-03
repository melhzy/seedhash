"""SeedHash: Deterministic seed generation from string inputs using MD5 hashing.

This library provides a simple way to generate reproducible random seeds
from string inputs, useful for reproducible experiments and simulations.

Features:
- Generate deterministic seeds from string inputs
- Deep learning framework support (PyTorch, TensorFlow, NumPy)
- Hierarchical seed management for systematic experiments
- Multiple sampling methods (simple, stratified, cluster, systematic)
- ML experiment tracking with pandas DataFrame output
"""

from .core import SeedHashGenerator
from .experiment import (
    SeedExperimentManager,
    SeedSampler,
    MLMetrics,
    ExperimentResult
)

__version__ = "0.2.0"
__author__ = "melhzy"
__all__ = [
    "SeedHashGenerator",
    "SeedExperimentManager",
    "SeedSampler",
    "MLMetrics",
    "ExperimentResult"
]
