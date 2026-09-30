# Python vs R: seedhash Comparison

This document compares the Python and R implementations of the seedhash library, highlighting similarities, differences, and how to translate code between the two versions.

## Quick Comparison Table

| Feature | Python | R |
|---------|--------|---|
| **Class System** | Native classes | R6 classes |
| **Method Access** | `.` (dot notation) | `$` (dollar notation) |
| **Installation** | `pip install` | `devtools::install_github()` |
| **Import/Load** | `import seedhash` | `library(seedhash)` |
| **Integer Size** | Unlimited | 32-bit (limited) |
| **Hash Conversion** | Full MD5 hash | First 8 hex chars |
| **Documentation** | Docstrings | Roxygen2 |

## Installation

### Python
```python
# From PyPI (when published)
pip install seedhash

# From GitHub
pip install git+https://github.com/melhzy/seedhash.git

# Local development
pip install -e .
```

### R
```r
# From GitHub
devtools::install_github("melhzy/seedhash", subdir = "R")

# Local development
devtools::install("path/to/seedhash/R")

# Or source directly
source("R/seedhash.R")
```

## Basic Usage Comparison

### Creating a Generator

**Python:**
```python
from seedhash import SeedHashGenerator

gen = SeedHashGenerator("Shalini")
```

**R:**
```r
library(seedhash)

gen <- SeedHashGenerator$new("Shalini")
```

### Generating Seeds

**Python:**
```python
seeds = gen.generate_seeds(10)
print(seeds)
```

**R:**
```r
seeds <- gen$generate_seeds(10)
print(seeds)
```

### Custom Range

**Python:**
```python
gen = SeedHashGenerator(
    input_string="MyProject",
    min_value=1,
    max_value=100
)
seeds = gen.generate_seeds(5)
```

**R:**
```r
gen <- SeedHashGenerator$new(
    input_string = "MyProject",
    min_value = 1,
    max_value = 100
)
seeds <- gen$generate_seeds(5)
```

### Getting Hash

**Python:**
```python
hash_value = gen.get_hash()
print(hash_value)
```

**R:**
```r
hash_value <- gen$get_hash()
print(hash_value)
```

## Advanced Features Comparison

### Error Handling

**Python:**
```python
try:
    gen = SeedHashGenerator("")
except ValueError as e:
    print(f"Error: {e}")

try:
    gen = SeedHashGenerator("test", min_value=100, max_value=10)
except ValueError as e:
    print(f"Error: {e}")
```

**R:**
```r
tryCatch({
    gen <- SeedHashGenerator$new("")
}, error = function(e) {
    cat("Error:", e$message, "\n")
})

tryCatch({
    gen <- SeedHashGenerator$new("test", min_value = 100, max_value = 10)
}, error = function(e) {
    cat("Error:", e$message, "\n")
})
```

### Accessing Attributes

**Python:**
```python
print(f"Input String: {gen.input_string}")
print(f"Seed Number: {gen.seed_number}")
print(f"Min Value: {gen.min_value}")
print(f"Max Value: {gen.max_value}")
```

**R:**
```r
cat("Input String:", gen$input_string, "\n")
cat("Seed Number:", gen$seed_number, "\n")
cat("Min Value:", gen$min_value, "\n")
cat("Max Value:", gen$max_value, "\n")
```

### String Representation

**Python:**
```python
print(gen)
# Output: SeedHashGenerator(input_string='Shalini', min_value=0, max_value=2147483647, seed_number=...)
```

**R:**
```r
print(gen)
# Output:
# SeedHashGenerator:
#   Input String: 'Shalini'
#   Range: [0, 2147483647]
#   Seed Number: ...
#   MD5 Hash: ...
```

## Complete Example: Side-by-Side

### Python Version
```python
from seedhash import SeedHashGenerator

# Create generator
gen = SeedHashGenerator("experiment_001", min_value=0, max_value=100)

# Generate seeds
seeds = gen.generate_seeds(10)
print(f"Seeds: {seeds}")

# Get hash
hash_val = gen.get_hash()
print(f"Hash: {hash_val}")

# Verify reproducibility
gen2 = SeedHashGenerator("experiment_001", min_value=0, max_value=100)
seeds2 = gen2.generate_seeds(10)
print(f"Reproducible: {seeds == seeds2}")

# Error handling
try:
    bad_gen = SeedHashGenerator("")
except ValueError as e:
    print(f"Caught error: {e}")
```

### R Version
```r
library(seedhash)

# Create generator
gen <- SeedHashGenerator$new("experiment_001", min_value = 0, max_value = 100)

# Generate seeds
seeds <- gen$generate_seeds(10)
cat("Seeds:", paste(seeds, collapse = ", "), "\n")

# Get hash
hash_val <- gen$get_hash()
cat("Hash:", hash_val, "\n")

# Verify reproducibility
gen2 <- SeedHashGenerator$new("experiment_001", min_value = 0, max_value = 100)
seeds2 <- gen2$generate_seeds(10)
cat("Reproducible:", identical(seeds, seeds2), "\n")

# Error handling
tryCatch({
    bad_gen <- SeedHashGenerator$new("")
}, error = function(e) {
    cat("Caught error:", e$message, "\n")
})
```

## Key Differences Explained

### 1. Integer Handling

**Python:**
- Uses unlimited precision integers
- Seed number is the MD5 digest modulo 2^32
- Seed range up to 2^31 - 1 by default

**R:**
- Uses 32-bit integers (limited to ~2.1 billion)
- Seed number is the MD5 digest modulo 2^32, stored as a double
- Same default seed range (2^31 - 1)

**Impact:** `seed_number` is the same in both languages. Because it can exceed R's integer range, seed R's generator with `gen$set_seed()` rather than `set.seed(gen$seed_number)`.

### 2. Random Number Generation

**Python:**
```python
random.seed(seed_number)
random_numbers = [random.randint(min_val, max_val) for _ in range(count)]
```

**R:**
```r
gen$set_seed()  # set.seed() with seed_number mapped into R's integer range
random_numbers <- sample.int(n = max_val - min_val + 1, size = count, replace = TRUE) + min_val - 1
```

**Impact:** Even with the same seed, the actual random numbers generated will differ between Python and R due to different underlying algorithms.

### 3. Class Syntax

**Python (Native Classes):**
```python
class SeedHashGenerator:
    def __init__(self, input_string, min_value=0, max_value=2**31-1):
        self.input_string = input_string
        
    def generate_seeds(self, count):
        return [...]
```

**R (R6 Classes):**
```r
SeedHashGenerator <- R6Class(
    "SeedHashGenerator",
    public = list(
        input_string = NULL,
        initialize = function(input_string, min_value = 0, max_value = 2^31-1) {
            self$input_string <- input_string
        },
        generate_seeds = function(count) {
            return(c(...))
        }
    )
)
```

### 4. Type Checking

**Python:**
```python
if not isinstance(input_string, str):
    raise TypeError("input_string must be a string")
```

**R:**
```r
if (!is.character(input_string) || length(input_string) != 1) {
    stop("input_string must be a single character string")
}
```

## Migration Guide

### From Python to R

1. **Change import to library load:**
   - `from seedhash import SeedHashGenerator` → `library(seedhash)`

2. **Change instantiation:**
   - `gen = SeedHashGenerator(...)` → `gen <- SeedHashGenerator$new(...)`

3. **Change method calls:**
   - `gen.method()` → `gen$method()`

4. **Change assignment:**
   - `=` → `<-` (though `=` works in R too)

5. **Change list comprehensions:**
   - `[x for x in items]` → `lapply(items, function(x) x)` or vectorized operations

### From R to Python

1. **Change library to import:**
   - `library(seedhash)` → `from seedhash import SeedHashGenerator`

2. **Change instantiation:**
   - `gen <- SeedHashGenerator$new(...)` → `gen = SeedHashGenerator(...)`

3. **Change method calls:**
   - `gen$method()` → `gen.method()`

4. **Change vectorized operations to loops:**
   - R's vectorization → Python list comprehensions or numpy

## Performance Considerations

### Python
- Generally faster for large-scale computations
- Better for heavy numerical work
- Native list comprehensions are efficient

### R
- Optimized for statistical operations
- Vectorized operations are very fast
- May be slower for loops but fast for vector operations

## When to Use Each

### Use Python Version When:
- You need unlimited integer precision
- Working in a Python data science stack (pandas, numpy, scikit-learn)
- Building web applications or APIs
- Need specific Python library integrations

### Use R Version When:
- Working primarily in R/RStudio
- Integrating with R statistical packages
- Creating R Shiny applications
- Working with R data frames and tidyverse

## Reproducibility Across Languages

Both implementations derive `seed_number` the same way: the MD5 digest of the UTF-8 encoded input string, modulo 2^32. The same string therefore has the same `seed_number` in Python and R.

The seeds returned by `generate_seeds()` still differ between the languages, because each one draws them from its own random number generator (Python's `random.Random` and R's `sample.int()`). Each implementation is reproducible within its own language. If you need identical seed lists in both languages, export the generated seeds rather than sharing only the input string.

## Example: Same Seed Number, Different Seed Lists

**Python:**
```python
gen = SeedHashGenerator("test")
print(gen.seed_number)  # 640136438
seeds = gen.generate_seeds(3)  # Python's own sequence
```

**R:**
```r
gen <- SeedHashGenerator$new("test")
print(gen$seed_number)  # 640136438 (same as Python)
seeds <- gen$generate_seeds(3)  # R's own sequence, differs from Python
```

R stores `seed_number` as a double because it can exceed R's integer range; it is converted to a valid `set.seed()` value internally.

## Conclusion

Both implementations provide the same high-level functionality:
- ✅ Deterministic seed generation from strings
- ✅ Customizable ranges
- ✅ Error handling
- ✅ Reproducibility within language
- ✅ Similar API design

Choose the version that matches your primary development environment and ecosystem.
