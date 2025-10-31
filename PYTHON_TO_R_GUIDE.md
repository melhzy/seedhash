# Python to R Conversion Guide for seedhash
# ============================================
# Reference document for converting Python seedhash features to R
# Last Updated: October 31, 2025

## Table of Contents
1. [Language Differences Overview](#language-differences)
2. [Data Types & Limitations](#data-types)
3. [Class Structure Conversion](#class-structure)
4. [Common Operations Mapping](#operations)
5. [Testing & Validation](#testing)
6. [Packaging & Distribution](#packaging)
7. [Lessons Learned](#lessons-learned)

---

## 1. Language Differences Overview

### Python Advantages
- Unlimited integer precision (handles any size number)
- Simpler class syntax with `__init__`
- Native support for `__str__` and `__repr__`
- More flexible with dynamic typing
- pip ecosystem is straightforward

### R Advantages  
- Better statistical computing integration
- Built-in vectorization
- CRAN provides quality control
- Easier integration with scientific workflows
- R6 provides good OOP support

---

## 2. Data Types & Limitations

### Integer Handling

**Python:**
```python
# Unlimited precision - any integer size works
hash_int = int(hash_hex[:8], 16)  # Can be any size
min_value = -10**33  # Works fine
max_value = 10**33   # Works fine
range_size = max_value - min_value  # No problem
```

**R - CRITICAL LIMITATIONS:**
```r
# 32-bit signed integer limit: -2,147,483,648 to 2,147,483,647
hash_int <- strtoi(substr(hash_hex, 1, 7), base = 16)  # Use 7 chars, not 8!
min_value <- -1e9    # Safe: -1,000,000,000
max_value <- 1e9     # Safe:  1,000,000,000
range_size <- max_value - min_value + 1  # Must be <= 2,147,483,647
```

**Key Conversion Rules:**
1. **Hex to Integer**: Use max 7 hex characters (28 bits) in R, not 8
2. **Default Ranges**: Use -1e9 to 1e9 in R (not 0 to 2^31-1)
3. **Range Validation**: Check BOTH values AND total range span
4. **Coercion**: Always validate BEFORE `as.integer()` conversion

### String Handling

**Python:**
```python
# Simple string operations
input_string = "My Experiment"
hash_value = hashlib.md5(input_string.encode()).hexdigest()
```

**R:**
```r
# Need digest package
hash_value <- digest::digest(input_string, algo = "md5", serialize = FALSE)
# Note: serialize = FALSE is important for consistency
```

### Random Number Generation

**Python:**
```python
random.seed(seed_number)
seeds = [random.randint(min_value, max_value) for _ in range(count)]
```

**R:**
```r
set.seed(seed_number)
range_size <- as.numeric(max_value) - as.numeric(min_value) + 1

# CRITICAL: Validate range_size
if (range_size > .Machine$integer.max) {
  stop("Range is too large. Maximum range size is ", .Machine$integer.max)
}

random_numbers <- sample.int(
  n = as.integer(range_size),
  size = count,
  replace = TRUE
) + min_value - 1
```

---

## 3. Class Structure Conversion

### Python Class Structure

**Python (seedhash/core.py):**
```python
class SeedHashGenerator:
    """Generate reproducible random seeds from string inputs."""
    
    def __init__(self, input_string, min_value=-(10**9), max_value=10**9):
        """Initialize the generator."""
        self.input_string = input_string
        self.min_value = min_value
        self.max_value = max_value
        self._seed_number = self._generate_seed()
    
    def _generate_seed(self):
        """Private method to generate seed."""
        hash_value = hashlib.md5(self.input_string.encode()).hexdigest()
        return int(hash_value[:8], 16)
    
    def generate_seeds(self, count):
        """Generate random seeds."""
        random.seed(self._seed_number)
        return [random.randint(self.min_value, self.max_value) 
                for _ in range(count)]
    
    def get_hash(self):
        """Get MD5 hash."""
        return hashlib.md5(self.input_string.encode()).hexdigest()
    
    def __str__(self):
        """String representation."""
        return f"SeedHashGenerator('{self.input_string}')"
```

### R Class Structure (R6)

**R (R/seedhash.R):**
```r
#' @export
SeedHashGenerator <- R6::R6Class(
  "SeedHashGenerator",
  
  # Public fields (like Python attributes)
  public = list(
    #' @field input_string The input string
    input_string = NULL,
    
    #' @field min_value Minimum value
    min_value = NULL,
    
    #' @field max_value Maximum value
    max_value = NULL,
    
    #' @field seed_number The integer seed
    seed_number = NULL,
    
    #' @description Initialize (Python's __init__)
    #' @param input_string The string to hash
    #' @param min_value Minimum value (default: -1e9)
    #' @param max_value Maximum value (default: 1e9)
    initialize = function(input_string, min_value = -1e9, max_value = 1e9) {
      # Validate string
      if (!is.character(input_string) || length(input_string) != 1) {
        stop("input_string must be a single character string")
      }
      
      if (nchar(input_string) == 0) {
        stop("input_string cannot be empty")
      }
      
      self$input_string <- input_string
      
      # Validate range BEFORE converting to integer
      if (!is.numeric(min_value) || !is.numeric(max_value)) {
        stop("min_value and max_value must be numeric")
      }
      
      if (min_value >= max_value) {
        stop(sprintf("min_value (%.0f) must be less than max_value (%.0f)",
                    min_value, max_value))
      }
      
      # Check R's integer range limits
      max_int <- 2^31 - 1
      min_int <- -2^31
      
      if (min_value < min_int || min_value > max_int) {
        stop(sprintf("min_value (%.0f) is outside R's integer range [%d, %d]",
                    min_value, min_int, max_int))
      }
      
      if (max_value < min_int || max_value > max_int) {
        stop(sprintf("max_value (%.0f) is outside R's integer range [%d, %d]",
                    max_value, min_int, max_int))
      }
      
      # Now safe to convert
      self$min_value <- as.integer(min_value)
      self$max_value <- as.integer(max_value)
      
      # Generate seed
      self$seed_number <- private$generate_seed()
    },
    
    #' @description Generate random seeds
    #' @param count Number of seeds to generate
    #' @return Vector of random integers
    generate_seeds = function(count) {
      if (!is.numeric(count) || length(count) != 1) {
        stop("count must be a single numeric value")
      }
      
      count <- as.integer(count)
      
      if (count <= 0) {
        stop("count must be a positive integer")
      }
      
      # Set seed
      set.seed(self$seed_number)
      
      # Calculate range size - handle potential overflow
      range_size <- as.numeric(self$max_value) - as.numeric(self$min_value) + 1
      
      # Validate range size
      if (range_size > .Machine$integer.max) {
        stop("Range is too large. Maximum range size is ", .Machine$integer.max)
      }
      
      # Generate random numbers
      random_numbers <- sample.int(
        n = as.integer(range_size),
        size = count,
        replace = TRUE
      ) + self$min_value - 1
      
      return(random_numbers)
    },
    
    #' @description Get MD5 hash
    #' @return MD5 hash as hexadecimal string
    get_hash = function() {
      return(digest::digest(self$input_string, algo = "md5", serialize = FALSE))
    },
    
    #' @description Print method (Python's __str__)
    #' @param ... Additional arguments (unused)
    print = function(...) {
      cat(sprintf("SeedHashGenerator:\n"))
      cat(sprintf("  Input String: '%s'\n", self$input_string))
      cat(sprintf("  Range: [%d, %d]\n", self$min_value, self$max_value))
      cat(sprintf("  Seed Number: %d\n", self$seed_number))
      cat(sprintf("  MD5 Hash: %s\n", self$get_hash()))
      invisible(self)
    }
  ),
  
  # Private methods (Python's _method)
  private = list(
    generate_seed = function() {
      # Get MD5 hash
      hash_value <- digest::digest(self$input_string, algo = "md5", serialize = FALSE)
      
      # Convert hex to integer
      # CRITICAL: Use 7 chars (28 bits) not 8 (32 bits) to avoid overflow
      seed <- strtoi(substr(hash_value, 1, 7), base = 16)
      
      # Validate result
      if (is.na(seed)) {
        stop("Failed to generate valid seed from input string")
      }
      
      return(seed)
    }
  )
)
```

---

## 4. Common Operations Mapping

### Hashing

| Operation | Python | R |
|-----------|--------|---|
| Import | `import hashlib` | `library(digest)` |
| Hash string | `hashlib.md5(s.encode()).hexdigest()` | `digest::digest(s, algo="md5", serialize=FALSE)` |
| Hex to int | `int(hex_str[:8], 16)` | `strtoi(substr(hex_str, 1, 7), base=16)` ⚠️ Use 7 not 8! |

### Random Generation

| Operation | Python | R |
|-----------|--------|---|
| Set seed | `random.seed(n)` | `set.seed(n)` |
| Random int | `random.randint(a, b)` | `sample.int(b-a+1, 1) + a - 1` |
| Multiple | `[random.randint(a,b) for _ in range(n)]` | `sample.int(b-a+1, n, replace=TRUE) + a - 1` |

### Validation

| Check | Python | R |
|-------|--------|---|
| Is string | `isinstance(s, str)` | `is.character(s) && length(s)==1` |
| Is integer | `isinstance(n, int)` | `is.numeric(n)` then `as.integer(n)` |
| Range check | Usually not needed | ALWAYS check before `as.integer()` |
| Empty string | `len(s) == 0` | `nchar(s) == 0` |

### Error Handling

**Python:**
```python
if not isinstance(input_string, str):
    raise TypeError("input_string must be a string")

if min_value >= max_value:
    raise ValueError(f"min_value must be less than max_value")
```

**R:**
```r
if (!is.character(input_string)) {
  stop("input_string must be a character string")
}

if (min_value >= max_value) {
  stop(sprintf("min_value (%.0f) must be less than max_value (%.0f)",
              min_value, max_value))
}
```

---

## 5. Testing & Validation

### Python Tests (pytest)

**tests/test_seedhash.py:**
```python
import pytest
from seedhash import SeedHashGenerator

def test_basic_generation():
    gen = SeedHashGenerator("test")
    seeds = gen.generate_seeds(5)
    assert len(seeds) == 5
    assert all(isinstance(s, int) for s in seeds)

def test_reproducibility():
    gen1 = SeedHashGenerator("test")
    gen2 = SeedHashGenerator("test")
    assert gen1.generate_seeds(5) == gen2.generate_seeds(5)

def test_large_range():
    gen = SeedHashGenerator("test", -10**15, 10**15)  # Works in Python!
    seeds = gen.generate_seeds(5)
    assert len(seeds) == 5
```

### R Tests (testthat)

**tests/testthat/test-seedhash.R:**
```r
library(testthat)
library(seedhash)

test_that("Basic seed generation works", {
  gen <- SeedHashGenerator$new("test")
  seeds <- gen$generate_seeds(5)
  
  expect_length(seeds, 5)
  expect_true(all(is.integer(seeds)))
})

test_that("Reproducibility works", {
  gen1 <- SeedHashGenerator$new("test")
  gen2 <- SeedHashGenerator$new("test")
  
  expect_equal(gen1$generate_seeds(5), gen2$generate_seeds(5))
})

test_that("Large range fails appropriately", {
  # This would work in Python but must fail in R
  expect_error(
    SeedHashGenerator$new("test", -10^33, 10^33),
    "outside R's integer range"
  )
})

test_that("Valid large range works", {
  # This is the R-appropriate large range
  gen <- SeedHashGenerator$new("test", -1e9, 1e9)
  seeds <- gen$generate_seeds(5)
  expect_length(seeds, 5)
})
```

---

## 6. Packaging & Distribution

### Python Package Structure

```
seedhash/
├── seedhash/
│   ├── __init__.py          # Exports
│   └── core.py              # Main class
├── tests/
│   └── test_seedhash.py     # Tests
├── setup.py                 # Package config
├── pyproject.toml           # Modern config
├── README.md
└── LICENSE
```

**setup.py:**
```python
from setuptools import setup, find_packages

setup(
    name="seedhash",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],  # No external deps
    python_requires=">=3.6",
)
```

**Installation:**
```bash
pip install .
# or
pip install git+https://github.com/melhzy/seedhash.git
```

### R Package Structure

```
R/
├── R/
│   └── seedhash.R           # Main class
├── man/                     # Generated docs
│   └── *.Rd
├── tests/
│   └── testthat/
│       └── test-seedhash.R
├── DESCRIPTION              # Package metadata
├── NAMESPACE                # Exports (generated)
├── LICENSE
├── README.md
└── INSTALL.md
```

**DESCRIPTION:**
```
Package: seedhash
Type: Package
Title: Generate Reproducible Random Seeds from String Inputs
Version: 0.1.0
Authors@R: person("Your", "Name", email = "you@example.com",
                  role = c("aut", "cre"))
Description: Provides functionality to generate reproducible random seeds.
License: MIT + file LICENSE
Encoding: UTF-8
Roxygen: list(markdown = TRUE)
RoxygenNote: 7.3.2
Imports:
    R6,
    digest
Suggests:
    testthat (>= 3.0.0)
```

**Installation:**
```r
# Method 1: pak (recommended)
pak::pkg_install("github::melhzy/seedhash/R")

# Method 2: devtools
devtools::install_github("melhzy/seedhash", subdir = "R")

# Method 3: CRAN (after submission)
install.packages("seedhash")
```

---

## 7. Lessons Learned

### Critical Differences to Remember

1. **Integer Limits**
   - Python: Unlimited ✅
   - R: ±2.1 billion ⚠️
   - Solution: Validate BEFORE conversion, use smaller defaults

2. **Hex Conversion**
   - Python: `int(hash[:8], 16)` works
   - R: `strtoi(substr(hash, 1, 7), 16)` - use 7 not 8!
   - Reason: 8 hex chars = 32 bits can overflow signed int

3. **Default Ranges**
   - Python: Can use any range
   - R: Use -1e9 to 1e9 (not 0 to 2^31-1)
   - Reason: Range SPAN must also fit in integer

4. **Package Installation**
   - Python: pip handles everything
   - R: Use pak for GitHub, devtools has issues
   - CRAN: More rigorous than PyPI

5. **Documentation**
   - Python: Docstrings + Sphinx
   - R: roxygen2 comments + R CMD check
   - R requires more formal structure

6. **Class Methods**
   - Python: `self.method()`
   - R: `self$method()` (dollar sign!)
   - R: Use `private = list(...)` for private methods

7. **Error Messages**
   - Python: Can be simple
   - R: Should use `sprintf()` for formatted messages
   - Both: Clear error messages prevent user confusion

---

## Conversion Checklist

When adding new Python features to R:

- [ ] Check if feature uses large integers
- [ ] Validate integer ranges BEFORE conversion
- [ ] Use `as.numeric()` for calculations, `as.integer()` for final
- [ ] Test with edge cases: -2^31, 2^31-1, ranges > 2.1B
- [ ] Use 7 hex characters for hash-to-int conversion
- [ ] Add roxygen2 documentation (@description, @param, @return)
- [ ] Write testthat tests with R-appropriate limits
- [ ] Update DESCRIPTION if new dependencies added
- [ ] Run `devtools::check()` before committing
- [ ] Update INSTALL.md if installation changes
- [ ] Test with pak installation from GitHub

---

## Quick Reference Card

### Python → R Translation

| Python | R | Notes |
|--------|---|-------|
| `class MyClass:` | `MyClass <- R6Class("MyClass", ...)` | R6 for OOP |
| `self.attr` | `self$attr` | Dollar sign! |
| `def __init__(self, x):` | `initialize = function(x) {` | Constructor |
| `def method(self):` | `method = function() {` | Public method |
| `def _private(self):` | `private = list(method = function() {})` | Private |
| `raise ValueError(msg)` | `stop(msg)` | Error |
| `isinstance(x, int)` | `is.numeric(x)` | Type check |
| `len(items)` | `length(items)` | Length |
| `range(n)` | `1:n` or `seq_len(n)` | Sequence |
| `[x for x in items]` | `sapply(items, function(x) x)` | List comp |
| `f"{var}"` | `sprintf("%s", var)` | String format |

---

## Resources

- **R6 Documentation**: https://r6.r-lib.org/
- **roxygen2**: https://roxygen2.r-lib.org/
- **testthat**: https://testthat.r-lib.org/
- **CRAN Policies**: https://cran.r-project.org/web/packages/policies.html
- **Writing R Extensions**: https://cran.r-project.org/doc/manuals/r-release/R-exts.html
- **pak Package Manager**: https://pak.r-lib.org/

---

**Last Updated**: October 31, 2025  
**Version**: 1.0  
**Status**: Production-ready conversion guide
