# seedhash - R Package

This directory contains the R implementation of the seedhash library.

## Structure

```
R/
├── R/                          # R source code
│   └── seedhash.R              # SeedHashGenerator R6 class
├── man/                        # Generated documentation (roxygen2)
│   └── *.Rd
├── tests/                      # Unit tests
│   └── testthat/
│       └── test-seedhash.R
├── examples/                   # Usage examples
│   └── example_usage.R
├── DESCRIPTION                 # Package metadata
├── NAMESPACE                   # Exports (auto-generated)
├── LICENSE                     # MIT License
├── NEWS.md                     # Version history
├── README.md                   # R package documentation
├── INSTALL.md                  # Installation instructions
├── seedhash_0.1.0.tar.gz      # Built package for CRAN
│
├── Test & Installation Files:
│   ├── fix_and_install.R
│   ├── install_with_pak.R
│   ├── test_*.R
│   └── quick_*.R
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
    └── VSCODE_R_SETUP.md
```

## Installation

### ✅ Recommended: Using pak

```r
# Install pak
install.packages("pak", repos = "https://r-lib.github.io/p/pak/stable/")

# Install seedhash from GitHub
pak::pkg_install("github::melhzy/seedhash/R")
```

### Alternative: Using devtools

```r
# Install devtools
install.packages("devtools")

# Install from GitHub
devtools::install_github("melhzy/seedhash", subdir = "R")

# Or install from local directory
devtools::install("path/to/seedhash/R")
```

### From CRAN (After Publication)

```r
install.packages("seedhash")
```

## Quick Start

```r
library(seedhash)

# Create a generator
gen <- SeedHashGenerator$new("my_experiment")

# Generate 5 random seeds
seeds <- gen$generate_seeds(5)
print(seeds)

# Get the MD5 hash
cat("Hash:", gen$get_hash(), "\n")

# View generator details
print(gen)
```

## Features

- **R6 class** for object-oriented design
- **Reproducible** seeds based on string input
- **Safe integer handling** with clear error messages
- **Default range**: -1 billion to +1 billion
- **Dependencies**: R6, digest

## Important: R Integer Limitations

⚠️ R uses 32-bit signed integers: **-2,147,483,648 to 2,147,483,647**

```r
# ✅ This works
gen <- SeedHashGenerator$new("test", -1e9, 1e9)

# ❌ This fails (range too large)
gen <- SeedHashGenerator$new("test", -10^33, 10^33)
```

See [INTEGER_RANGE_SOLUTION.md](INTEGER_RANGE_SOLUTION.md) for details.

## Testing

```r
# Run tests
devtools::test()

# Or using R CMD check
R CMD check .
```

## Building for CRAN

```r
# Build package
devtools::build()

# Run CRAN checks
devtools::check()

# Submit to CRAN
# See CRAN_SUBMISSION.md for complete guide
```

## Development Notes

When developing R features based on Python:
- Validate integers BEFORE `as.integer()` conversion
- Use 7 hex characters (not 8) for hash-to-int
- Default range: -1e9 to 1e9 (not full int range)
- Test edge cases around ±2^31

See [PYTHON_TO_R_GUIDE.md](../PYTHON_TO_R_GUIDE.md) for complete conversion guide.

## Documentation

- **Installation**: [INSTALL.md](INSTALL.md)
- **CRAN Submission**: [CRAN_SUBMISSION.md](CRAN_SUBMISSION.md)
- **Integer Limits**: [INTEGER_RANGE_SOLUTION.md](INTEGER_RANGE_SOLUTION.md)
- **Troubleshooting**: [GITHUB_INSTALL_TROUBLESHOOTING.md](GITHUB_INSTALL_TROUBLESHOOTING.md)

## CRAN Submission Status

See [SUBMISSION_STATUS.md](SUBMISSION_STATUS.md) for current status.

---

**Version**: 0.1.0  
**License**: MIT  
**R**: >= 3.5.0  
**Status**: Ready for CRAN submission
