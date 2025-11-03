"""Core module for seed generation using hash-based initialization."""

import random
import hashlib
import os
import warnings
from typing import List, Optional, Literal


# Optional deep learning framework imports
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


FrameworkType = Literal["torch", "tensorflow", "numpy", "all", "python"]


class SeedHashGenerator:
    """Generate deterministic random seeds from string input using MD5 hashing.
    
    This class allows users to generate reproducible sequences of random numbers
    by hashing an input string and using it as a seed for Python's random module
    and optionally for deep learning frameworks (PyTorch, TensorFlow, NumPy).
    
    Attributes:
        input_string (str): The string used to generate the initial seed.
        min_value (int): Minimum value for generated random numbers (inclusive).
        max_value (int): Maximum value for generated random numbers (inclusive).
        seed_number (int): The integer seed derived from hashing the input string.
    
    Example:
        >>> gen = SeedHashGenerator("experiment_1")
        >>> gen.set_seed()  # Seeds PyTorch by default
        >>> seeds = gen.generate_seeds(5)
    """
    
    DEFAULT_MIN = 0
    DEFAULT_MAX = 2**31 - 1
    
    def __init__(
        self, 
        input_string: str,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None
    ):
        """Initialize the SeedHashGenerator.
        
        Args:
            input_string: The string to hash for seed generation.
            min_value: Minimum value for random number range (default: 0).
            max_value: Maximum value for random number range (default: 2^31 - 1).
            
        Raises:
            ValueError: If input_string is empty or if min_value >= max_value.
            TypeError: If input_string is not a string.
        """
        if not isinstance(input_string, str):
            raise TypeError("input_string must be a string")
        
        if not input_string:
            raise ValueError("input_string cannot be empty")
        
        self.input_string = input_string
        self.min_value = min_value if min_value is not None else self.DEFAULT_MIN
        self.max_value = max_value if max_value is not None else self.DEFAULT_MAX
        
        # Validate range
        if not isinstance(self.min_value, int):
            raise TypeError("min_value must be an integer")
        if not isinstance(self.max_value, int):
            raise TypeError("max_value must be an integer")
        if self.min_value >= self.max_value:
            raise ValueError(
                f"min_value ({self.min_value}) must be less than "
                f"max_value ({self.max_value})"
            )
        
        # Generate the seed from the input string
        self.seed_number = self._generate_seed()
        
    def _generate_seed(self) -> int:
        """Generate an integer seed from the input string using MD5 hashing.
        
        Returns:
            An integer representation of the MD5 hash (modulo 2^32 for compatibility).
        """
        md5_hasher = hashlib.md5()
        md5_hasher.update(self.input_string.encode('utf-8'))
        hashed_value = md5_hasher.hexdigest()
        # Use modulo 2^32 to ensure compatibility with all frameworks
        return int(hashed_value, 16) % (2**32)
    
    def set_seed(
        self, 
        framework: FrameworkType = "torch",
        deterministic: bool = True
    ) -> dict:
        """Set random seeds for specified deep learning framework(s).
        
        Args:
            framework: Which framework to seed. Options:
                - "torch": Seed PyTorch (default)
                - "tensorflow": Seed TensorFlow
                - "numpy": Seed NumPy
                - "all": Seed all available frameworks
                - "python": Seed only Python's random module
            deterministic: If True, enable deterministic algorithms (PyTorch only).
                For PyTorch, sets torch.use_deterministic_algorithms(True) and
                CUBLAS environment variables for reproducibility.
        
        Returns:
            A dictionary with the status of seeding for each framework.
        
        Raises:
            ImportError: If the specified framework is not installed.
            ValueError: If an invalid framework name is provided.
        
        Example:
            >>> gen = SeedHashGenerator("experiment_1")
            >>> gen.set_seed("torch")  # Seed PyTorch
            >>> gen.set_seed("all")    # Seed all available frameworks
        """
        valid_frameworks = ["torch", "tensorflow", "numpy", "all", "python"]
        if framework not in valid_frameworks:
            raise ValueError(
                f"Invalid framework '{framework}'. "
                f"Must be one of: {valid_frameworks}"
            )
        
        status = {}
        frameworks_to_seed = []
        
        # Determine which frameworks to seed
        if framework == "all":
            frameworks_to_seed = ["python", "numpy", "torch", "tensorflow"]
        elif framework == "python":
            frameworks_to_seed = ["python"]
        else:
            frameworks_to_seed = ["python", framework]
        
        # Seed Python's random module (always)
        if "python" in frameworks_to_seed:
            random.seed(self.seed_number)
            status["python"] = "seeded"
        
        # Seed NumPy
        if "numpy" in frameworks_to_seed:
            if NUMPY_AVAILABLE:
                np.random.seed(self.seed_number)
                status["numpy"] = "seeded"
            elif framework == "numpy":
                raise ImportError(
                    "NumPy is not installed. Install it with: pip install numpy"
                )
            else:
                status["numpy"] = "not_available"
        
        # Seed PyTorch
        if "torch" in frameworks_to_seed:
            if TORCH_AVAILABLE:
                torch.manual_seed(self.seed_number)
                
                # Seed CUDA if available
                if torch.cuda.is_available():
                    torch.cuda.manual_seed(self.seed_number)
                    torch.cuda.manual_seed_all(self.seed_number)
                
                # Enable deterministic mode if requested
                if deterministic:
                    # Set deterministic algorithms
                    torch.use_deterministic_algorithms(True, warn_only=True)
                    
                    # Set CUDNN to deterministic mode
                    torch.backends.cudnn.deterministic = True
                    torch.backends.cudnn.benchmark = False
                    
                    # Set environment variables for CUBLAS
                    os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'
                
                status["torch"] = "seeded" + ("_deterministic" if deterministic else "")
            elif framework == "torch":
                raise ImportError(
                    "PyTorch is not installed. Install it with: pip install torch"
                )
            else:
                status["torch"] = "not_available"
        
        # Seed TensorFlow
        if "tensorflow" in frameworks_to_seed:
            if TF_AVAILABLE:
                tf.random.set_seed(self.seed_number)
                
                # Set deterministic operations if requested
                if deterministic:
                    os.environ['TF_DETERMINISTIC_OPS'] = '1'
                    os.environ['TF_CUDNN_DETERMINISTIC'] = '1'
                
                status["tensorflow"] = "seeded" + ("_deterministic" if deterministic else "")
            elif framework == "tensorflow":
                raise ImportError(
                    "TensorFlow is not installed. Install it with: pip install tensorflow"
                )
            else:
                status["tensorflow"] = "not_available"
        
        return status
    
    def seed_all(self, deterministic: bool = True) -> dict:
        """Convenience method to seed all available frameworks.
        
        Args:
            deterministic: If True, enable deterministic algorithms where applicable.
        
        Returns:
            A dictionary with the status of seeding for each framework.
        
        Example:
            >>> gen = SeedHashGenerator("experiment_1")
            >>> status = gen.seed_all()
            >>> print(status)
        """
        return self.set_seed("all", deterministic=deterministic)
    
    def generate_seeds(self, count: int) -> List[int]:
        """Generate a list of random seed numbers.
        
        Args:
            count: The number of random seeds to generate.
            
        Returns:
            A list of random integers within the specified range.
            
        Raises:
            ValueError: If count is not a positive integer.
            TypeError: If count is not an integer.
        """
        if not isinstance(count, int):
            raise TypeError("count must be an integer")
        
        if count <= 0:
            raise ValueError("count must be a positive integer")
        
        # Set the random seed
        random.seed(self.seed_number)
        
        # Generate random numbers
        random_numbers = [
            random.randint(self.min_value, self.max_value) 
            for _ in range(count)
        ]
        
        return random_numbers
    
    def get_hash(self) -> str:
        """Get the MD5 hash of the input string.
        
        Returns:
            The MD5 hash as a hexadecimal string.
        """
        md5_hasher = hashlib.md5()
        md5_hasher.update(self.input_string.encode('utf-8'))
        return md5_hasher.hexdigest()
    
    def __repr__(self) -> str:
        """Return a string representation of the generator."""
        return (
            f"SeedHashGenerator(input_string='{self.input_string}', "
            f"min_value={self.min_value}, max_value={self.max_value}, "
            f"seed_number={self.seed_number})"
        )
