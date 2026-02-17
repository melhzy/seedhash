# seedhash - R Package

Deterministic seed generation from string inputs using MD5 hashing.

## Overview

The `seedhash` R package provides a simple way to generate reproducible random seeds from string inputs. This is particularly useful for:

- Reproducible experiments and simulations
- Generating consistent random numbers across different runs
- Using human-readable identifiers as seeds

## Installation

### From GitHub

You can install the development version from GitHub:

```r
# Install devtools if you haven't already
install.packages("devtools")

# Install seedhash
devtools::install_github("melhzy/seedhash", subdir = "R")
```

### Dependencies

The package requires:
- R (>= 3.5.0)
- digest
- R6

Install dependencies manually if needed:

```r
install.packages(c("digest", "R6"))
```

## Quick Start

### Basic Usage

```r
library(seedhash)

# Create a generator with default range (0 to 2^31 - 1)
gen <- SeedHashGenerator$new("Shalini")

# Generate 10 random seeds
seeds <- gen$generate_seeds(10)
print(seeds)

# Get the MD5 hash
hash_value <- gen$get_hash()
print(hash_value)

# Print generator info
print(gen)
```

### Custom Range

```r
# Create a generator with custom range
gen_custom <- SeedHashGenerator$new(
  input_string = "MyProject",
  min_value = 1,
  max_value = 100
)

# Generate 5 random seeds in the range [1, 100]
seeds <- gen_custom$generate_seeds(5)
print(seeds)
```

### Using the Convenience Function

```r
# Alternative way to create a generator
gen <- create_seedhash("Shalini")
seeds <- gen$generate_seeds(10)
```

## Features

### SeedHashGenerator Class

The main class that handles seed generation:

- **`new(input_string, min_value = 0, max_value = 2^31 - 1)`**: Initialize a new generator
- **`generate_seeds(count)`**: Generate a specified number of random seeds
- **`get_hash()`**: Get the MD5 hash of the input string
- **`print()`**: Display generator information

### Parameters

- **`input_string`**: A non-empty string used as the basis for seed generation
- **`min_value`**: Minimum value for the random number range (default: 0)
- **`max_value`**: Maximum value for the random number range (default: 2^31 - 1)
- **`count`**: Number of random seeds to generate

### Error Handling

The package includes comprehensive error handling:

```r
# Empty string
tryCatch(
  SeedHashGenerator$new(""),
  error = function(e) print(e$message)
)
# Output: "input_string cannot be empty"

# Invalid range
tryCatch(
  SeedHashGenerator$new("test", min_value = 100, max_value = 10),
  error = function(e) print(e$message)
)
# Output: "min_value (100) must be less than max_value (10)"

# Invalid count
tryCatch(
  gen$generate_seeds(-5),
  error = function(e) print(e$message)
)
# Output: "count must be a positive integer"
```

## Examples

### Example 1: Reproducible Experiments

```r
# Run 1
gen1 <- SeedHashGenerator$new("experiment_001")
results1 <- gen1$generate_seeds(5)

# Run 2 (same input string)
gen2 <- SeedHashGenerator$new("experiment_001")
results2 <- gen2$generate_seeds(5)

# Results are identical
identical(results1, results2)  # TRUE
```

### Example 2: Multiple Experiments with Different Seeds

```r
experiments <- c("exp_A", "exp_B", "exp_C")

for (exp_name in experiments) {
  gen <- SeedHashGenerator$new(exp_name)
  seeds <- gen$generate_seeds(3)
  cat(sprintf("Experiment %s: %s\n", exp_name, paste(seeds, collapse = ", ")))
}
```

### Example 3: Custom Range for Specific Use Cases

```r
# Generate seeds for selecting items from a list of 50
gen <- SeedHashGenerator$new("selection_task", min_value = 1, max_value = 50)
indices <- gen$generate_seeds(10)

# Generate seeds for probability sampling (0-100)
gen_prob <- SeedHashGenerator$new("probability_task", min_value = 0, max_value = 100)
probabilities <- gen_prob$generate_seeds(20)
```

## Comparison with Python Version

This R package mirrors the functionality of the Python `seedhash` library:

| Feature | Python | R |
|---------|--------|---|
| Class-based API | ✓ | ✓ (R6) |
| MD5 hashing | ✓ | ✓ |
| Custom range | ✓ | ✓ |
| Error handling | ✓ | ✓ |
| Reproducibility | ✓ | ✓ |

### Key Differences

1. **Seed Size**: R uses 32-bit integers for seeds, while Python can handle larger integers. The R version uses the first 8 hex characters of the MD5 hash.
2. **Syntax**: R uses `$` for method calls (e.g., `gen$generate_seeds()`), while Python uses `.` (e.g., `gen.generate_seeds()`).
3. **Random Number Generation**: R uses `sample.int()` while Python uses `random.randint()`.

## How It Works

1. **Hash Generation**: The input string is hashed using MD5 to create a deterministic hexadecimal value
2. **Seed Conversion**: The hash is converted to an integer seed
3. **Random Generation**: R's random number generator is seeded with this value
4. **Number Generation**: Random numbers are generated within the specified range

## License

MIT License - see LICENSE file for details.

## Author

**Ziyuan Huang**
- ORCID: [0000-0002-2215-2473](https://orcid.org/0000-0002-2215-2473)
- Affiliation: University of Massachusetts Chan Medical School
- GitHub: [@melhzy](https://github.com/melhzy)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Related Projects

- Python version: [seedhash (Python)](https://github.com/melhzy/seedhash)

## Support

For issues, questions, or contributions, please visit:
https://github.com/melhzy/seedhash
