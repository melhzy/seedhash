"""Core module for seed generation using hash-based initialization."""

import random
import hashlib
from typing import List, Optional


class SeedHashGenerator:
    """Generate deterministic random seeds from string input using MD5 hashing.
    
    This class allows users to generate reproducible sequences of random numbers
    by hashing an input string and using it as a seed for Python's random module.
    
    Attributes:
        input_string (str): The string used to generate the initial seed.
        min_value (int): Minimum value for generated random numbers (inclusive).
        max_value (int): Maximum value for generated random numbers (inclusive).
        seed_number (int): The integer seed derived from hashing the input string.
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
            An integer representation of the MD5 hash.
        """
        md5_hasher = hashlib.md5()
        md5_hasher.update(self.input_string.encode('utf-8'))
        hashed_value = md5_hasher.hexdigest()
        return int(hashed_value, 16)
    
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
