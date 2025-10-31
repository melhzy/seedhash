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

### Python Package Structure (Updated)

```
Python/
├── seedhash/
│   ├── __init__.py          # Exports
│   └── core.py              # Main class
├── examples/
│   └── demo.py              # Usage examples
├── dist/                    # Built distributions
├── seedhash.egg-info/       # Package metadata
├── base.py                  # Original standalone script
├── setup.py                 # Package config
├── pyproject.toml           # Modern config
├── requirements.txt         # Dependencies (none)
└── README.md                # Python documentation
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

**Installation (Updated Paths):**
```bash
# From GitHub
pip install git+https://github.com/melhzy/seedhash.git#subdirectory=Python

# Local
cd Python
pip install .
```

### R Package Structure (Updated)

```
R/
├── R/
│   └── seedhash.R           # Main R6 class
├── man/                     # Generated docs (roxygen2)
│   └── *.Rd
├── tests/
│   └── testthat/
│       └── test-seedhash.R
├── examples/
│   └── example_usage.R
├── DESCRIPTION              # Package metadata
├── NAMESPACE                # Exports (auto-generated)
├── LICENSE                  # MIT License
├── NEWS.md                  # Version history
├── README.md                # R package docs
├── INSTALL.md               # Installation guide
├── seedhash_0.1.0.tar.gz    # Built package for CRAN
│
├── Test & Installation Files:
│   ├── fix_and_install.R    # Clean install script
│   ├── install_with_pak.R   # pak installation
│   ├── test_*.R             # Various test scripts
│   └── quick_*.R            # Quick tests
│
├── CRAN Submission Files:
│   ├── CRAN_SUBMISSION.md
│   ├── cran-comments.md
│   ├── SUBMISSION_STATUS.md
│   └── submit_to_cran.R
│
└── Documentation:
    ├── INTEGER_RANGE_SOLUTION.md
    ├── INSTALL_SOLUTION.md
    ├── GITHUB_INSTALL_TROUBLESHOOTING.md
    ├── VSCODE_R_SETUP.md
    └── README_PACKAGE.md
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

**Installation (Updated - pak recommended):**
```r
# ✅ Method 1: pak (RECOMMENDED)
install.packages("pak", repos = "https://r-lib.github.io/p/pak/stable/")
pak::pkg_install("github::melhzy/seedhash/R")

# Method 2: devtools (may have SSL/PAT issues)
devtools::install_github("melhzy/seedhash", subdir = "R")

# Method 3: Local
devtools::install("path/to/seedhash/R")

# Method 4: CRAN (after submission)
install.packages("seedhash")
```

**Why pak over devtools?**
- ✅ Handles GitHub authentication better (no PAT issues)
- ✅ No SSL certificate problems on Windows
- ✅ Faster dependency resolution
- ✅ Modern and actively maintained
- ✅ Works reliably with subdirectory installations

---

## 7. Lessons Learned (Updated with Production Experience)

### Critical Differences to Remember

1. **Integer Limits** ⚠️ CRITICAL
   - Python: Unlimited ✅
   - R: ±2.1 billion ⚠️
   - Solution: Validate BEFORE conversion, use smaller defaults (-1e9 to 1e9)
   - **Real Issue**: Used full range 0 to 2^31-1, caused overflow in generate_seeds()

2. **Hex Conversion** ⚠️ CRITICAL FIX
   - Python: `int(hash[:8], 16)` works
   - R: `strtoi(substr(hash, 1, 7), 16)` - use 7 not 8!
   - Reason: 8 hex chars = 32 bits can overflow signed int
   - **Real Issue**: 8 chars caused NA values, set.seed() failed with "not a valid integer"

3. **Default Ranges** ⚠️ CRITICAL FIX
   - Python: Can use any range
   - R: Use -1e9 to 1e9 (not 0 to 2^31-1)
   - Reason: Range SPAN must also fit in integer
   - **Real Issue**: Default 0 to 2^31-1 worked for initialization but failed in generate_seeds()

4. **Package Installation** ⚠️ IMPORTANT
   - Python: pip handles everything reliably
   - R: Use **pak** for GitHub (not devtools!)
   - CRAN: More rigorous than PyPI
   - **Real Issue**: devtools::install_github() had SSL/PAT errors, pak solved it

5. **Documentation** 
   - Python: Docstrings + Sphinx
   - R: roxygen2 comments + R CMD check
   - R requires more formal structure
   - **Real Issue**: Duplicate @field tags caused warnings

6. **Class Methods**
   - Python: `self.method()`
   - R: `self$method()` (dollar sign!)
   - R: Use `private = list(...)` for private methods
   - R: `initialize` instead of `__init__`

7. **Error Messages**
   - Python: Can be simple
   - R: Should use `sprintf()` for formatted messages
   - Both: Clear error messages prevent user confusion
   - **Real Issue**: Silent NA conversion led to cryptic "not a valid integer" error

8. **Repository Organization** ✨ NEW
   - Separate Python/ and R/ directories
   - Each with own README and examples
   - Clear separation prevents confusion
   - Makes dual-language projects maintainable

9. **Range Validation** ⚠️ CRITICAL
   - Must check BOTH individual values AND total span
   - Example: -2e9 and 2e9 are both valid, but span is 4e9 (too large!)
   - Always use `as.numeric()` for calculations, `as.integer()` for final
   - **Real Issue**: Validated values but not range size, caused sample.int() errors

10. **Build Artifacts** 
    - Python: Keep in Python/dist/
    - R: Keep seedhash_0.1.0.tar.gz in R/
    - Don't clutter root directory
    - **New**: Reorganized for clean structure

---

## Conversion Checklist (Updated)

When adding new Python features to R:

**Critical Validations:**
- [ ] Check if feature uses large integers
- [ ] Validate integer ranges BEFORE conversion (not after!)
- [ ] Check BOTH individual values AND range span
- [ ] Use `as.numeric()` for calculations, `as.integer()` only for final values
- [ ] Test with edge cases: -2^31, 2^31-1, ranges > 2.1B

**Code Implementation:**
- [ ] Use 7 hex characters (not 8) for hash-to-int conversion
- [ ] Set safe defaults: -1e9 to 1e9 (not 0 to 2^31-1)
- [ ] Add range size validation before sample.int()
- [ ] Provide clear error messages with sprintf()
- [ ] Use R6 class structure properly (self$field, not self.field)

**Documentation:**
- [ ] Add roxygen2 documentation (@description, @param, @return, @field)
- [ ] No duplicate @field tags
- [ ] Document R-specific limitations clearly
- [ ] Provide working examples with safe ranges

**Testing:**
- [ ] Write testthat tests with R-appropriate limits
- [ ] Test edge cases: NA, overflow, range limits
- [ ] Test both valid and invalid inputs
- [ ] Verify error messages are helpful

**Package Management:**
- [ ] Update DESCRIPTION if new dependencies added
- [ ] Run `devtools::check()` before committing (0 errors, 0 warnings)
- [ ] Test installation with pak (not just devtools)
- [ ] Update INSTALL.md if installation changes
- [ ] Verify README examples work

**Repository Organization:**
- [ ] Keep Python files in Python/
- [ ] Keep R files in R/
- [ ] Update relevant README files
- [ ] Test installation from GitHub with new paths

**Pre-Commit:**
- [ ] All tests pass
- [ ] No build warnings
- [ ] Documentation builds correctly
- [ ] Examples run without errors
- [ ] Git status clean in correct directories

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

## Resources (Updated)

### Official Documentation
- **R6 Documentation**: https://r6.r-lib.org/
- **roxygen2**: https://roxygen2.r-lib.org/
- **testthat**: https://testthat.r-lib.org/
- **pak Package Manager**: https://pak.r-lib.org/ ⭐ Recommended
- **devtools**: https://devtools.r-lib.org/
- **CRAN Policies**: https://cran.r-project.org/web/packages/policies.html
- **Writing R Extensions**: https://cran.r-project.org/doc/manuals/r-release/R-exts.html

### Project-Specific Documentation
- **Python Package**: [Python/README.md](Python/README.md)
- **R Package**: [R/README.md](R/README.md) and [R/INSTALL.md](R/INSTALL.md)
- **Installation Guide**: [GITHUB_INSTALL.md](GITHUB_INSTALL.md)
- **Integer Issues**: [R/INTEGER_RANGE_SOLUTION.md](R/INTEGER_RANGE_SOLUTION.md)
- **GitHub Troubleshooting**: [R/GITHUB_INSTALL_TROUBLESHOOTING.md](R/GITHUB_INSTALL_TROUBLESHOOTING.md)
- **CRAN Submission**: [R/CRAN_SUBMISSION.md](R/CRAN_SUBMISSION.md)

### Key Takeaways from This Project

1. **Always use pak for GitHub R installations** - saves hours of debugging
2. **7 hex characters, not 8** - prevents integer overflow in R
3. **Default to -1e9 to 1e9** - safe range that works for most use cases
4. **Validate before conversion** - catch errors before they become NAs
5. **Test the range span** - not just individual min/max values
6. **Separate Python/ and R/** - keeps dual-language projects organized
7. **Clear error messages** - saves user frustration
8. **Document limitations** - R users need to know about integer constraints

### Common Pitfalls Encountered

| Issue | Symptom | Solution |
|-------|---------|----------|
| 8 hex chars | "not a valid integer" | Use 7 chars: `substr(hash, 1, 7)` |
| Large default range | "Range is too large" | Use -1e9 to 1e9, not 0 to 2^31-1 |
| devtools SSL error | "cannot open URL" | Use pak instead of devtools |
| Silent NA conversion | Cryptic errors later | Validate BEFORE as.integer() |
| Range overflow | sample.int() fails | Check range SPAN, not just values |
| Duplicate @field | roxygen2 warnings | Use @description for R6 fields |
| Corrupted lazy-load | Package won't load | Remove pkg dir, clean install |

---

## Repository Structure (Updated)

After reorganization, the repository now has a clean structure:

```
seedhash/
├── Python/                      # Python implementation
│   ├── seedhash/                # Package source
│   ├── examples/                # Usage examples
│   ├── setup.py                 # Package configuration
│   └── README.md                # Python docs
│
├── R/                           # R implementation
│   ├── R/                       # R source code
│   │   └── seedhash.R           # Main R6 class
│   ├── tests/                   # testthat tests
│   ├── examples/                # R examples
│   ├── DESCRIPTION              # Package metadata
│   └── INSTALL.md               # Installation guide
│
├── PYTHON_TO_R_GUIDE.md         # This guide
└── README.md                    # Main documentation
```

## Installation Paths (Updated)

### Python Installation

```bash
# From GitHub (updated path)
pip install git+https://github.com/melhzy/seedhash.git#subdirectory=Python

# Local installation
cd Python
pip install .
```

### R Installation (Updated - pak is now recommended)

```r
# ✅ RECOMMENDED: Using pak
install.packages("pak", repos = "https://r-lib.github.io/p/pak/stable/")
pak::pkg_install("github::melhzy/seedhash/R")

# Alternative: devtools (may have issues)
devtools::install_github("melhzy/seedhash", subdir = "R")

# Local installation
devtools::install("path/to/seedhash/R")
```

**Why pak?** Better GitHub authentication, no SSL issues, faster and more reliable.

---

## Recent Fixes Applied (October 31, 2025)

### Fix #1: Seed Generation Integer Overflow
**Issue**: Using 8 hex characters caused integer overflow  
**Solution**: Changed to 7 hex characters (28 bits vs 32 bits)

```r
# OLD (caused NA values):
seed <- strtoi(substr(hash_value, 1, 8), base = 16)

# NEW (safe):
seed <- strtoi(substr(hash_value, 1, 7), base = 16)
```

### Fix #2: Default Range Too Large
**Issue**: Default range 0 to 2^31-1 exceeded sample.int() capacity  
**Solution**: Changed defaults to -1e9 to 1e9

```r
# OLD (caused range overflow):
initialize = function(input_string, min_value = 0, max_value = 2^31 - 1)

# NEW (safe default):
initialize = function(input_string, min_value = -1e9, max_value = 1e9)
```

### Fix #3: Range Size Validation
**Issue**: Large valid integers could create range > 2.1 billion  
**Solution**: Added range size validation

```r
# Calculate range size safely
range_size <- as.numeric(self$max_value) - as.numeric(self$min_value) + 1

# Validate before use
if (range_size > .Machine$integer.max) {
  stop("Range is too large. Maximum range size is ", .Machine$integer.max)
}
```

### Fix #4: Pre-Conversion Validation
**Issue**: as.integer() silently converted out-of-range values to NA  
**Solution**: Validate BEFORE conversion

```r
# Check BEFORE converting
if (min_value < -2^31 || min_value > 2^31 - 1) {
  stop(sprintf("min_value (%.0f) is outside R's integer range", min_value))
}

# Now safe to convert
self$min_value <- as.integer(min_value)
```

---

**Last Updated**: October 31, 2025 (Final)  
**Version**: 2.0  
**Status**: Production-ready with all fixes applied  
**Repository**: https://github.com/melhzy/seedhash
