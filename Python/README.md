# seedhash - Python Package

This directory contains the Python implementation of the seedhash library with support for popular deep learning frameworks.

## Structure

```
Python/
├── base.py                  # Original standalone script
├── seedhash/               # Python package
│   ├── __init__.py         # Package exports
│   └── core.py             # SeedHashGenerator class
├── examples/               # Usage examples
│   ├── basic_usage.py
│   ├── advanced_usage.py
│   ├── deep_learning_seeding.py  # NEW: Deep learning examples
│   └── README.md
├── dist/                   # Built distributions
├── seedhash.egg-info/      # Package metadata
├── setup.py                # Package configuration
├── pyproject.toml          # Modern Python packaging
└── requirements.txt        # Dependencies
```

## Installation

### Basic Installation (No ML frameworks)
```bash
pip install git+https://github.com/melhzy/seedhash.git#subdirectory=Python
```

### With PyTorch Support (Recommended for ML)
```bash
pip install "git+https://github.com/melhzy/seedhash.git#subdirectory=Python[torch]"
```

### With TensorFlow Support
```bash
pip install "git+https://github.com/melhzy/seedhash.git#subdirectory=Python[tensorflow]"
```

### With All Frameworks (PyTorch, TensorFlow, NumPy)
```bash
pip install "git+https://github.com/melhzy/seedhash.git#subdirectory=Python[all]"
```

### Local Installation
```bash
cd Python
pip install .               # Basic
pip install .[torch]        # With PyTorch
pip install .[all]          # With all frameworks
```

## Quick Start

### Basic Usage
```python
from seedhash import SeedHashGenerator

# Create a generator
gen = SeedHashGenerator("my_experiment")

# Generate 5 random seeds
seeds = gen.generate_seeds(5)
print(seeds)

# Get the MD5 hash
print(gen.get_hash())
```

### Deep Learning Framework Seeding 🆕

#### PyTorch (Default)
```python
from seedhash import SeedHashGenerator
import torch

# Create generator and seed PyTorch
gen = SeedHashGenerator("pytorch_experiment")
gen.set_seed()  # Seeds PyTorch by default

# Or explicitly:
gen.set_seed("torch")

# Enable deterministic mode for maximum reproducibility
gen.set_seed("torch", deterministic=True)

# Now all PyTorch operations are reproducible
model = torch.nn.Linear(10, 5)
data = torch.randn(32, 10)
```

#### TensorFlow
```python
from seedhash import SeedHashGenerator
import tensorflow as tf

gen = SeedHashGenerator("tensorflow_experiment")
gen.set_seed("tensorflow")

# Now TensorFlow is seeded
model = tf.keras.Sequential([...])
```

#### NumPy
```python
from seedhash import SeedHashGenerator
import numpy as np

gen = SeedHashGenerator("numpy_experiment")
gen.set_seed("numpy")

# NumPy operations are now reproducible
data = np.random.randn(100, 10)
```

#### Seed All Frameworks
```python
gen = SeedHashGenerator("multi_framework_experiment")

# Seed all available frameworks at once
status = gen.seed_all(deterministic=True)
print(status)  # Shows which frameworks were seeded

# Convenience method (same as seed_all)
status = gen.set_seed("all", deterministic=True)
```

## Features

- **Unlimited integer range** (Python's arbitrary precision integers)
- **Reproducible** seeds based on string input
- **No required dependencies** (uses only Python stdlib)
- **Deep Learning Support** 🆕:
  - PyTorch seeding (CPU and CUDA)
  - TensorFlow seeding
  - NumPy seeding
  - Deterministic mode for maximum reproducibility
  - Seed all frameworks with one command
- **Fast** MD5-based hashing
- **Simple API** with clear error messages

## Supported Frameworks

| Framework | Status | Notes |
|-----------|--------|-------|
| Python random | ✅ Always | Built-in, no extra dependencies |
| PyTorch | ✅ Optional | Install with `pip install torch` |
| TensorFlow | ✅ Optional | Install with `pip install tensorflow` |
| NumPy | ✅ Optional | Install with `pip install numpy` |

## API Reference

### `set_seed(framework="torch", deterministic=True)`

Seed the specified framework(s).

**Parameters:**
- `framework` (str): Which framework to seed:
  - `"torch"` - PyTorch (default)
  - `"tensorflow"` - TensorFlow
  - `"numpy"` - NumPy
  - `"python"` - Python's random module only
  - `"all"` - All available frameworks
- `deterministic` (bool): Enable deterministic algorithms (default: True)

**Returns:** Dictionary with seeding status for each framework

**Examples:**
```python
gen.set_seed()                              # PyTorch (default)
gen.set_seed("tensorflow")                  # TensorFlow
gen.set_seed("all")                         # All frameworks
gen.set_seed("torch", deterministic=False)  # PyTorch, non-deterministic
```

### `seed_all(deterministic=True)`

Convenience method to seed all available frameworks.

**Parameters:**
- `deterministic` (bool): Enable deterministic algorithms (default: True)

**Returns:** Dictionary with seeding status

**Example:**
```python
status = gen.seed_all()
# Returns: {'python': 'seeded', 'torch': 'seeded_deterministic', ...}
```

## Examples

See [examples/deep_learning_seeding.py](examples/deep_learning_seeding.py) for comprehensive examples including:
- PyTorch training setup
- TensorFlow model seeding
- NumPy reproducibility
- Multi-framework experiments
- Deterministic mode usage

Run examples:
```bash
cd Python
python examples/deep_learning_seeding.py
```

## Deterministic Mode

When `deterministic=True` (default), seedhash configures frameworks for maximum reproducibility:

**PyTorch:**
- Sets `torch.use_deterministic_algorithms(True)`
- Sets `torch.backends.cudnn.deterministic = True`
- Sets `torch.backends.cudnn.benchmark = False`
- Sets `CUBLAS_WORKSPACE_CONFIG` environment variable

**TensorFlow:**
- Sets `TF_DETERMINISTIC_OPS=1`
- Sets `TF_CUDNN_DETERMINISTIC=1`

**Note:** Deterministic mode may reduce performance but ensures reproducibility.

## Testing

```bash
cd Python
pytest tests/
```

## Building

```bash
cd Python
python setup.py sdist bdist_wheel
```

## Documentation

See the main repository [README.md](../README.md) for complete documentation.

For converting Python features to R, see [PYTHON_TO_R_GUIDE.md](../PYTHON_TO_R_GUIDE.md).

---

**Version**: 0.1.0  
**License**: MIT  
**Python**: >=3.7
