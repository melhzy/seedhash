# 🎯 Quick Start: Install seedhash from GitHub

GitHub Repository: **https://github.com/melhzy/seedhash/tree/main/R**

## ✅ Installation (Copy & Paste)

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

## 📚 Usage Examples

```r
# Example 1: Default range (-1 billion to 1 billion)
gen1 <- SeedHashGenerator$new("C57BL/6 experiment 1")
seeds1 <- gen1$generate_seeds(5)

# Example 2: Custom range
gen2 <- SeedHashGenerator$new("my_experiment", min_value = 0, max_value = 10000)
seeds2 <- gen2$generate_seeds(10)

# Example 3: Get MD5 hash
hash <- gen1$get_hash()
print(hash)
```

## 🔧 Why pak instead of devtools?

- ✅ Better GitHub authentication handling
- ✅ No SSL certificate issues  
- ✅ Faster and more reliable
- ✅ Modern dependency resolution

## 📖 Full Documentation

See `R/INSTALL.md` for complete installation methods and troubleshooting.

---

**Status**: ✅ Working and tested  
**Last Updated**: October 31, 2025
