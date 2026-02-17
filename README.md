# SeedHash: Deterministic Random Seed Generation from String Inputs

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![R Version](https://img.shields.io/badge/R-3.5+-blue.svg)](https://www.r-project.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/melhzy/seedhash/workflows/Tests/badge.svg)](https://github.com/melhzy/seedhash/actions)

**SeedHash** is a library for generating deterministic random seeds from string inputs using MD5 hashing. Available in both **Python** and **R**, it's perfect for creating reproducible experiments, simulations, and any scenario where you need consistent random number generation across different runs.

## 📁 Repository Structure

```
seedhash/
├── Python/              # Python implementation
│   ├── seedhash/        # Python package
│   ├── examples/        # Python examples
│   └── README.md        # Python documentation
│
├── R/                   # R implementation  
│   ├── R/               # R package source
│   ├── tests/           # R tests
│   ├── examples/        # R examples
│   └── README.md        # R documentation
│
├── PYTHON_TO_R_GUIDE.md # Conversion guide for developers
└── README.md            # This file
```

## Features

- 🎯 **Deterministic**: Same input string always produces the same sequence of random numbers
- 🔧 **Configurable**: Customize the range of generated random numbers
- ✅ **Type-Safe**: Comprehensive error handling and input validation
- 📦 **Lightweight**: Minimal dependencies (Python: none, R: R6 + digest)
- 🚀 **Easy to Use**: Simple, intuitive API
- 🔄 **Cross-Language**: Available in both Python and R
- 🎲 **4 Sampling Methods**: Simple, Stratified, Cluster, and Systematic random sampling
- 🧪 **ML Integration**: Experiment tracking with hierarchical seed management

## Installation

### Python

```bash
# From GitHub
pip install git+https://github.com/melhzy/seedhash.git#subdirectory=Python

# From local directory
cd Python
pip install .
```

See [Python/README.md](Python/README.md) for detailed instructions.

### R

```r
# Recommended: Using pak
install.packages("pak", repos = "https://r-lib.github.io/p/pak/stable/")
pak::pkg_install("github::melhzy/seedhash/R")

# Alternative: Using devtools
devtools::install_github("melhzy/seedhash", subdir = "R")
```

See [R/INSTALL.md](R/INSTALL.md) for detailed instructions.

## Quick Start

### Python

```python
from seedhash import SeedHashGenerator

# Create a generator with an input string
generator = SeedHashGenerator("my_experiment_name")

# Generate 10 random seeds
seeds = generator.generate_seeds(10)
print(seeds)

# Get the MD5 hash
print(generator.get_hash())
```

### R

```r
library(seedhash)

# Create a generator
generator <- SeedHashGenerator$new("my_experiment_name")

# Generate 10 random seeds
seeds <- generator$generate_seeds(10)
print(seeds)

# Get the MD5 hash
cat(generator$get_hash(), "\n")
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
```

## Advanced Features

### 🎲 4 Random Sampling Techniques

SeedHash includes 4 scientifically-backed sampling methods for systematic seed generation:

```python
from seedhash import SeedSampler

sampler = SeedSampler(master_seed=42)

# 1. Simple Random Sampling - Pure randomness
simple = sampler.simple_random_sampling(n_samples=10, seed_range=(0, 1000))

# 2. Stratified Random Sampling - Balanced coverage
stratified = sampler.stratified_random_sampling(
    n_samples=25, seed_range=(0, 1000), n_strata=5
)

# 3. Cluster Random Sampling - Grouped seeds
cluster = sampler.cluster_random_sampling(
    n_samples=20, seed_range=(0, 1000), n_clusters=4
)

# 4. Systematic Random Sampling - Even intervals
systematic = sampler.systematic_random_sampling(n_samples=15, seed_range=(0, 1000))
```

📖 **[Full Sampling Methods Documentation →](SAMPLING_METHODS.md)**

### 🧪 Hierarchical Seed Management & Experiment Tracking

```python
from seedhash import SeedExperimentManager
import numpy as np

# Create experiment manager
manager = SeedExperimentManager("my_ml_project")

# Generate hierarchical seeds: master → seeds → sub-seeds
hierarchy = manager.generate_seed_hierarchy(
    n_seeds=10,
    n_sub_seeds=5,
    max_depth=2,
    sampling_method="stratified"  # Use any of the 4 methods
)

# Track experiments
for seed in hierarchy[1]:
    # Run your experiment
    np.random.seed(seed)
    accuracy = 0.8 + np.random.rand() * 0.15
    
    # Record results
    manager.add_experiment_result(
        seed=seed,
        ml_task="classification",
        metrics={"accuracy": accuracy, "f1_score": 0.85},
        sampling_method="stratified"
    )

# Export to DataFrame
df = manager.get_results_dataframe()
df.to_csv('experiment_results.csv')
```

📖 **[Full Documentation](Python/README.md)** | 📓 **[Jupyter Tutorials](jupyter/README.md)**
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

We welcome contributions from the community! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- Reporting bugs and suggesting enhancements
- Development setup for Python and R
- Coding standards and testing requirements
- Pull request process

Please also read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

### Quick Start for Contributors

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following our coding standards
4. Add tests for new functionality
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add some amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

For questions, please open an issue on GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Ziyuan Huang**
- ORCID: [0000-0002-2215-2473](https://orcid.org/0000-0002-2215-2473)
- Affiliation: University of Massachusetts Chan Medical School
- GitHub: [@melhzy](https://github.com/melhzy)

## Citation

If you use SeedHash in your research or project, please consider citing it:

### BibTeX

```bibtex
@software{seedhash2025,
  author = {Ziyuan Huang},
  title = {SeedHash: Deterministic Random Seed Generation from String Inputs},
  year = {2025},
  url = {https://github.com/melhzy/seedhash},
  note = {Python and R implementation}
}
```

### APA Style

```
Huang, Z. (2025). SeedHash: Deterministic Random Seed Generation from String Inputs 
(Version 0.1.0) [Computer software]. https://github.com/melhzy/seedhash
```

### Chicago Style

```
Huang, Ziyuan. 2025. "SeedHash: Deterministic Random Seed Generation from String Inputs." 
Computer software. Version 0.1.0. https://github.com/melhzy/seedhash.
```

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

## Reference

- Rivest, R. (1992). The MD5 Message-Digest Algorithm (RFC 1321). MIT Laboratory for Computer Science and RSA Data Security, Inc. https://datatracker.ietf.org/doc/html/rfc1321
- Python Software Foundation. (2024). random — Generate pseudo-random numbers. In Python Standard Library (Python 3.x documentation). https://docs.python.org/3/library/random.html
---

**Note**: This library uses MD5 hashing for seed generation. MD5 is suitable for non-cryptographic purposes like seed generation. Do not use this library for cryptographic or security-sensitive applications.
