# SeedHash

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**SeedHash** is a Python library for generating deterministic random seeds from string inputs using MD5 hashing. It's perfect for creating reproducible experiments, simulations, and any scenario where you need consistent random number generation across different runs.

## Features

- 🎯 **Deterministic**: Same input string always produces the same sequence of random numbers
- 🔧 **Configurable**: Customize the range of generated random numbers
- ✅ **Type-Safe**: Comprehensive error handling and input validation
- 📦 **Lightweight**: No external dependencies beyond Python standard library
- 🚀 **Easy to Use**: Simple, intuitive API

## Installation

### From GitHub (Development)

```bash
pip install git+https://github.com/melhzy/seedhash.git
```

### Local Installation

```bash
git clone https://github.com/melhzy/seedhash.git
cd seedhash
pip install -e .
```

### Future PyPI Installation

```bash
# Once published to PyPI
pip install seedhash
```

## Quick Start

```python
from seedhash import SeedHashGenerator

# Create a generator with an input string
generator = SeedHashGenerator("my_experiment_name")

# Generate 10 random seeds
seeds = generator.generate_seeds(10)
print(seeds)
```

## Usage Examples

### Basic Usage

```python
from seedhash import SeedHashGenerator

# Initialize with a string
gen = SeedHashGenerator("Shalini")

# Generate 10 random seeds (default range: 0 to 2^31-1)
random_seeds = gen.generate_seeds(10)
print(f"Generated seeds: {random_seeds}")

# Get the underlying hash
print(f"MD5 Hash: {gen.get_hash()}")
print(f"Seed number: {gen.seed_number}")
```

### Custom Range

```python
from seedhash import SeedHashGenerator

# Custom range for random numbers
gen = SeedHashGenerator(
    input_string="experiment_42",
    min_value=100,
    max_value=1000
)

# Generate 5 seeds in the range [100, 1000]
seeds = gen.generate_seeds(5)
print(f"Seeds in range [100, 1000]: {seeds}")
```

### Error Handling

```python
from seedhash import SeedHashGenerator

# The library includes comprehensive error checking
try:
    # Empty string raises ValueError
    gen = SeedHashGenerator("")
except ValueError as e:
    print(f"Error: {e}")

try:
    # Invalid range raises ValueError
    gen = SeedHashGenerator("test", min_value=100, max_value=50)
except ValueError as e:
    print(f"Error: {e}")

try:
    # Non-positive count raises ValueError
    gen = SeedHashGenerator("test")
    seeds = gen.generate_seeds(0)
except ValueError as e:
    print(f"Error: {e}")
```

### Reproducibility Demo

```python
from seedhash import SeedHashGenerator

# Same input always produces same output
gen1 = SeedHashGenerator("experiment_1")
seeds1 = gen1.generate_seeds(5)

gen2 = SeedHashGenerator("experiment_1")
seeds2 = gen2.generate_seeds(5)

assert seeds1 == seeds2  # Always True!
print(f"Reproducible: {seeds1} == {seeds2}")
```

## API Reference

### `SeedHashGenerator`

#### Constructor

```python
SeedHashGenerator(input_string, min_value=None, max_value=None)
```

**Parameters:**
- `input_string` (str): The string to hash for seed generation
- `min_value` (int, optional): Minimum value for random number range. Default: 0
- `max_value` (int, optional): Maximum value for random number range. Default: 2^31 - 1

**Raises:**
- `TypeError`: If `input_string` is not a string or range values are not integers
- `ValueError`: If `input_string` is empty or `min_value >= max_value`

#### Methods

##### `generate_seeds(count)`

Generate a list of random seed numbers.

**Parameters:**
- `count` (int): The number of random seeds to generate

**Returns:**
- `List[int]`: A list of random integers within the specified range

**Raises:**
- `TypeError`: If count is not an integer
- `ValueError`: If count is not positive

##### `get_hash()`

Get the MD5 hash of the input string.

**Returns:**
- `str`: The MD5 hash as a hexadecimal string

#### Attributes

- `input_string` (str): The input string used for seed generation
- `min_value` (int): Minimum value for random numbers
- `max_value` (int): Maximum value for random numbers
- `seed_number` (int): The integer seed derived from the input string

## Use Cases

### Machine Learning Experiments

```python
from seedhash import SeedHashGenerator

# Reproducible train/test splits
experiment_name = "model_v1_baseline"
gen = SeedHashGenerator(experiment_name)
seeds = gen.generate_seeds(5)  # For different folds

for i, seed in enumerate(seeds):
    print(f"Fold {i+1} seed: {seed}")
    # Use seed for train_test_split, model initialization, etc.
```

### Monte Carlo Simulations

```python
from seedhash import SeedHashGenerator

# Reproducible simulation runs
simulation_id = "monte_carlo_sim_2025"
gen = SeedHashGenerator(simulation_id, min_value=1, max_value=10000)

# Generate seeds for parallel simulation runs
num_simulations = 100
simulation_seeds = gen.generate_seeds(num_simulations)
```

### Data Sampling

```python
from seedhash import SeedHashGenerator
import random

# Reproducible data sampling
dataset_version = "dataset_v2.1"
gen = SeedHashGenerator(dataset_version)
sample_seed = gen.generate_seeds(1)[0]

random.seed(sample_seed)
# Use random module for sampling with reproducibility
```

## Project Structure

```
seedhash/
├── seedhash/
│   ├── __init__.py       # Package initialization
│   └── core.py           # Core SeedHashGenerator class
├── examples/
│   └── demo.py           # Usage examples
├── base.py               # Original implementation
├── setup.py              # Setup configuration
├── pyproject.toml        # Modern Python packaging
├── requirements.txt      # Dependencies
├── README.md             # This file
└── LICENSE               # MIT License
```

## Development

### Running Tests

```bash
# Install in development mode
pip install -e .

# Run the example script
python examples/demo.py
```

### Building the Package

```bash
# Install build tools
pip install build

# Build the package
python -m build

# This creates dist/seedhash-0.1.0.tar.gz and dist/seedhash-0.1.0-whl
```

### Publishing to PyPI

```bash
# Install twine
pip install twine

# Upload to PyPI
twine upload dist/*
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**melhzy**
- GitHub: [@melhzy](https://github.com/melhzy)

## Changelog

### v0.1.0 (2025-10-29)
- Initial release
- Core `SeedHashGenerator` class
- MD5-based seed generation
- Configurable random number ranges
- Comprehensive error handling
- Full documentation and examples

## Acknowledgments

- Inspired by the need for reproducible random number generation in scientific computing
- Built with Python's standard library for maximum compatibility

---

**Note**: This library uses MD5 hashing for seed generation. MD5 is suitable for non-cryptographic purposes like seed generation. Do not use this library for cryptographic or security-sensitive applications.
