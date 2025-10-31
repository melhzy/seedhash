# ══════════════════════════════════════════════════════════════════════════════
# Install seedhash from GitHub: https://github.com/melhzy/seedhash/tree/main/R
# ══════════════════════════════════════════════════════════════════════════════

cat("Installing seedhash from GitHub...\n\n")

# Method 1: Using devtools with proper authentication bypass
cat("Method 1: devtools::install_github with auth = NULL\n")

if (!require("devtools", quietly = TRUE)) {
  install.packages("devtools")
}

# Clear problematic environment variables
Sys.unsetenv("GITHUB_PAT")
Sys.unsetenv("GITHUB_TOKEN")

# Install without authentication (works for public repos)
tryCatch({
  devtools::install_github(
    repo = "melhzy/seedhash",
    subdir = "R",
    auth_token = NULL,
    quiet = FALSE,
    force = TRUE
  )
  cat("✅ Method 1 succeeded!\n\n")
}, error = function(e) {
  cat("❌ Method 1 failed:", e$message, "\n")
  cat("Trying alternative method...\n\n")
  
  # Method 2: Using pak (modern alternative)
  cat("Method 2: Using pak package\n")
  if (!require("pak", quietly = TRUE)) {
    install.packages("pak")
  }
  
  pak::pkg_install("melhzy/seedhash/R")
  cat("✅ Method 2 succeeded!\n\n")
})

# Test the installation
cat("═══════════════════════════════════════════════════\n")
cat("Testing installed package...\n")
cat("═══════════════════════════════════════════════════\n\n")

library(seedhash)

# Test 1: Basic functionality
cat("Test 1: Basic usage\n")
gen1 <- SeedHashGenerator$new("experiment_1")
seeds1 <- gen1$generate_seeds(5)
cat("Generated seeds:", paste(seeds1, collapse = ", "), "\n")
cat("✅ Test 1 passed\n\n")

# Test 2: Custom range
cat("Test 2: Custom range (0 to 10000)\n")
gen2 <- SeedHashGenerator$new("my_experiment", 0, 10000)
seeds2 <- gen2$generate_seeds(5)
cat("Generated seeds:", paste(seeds2, collapse = ", "), "\n")
cat("✅ Test 2 passed\n\n")

# Test 3: Large range
cat("Test 3: Large range (-1e9 to 1e9)\n")
gen3 <- SeedHashGenerator$new("C57BL/6 experiment 1", -1e9, 1e9)
seeds3 <- gen3$generate_seeds(5)
cat("Generated seeds:", paste(seeds3, collapse = ", "), "\n")
cat("✅ Test 3 passed\n\n")

cat("═══════════════════════════════════════════════════\n")
cat("✅ ALL TESTS PASSED!\n")
cat("═══════════════════════════════════════════════════\n\n")

cat("Package successfully installed from:\n")
cat("https://github.com/melhzy/seedhash/tree/main/R\n\n")

cat("To use in your R scripts:\n")
cat("  library(seedhash)\n")
cat("  gen <- SeedHashGenerator$new('your_experiment')\n")
cat("  seeds <- gen$generate_seeds(5)\n")
