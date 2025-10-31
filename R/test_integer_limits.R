# Testing seedhash with Fixed Integer Range Validation

cat("═══════════════════════════════════════════════════════\n")
cat("  Testing seedhash R Package - Integer Range Handling\n")
cat("═══════════════════════════════════════════════════════\n\n")

# Load required packages
if (!require("devtools", quietly = TRUE)) install.packages("devtools")
if (!require("R6", quietly = TRUE)) install.packages("R6")
if (!require("digest", quietly = TRUE)) install.packages("digest")

# Install/reload the updated package
cat("Installing updated package...\n")
devtools::install("d:/Github/seedhash/R", quiet = TRUE, upgrade = "never")
library(seedhash)

cat("✓ Package loaded\n\n")

# Test 1: Valid range within R's integer limits
cat("Test 1: Valid range within R's integer limits\n")
cat("─────────────────────────────────────────────────────\n")
tryCatch({
  gen1 <- SeedHashGenerator$new(
    input_string = "C57BL/6 experiment 1",
    min_value = 0,
    max_value = 2^31 - 1
  )
  seeds1 <- gen1$generate_seeds(5)
  cat("✓ Success! Generated seeds:\n")
  print(seeds1)
  cat("\n")
}, error = function(e) {
  cat("✗ Error:", e$message, "\n\n")
})

# Test 2: Smaller custom range
cat("Test 2: Smaller custom range (1 to 1000)\n")
cat("─────────────────────────────────────────────────────\n")
tryCatch({
  gen2 <- SeedHashGenerator$new(
    input_string = "C57BL/6 experiment 1",
    min_value = 1,
    max_value = 1000
  )
  seeds2 <- gen2$generate_seeds(5)
  cat("✓ Success! Generated seeds:\n")
  print(seeds2)
  cat("Range check:", all(seeds2 >= 1 & seeds2 <= 1000), "\n\n")
}, error = function(e) {
  cat("✗ Error:", e$message, "\n\n")
})

# Test 3: Negative range
cat("Test 3: Negative range (-1000 to 1000)\n")
cat("─────────────────────────────────────────────────────\n")
tryCatch({
  gen3 <- SeedHashGenerator$new(
    input_string = "C57BL/6 experiment 1",
    min_value = -1000,
    max_value = 1000
  )
  seeds3 <- gen3$generate_seeds(5)
  cat("✓ Success! Generated seeds:\n")
  print(seeds3)
  cat("Range check:", all(seeds3 >= -1000 & seeds3 <= 1000), "\n\n")
}, error = function(e) {
  cat("✗ Error:", e$message, "\n\n")
})

# Test 4: OUT OF RANGE - Should fail gracefully with clear error
cat("Test 4: Out of range values (10^33) - Should fail\n")
cat("─────────────────────────────────────────────────────\n")
tryCatch({
  gen4 <- SeedHashGenerator$new(
    input_string = "C57BL/6 experiment 1",
    min_value = -10^33,
    max_value = 10^33
  )
  seeds4 <- gen4$generate_seeds(5)
  cat("✗ This should have failed!\n\n")
}, error = function(e) {
  cat("✓ Expected error (values too large):\n")
  cat("  ", e$message, "\n\n")
})

# Test 5: Maximum valid range
cat("Test 5: Maximum valid range for R integers\n")
cat("─────────────────────────────────────────────────────\n")
tryCatch({
  gen5 <- SeedHashGenerator$new(
    input_string = "C57BL/6 experiment 1",
    min_value = -2^31,
    max_value = 2^31 - 1
  )
  seeds5 <- gen5$generate_seeds(5)
  cat("✓ Success! Generated seeds:\n")
  print(seeds5)
  cat("\n")
}, error = function(e) {
  cat("✗ Error:", e$message, "\n\n")
})

# Display R's integer limits
cat("═══════════════════════════════════════════════════════\n")
cat("  R Integer Limits Information\n")
cat("═══════════════════════════════════════════════════════\n\n")

cat("R uses 32-bit integers:\n")
cat("  Minimum:", -2^31, "(-2,147,483,648)\n")
cat("  Maximum:", 2^31 - 1, "(2,147,483,647)\n\n")

cat("For larger values, R would need numeric (double) type,\n")
cat("but sample.int() requires integer range.\n\n")

cat("Recommended ranges for your use case:\n")
cat("  • Default:     0 to 2,147,483,647\n")
cat("  • Symmetric:   -2,147,483,648 to 2,147,483,647\n")
cat("  • Custom:      Any range within above limits\n")
cat("  • Scientific:  Use scientific notation within limits\n")
cat("                 e.g., -1e9 to 1e9\n\n")

cat("═══════════════════════════════════════════════════════\n")
cat("✓ All tests completed!\n")
cat("═══════════════════════════════════════════════════════\n")
