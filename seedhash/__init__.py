"""SeedHash: Deterministic seed generation from string inputs using MD5 hashing.

This library provides a simple way to generate reproducible random seeds
from string inputs, useful for reproducible experiments and simulations.
"""

from .core import SeedHashGenerator

__version__ = "0.1.0"
__author__ = "melhzy"
__all__ = ["SeedHashGenerator"]
