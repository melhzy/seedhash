# seedhash - Python Package

This directory contains the Python implementation of the seedhash library.

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
│   └── README.md
├── dist/                   # Built distributions
├── seedhash.egg-info/      # Package metadata
├── setup.py                # Package configuration
├── pyproject.toml          # Modern Python packaging
└── requirements.txt        # Dependencies (none for base package)
```

## Installation

### From Local Directory
```bash
cd Python
pip install .
```

### From GitHub
```bash
pip install git+https://github.com/melhzy/seedhash.git#subdirectory=Python
```

### Development Mode
```bash
cd Python
pip install -e .
```

## Quick Start

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

## Features

- **Unlimited integer range** (Python's arbitrary precision integers)
- **Reproducible** seeds based on string input
- **No external dependencies** (uses only Python stdlib)
- **Fast** MD5-based hashing
- **Simple API** with clear error messages

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
**Python**: >=3.6
