# Installation Guide for seedhash R Package

## Prerequisites

Before installing the seedhash R package, ensure you have:

1. **R** (version 3.5.0 or higher)
2. **Required packages**: `R6`, `digest` (installed automatically)

## Method 1: Install from GitHub using pak ✅ RECOMMENDED

**pak** is a modern package manager that reliably handles GitHub installations:

```r
# Install pak (one-time setup)
install.packages("pak", repos = "https://r-lib.github.io/p/pak/stable/")

# Install seedhash from GitHub
pak::pkg_install("github::melhzy/seedhash/R")

# Load the library
library(seedhash)

# Test it
gen <- SeedHashGenerator$new("experiment_1")
seeds <- gen$generate_seeds(5)
print(seeds)
```

**Repository**: https://github.com/melhzy/seedhash/tree/main/R

## Method 2: Install from GitHub using devtools (Alternative)

If you prefer devtools (may have authentication issues on some systems):

```r
# Install devtools if you haven't already
install.packages("devtools")

# Install seedhash from GitHub
devtools::install_github("melhzy/seedhash", subdir = "R")

# Load the library
library(seedhash)
```

## Method 2: Install from GitHub using devtools (Alternative)

If you prefer devtools (may have authentication issues on some systems):

```r
# Install devtools if you haven't already
install.packages("devtools")

# Install seedhash from GitHub
devtools::install_github("melhzy/seedhash", subdir = "R")

# Load the library
library(seedhash)
```

## Method 3: Install from Local Source

If you have cloned the repository locally:

```r
# Install devtools if needed
install.packages("devtools")

# Install from local directory (replace with your actual path)
devtools::install("d:/Github/seedhash/R")

# Load the library
library(seedhash)
```

## Method 4: Install from CRAN (After Publication)

Once published to CRAN, you can install with:

```r
install.packages("seedhash")
library(seedhash)
```

## Method 5: Manual Installation (Development)

For development purposes, you can source the files directly without installation:

```r
# Install dependencies
install.packages(c("R6", "digest"))

# Source the main file
# Replace with your actual path
source("d:/Github/seedhash/R/R/seedhash.R")

# Now you can use the functions directly
gen <- SeedHashGenerator$new("test")
```

## Installing Dependencies

The package requires two dependencies:

```r
# Install both at once
install.packages(c("R6", "digest"))

# Or install individually
install.packages("R6")      # For R6 class system
install.packages("digest")   # For MD5 hashing
```

## Verifying Installation

After installation, verify that everything works:

```r
# Load the library (if installed as package)
library(seedhash)

# Test basic functionality
gen <- SeedHashGenerator$new("test")
seeds <- gen$generate_seeds(5)
print(seeds)

# If this runs without errors, installation was successful!
```

## Running Tests

To run the test suite:

```r
# If using source files directly
source("d:/Github/seedhash/R/tests/test_seedhash.R")

# Tests will run automatically and show results
```

## Running Examples

To see various usage examples:

```r
# If using source files directly
source("d:/Github/seedhash/R/examples/example_usage.R")

# This will demonstrate all major features
```

## Troubleshooting

### Issue: Cannot find package 'R6' or 'digest'

**Solution**: Install the missing dependencies:
```r
install.packages(c("R6", "digest"))
```

### Issue: devtools::install_github() fails

**Solution 1**: Try updating devtools:
```r
install.packages("devtools")
```

**Solution 2**: Install from local source instead (Method 2)

### Issue: "there is no package called 'seedhash'"

**Solution**: Make sure you've installed the package. If using source files, use `source()` instead of `library()`.

### Issue: RStudio cannot find the package

**Solution**: Restart RStudio after installation:
```r
# In RStudio: Session > Restart R
# Then try again:
library(seedhash)
```

## Building from Source

If you want to build the package yourself:

```r
# Navigate to the parent directory containing the R folder
setwd("d:/Github/seedhash")

# Build the package
devtools::build("R")

# This creates a .tar.gz file
# Install the built package
install.packages("seedhash_0.1.0.tar.gz", repos = NULL, type = "source")
```

## Uninstalling

To remove the package:

```r
remove.packages("seedhash")
```

## Next Steps

After successful installation:

1. Read the [README.md](README.md) for usage examples
2. Check out [example_usage.R](examples/example_usage.R) for comprehensive examples
3. Run the test suite in [test_seedhash.R](tests/test_seedhash.R)
4. Read the documentation: `?SeedHashGenerator`

## Support

For issues or questions:
- GitHub Issues: https://github.com/melhzy/seedhash/issues
- Check the README.md for common use cases
- Review example_usage.R for code examples
