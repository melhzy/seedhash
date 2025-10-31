# 🎯 Quick Start: Install seedhash from GitHub

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://github.com/melhzy/seedhash/tree/main/Python)
[![R](https://img.shields.io/badge/R-3.5+-blue.svg)](https://github.com/melhzy/seedhash/tree/main/R)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**seedhash** is available in both **Python** and **R**. Choose your language below for installation instructions.

GitHub Repository: **https://github.com/melhzy/seedhash**

---

## 🐍 Python Installation

### Quick Install

```bash
# Install from GitHub
pip install git+https://github.com/melhzy/seedhash.git#subdirectory=Python
```

### Verify Installation

```python
from seedhash import SeedHashGenerator

# Test it
gen = SeedHashGenerator("experiment_1")
seeds = gen.generate_seeds(5)
print(seeds)
```

### Usage Examples

```python
# Example 1: Default range (unlimited in Python!)
gen1 = SeedHashGenerator("my_experiment")
seeds1 = gen1.generate_seeds(5)

# Example 2: Custom range (any size works)
gen2 = SeedHashGenerator("test", min_value=-10**9, max_value=10**9)
seeds2 = gen2.generate_seeds(10)

# Example 3: Get MD5 hash
hash_value = gen1.get_hash()
print(hash_value)

# Example 4: Reproducibility
gen_a = SeedHashGenerator("same_name")
gen_b = SeedHashGenerator("same_name")
assert gen_a.generate_seeds(5) == gen_b.generate_seeds(5)  # Always True!
```

### Alternative: Local Installation

```bash
# Clone repository
git clone https://github.com/melhzy/seedhash.git
cd seedhash/Python

# Install
pip install .

# Or install in development mode
pip install -e .
```

### 📚 Python Documentation

See [Python/README.md](https://github.com/melhzy/seedhash/tree/main/Python) for complete documentation.

---

## 📊 R Installation

### ✅ Recommended: Using pak

```r
# Install pak package manager
install.packages("pak", repos = "https://r-lib.github.io/p/pak/stable/")

# Install seedhash from GitHub
pak::pkg_install("github::melhzy/seedhash/R")

# Load and test
library(seedhash)
gen <- SeedHashGenerator$new("experiment_1")
seeds <- gen$generate_seeds(5)
print(seeds)
```

### Verify Installation

```r
library(seedhash)

# Create generator
gen <- SeedHashGenerator$new("test")

# Generate seeds
seeds <- gen$generate_seeds(5)
print(seeds)

# View details
print(gen)
```

### Usage Examples

```r
# Example 1: Default range (-1 billion to 1 billion)
gen1 <- SeedHashGenerator$new("C57BL/6 experiment 1")
seeds1 <- gen1$generate_seeds(5)

# Example 2: Custom range
gen2 <- SeedHashGenerator$new("my_experiment", min_value = 0, max_value = 10000)
seeds2 <- gen2$generate_seeds(10)

# Example 3: Get MD5 hash
hash <- gen1$get_hash()
cat("Hash:", hash, "\n")

# Example 4: Reproducibility
gen_a <- SeedHashGenerator$new("same_name")
gen_b <- SeedHashGenerator$new("same_name")
identical(gen_a$generate_seeds(5), gen_b$generate_seeds(5))  # TRUE
```

### Alternative: Using devtools

```r
# Install devtools
install.packages("devtools")

# Install seedhash
devtools::install_github("melhzy/seedhash", subdir = "R")

library(seedhash)
```

### Alternative: Local Installation

```r
# Install from local directory
devtools::install("path/to/seedhash/R")

library(seedhash)
```

### 🔧 Why pak instead of devtools?

- ✅ Better GitHub authentication handling (no PAT issues)
- ✅ No SSL certificate issues on Windows
- ✅ Faster and more reliable downloads
- ✅ Modern dependency resolution
- ✅ Works perfectly with subdirectory installations

### ⚠️ Important: R Integer Limitations

R uses 32-bit signed integers with these limits:
- **Minimum**: `-2,147,483,648`
- **Maximum**: `2,147,483,647`
- **Recommended range**: `-1e9` to `1e9` (default)

```r
# ✅ This works
gen <- SeedHashGenerator$new("test", -1e9, 1e9)

# ❌ This fails (values too large)
gen <- SeedHashGenerator$new("test", -10^33, 10^33)
```

See [R/INTEGER_RANGE_SOLUTION.md](https://github.com/melhzy/seedhash/tree/main/R/INTEGER_RANGE_SOLUTION.md) for details.

### 📚 R Documentation

See [R/INSTALL.md](https://github.com/melhzy/seedhash/tree/main/R/INSTALL.md) for complete installation methods and troubleshooting.

---

## 🔄 Python vs R Comparison

| Feature | Python | R |
|---------|--------|---|
| **Integer Range** | Unlimited ✅ | ±2.1 billion ⚠️ |
| **Default Range** | -10^9 to 10^9 | -1e9 to 1e9 |
| **Dependencies** | None (stdlib only) | R6, digest |
| **Installation** | pip | pak (recommended) |
| **Class System** | Native classes | R6 classes |
| **Syntax** | `gen.method()` | `gen$method()` |

For developers converting between languages, see [PYTHON_TO_R_GUIDE.md](https://github.com/melhzy/seedhash/tree/main/PYTHON_TO_R_GUIDE.md).

---

## 🚀 Quick Comparison Test

### Python
```python
from seedhash import SeedHashGenerator
gen = SeedHashGenerator("test")
print(gen.generate_seeds(5))
```

### R
```r
library(seedhash)
gen <- SeedHashGenerator$new("test")
print(gen$generate_seeds(5))
```

**Note**: Seeds will be different between Python and R due to different random number generators, but each is reproducible within its own language.

---

## 📖 Additional Resources

- **Main Documentation**: [README.md](https://github.com/melhzy/seedhash)
- **Python Package**: [Python/README.md](https://github.com/melhzy/seedhash/tree/main/Python)
- **R Package**: [R/README.md](https://github.com/melhzy/seedhash/tree/main/R)
- **Python to R Guide**: [PYTHON_TO_R_GUIDE.md](https://github.com/melhzy/seedhash/tree/main/PYTHON_TO_R_GUIDE.md)
- **R Integer Issues**: [R/INTEGER_RANGE_SOLUTION.md](https://github.com/melhzy/seedhash/tree/main/R/INTEGER_RANGE_SOLUTION.md)

---

## ❓ Troubleshooting

### Python: "No module named 'seedhash'"
```bash
# Make sure you installed from the Python subdirectory
pip install git+https://github.com/melhzy/seedhash.git#subdirectory=Python
```

### R: "cannot open URL" with devtools
```r
# Use pak instead (recommended)
pak::pkg_install("github::melhzy/seedhash/R")
```

### R: "Range is too large"
```r
# Use smaller range (within ±2.1 billion)
gen <- SeedHashGenerator$new("test", -1e9, 1e9)
```

### R: Package installation corrupted
```r
# Remove and reinstall
remove.packages("seedhash")
pak::pkg_install("github::melhzy/seedhash/R")
```

---

**Status**: ✅ Both Python and R implementations working and tested  
**Last Updated**: October 31, 2025  
**License**: MIT  
**Maintainer**: melhzy
