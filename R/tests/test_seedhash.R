# Test script for seedhash R package
# Run this script to test the functionality

library(R6)
library(digest)

# Source the main file
source("R/seedhash.R")

cat("=== Running Tests for seedhash R Package ===\n\n")

# Test 1: Basic initialization
cat("Test 1: Basic initialization... ")
tryCatch({
  gen <- SeedHashGenerator$new("test")
  if (!is.null(gen$input_string) && 
      !is.null(gen$seed_number) &&
      gen$min_value == 0 &&
      gen$max_value == 2^31 - 1) {
    cat("PASSED\n")
  } else {
    cat("FAILED\n")
  }
}, error = function(e) {
  cat("FAILED:", e$message, "\n")
})

# Test 2: Custom range
cat("Test 2: Custom range... ")
tryCatch({
  gen <- SeedHashGenerator$new("test", min_value = 10, max_value = 100)
  if (gen$min_value == 10 && gen$max_value == 100) {
    cat("PASSED\n")
  } else {
    cat("FAILED\n")
  }
}, error = function(e) {
  cat("FAILED:", e$message, "\n")
})

# Test 3: Empty string error
cat("Test 3: Empty string error... ")
tryCatch({
  gen <- SeedHashGenerator$new("")
  cat("FAILED (should have thrown error)\n")
}, error = function(e) {
  if (grepl("cannot be empty", e$message)) {
    cat("PASSED\n")
  } else {
    cat("FAILED (wrong error)\n")
  }
})

# Test 4: Invalid range error
cat("Test 4: Invalid range error... ")
tryCatch({
  gen <- SeedHashGenerator$new("test", min_value = 100, max_value = 10)
  cat("FAILED (should have thrown error)\n")
}, error = function(e) {
  if (grepl("must be less than", e$message)) {
    cat("PASSED\n")
  } else {
    cat("FAILED (wrong error)\n")
  }
})

# Test 5: Generate seeds
cat("Test 5: Generate seeds... ")
tryCatch({
  gen <- SeedHashGenerator$new("test")
  seeds <- gen$generate_seeds(10)
  if (length(seeds) == 10 && is.numeric(seeds)) {
    cat("PASSED\n")
  } else {
    cat("FAILED\n")
  }
}, error = function(e) {
  cat("FAILED:", e$message, "\n")
})

# Test 6: Reproducibility
cat("Test 6: Reproducibility... ")
tryCatch({
  gen1 <- SeedHashGenerator$new("reproducibility_test")
  seeds1 <- gen1$generate_seeds(5)
  
  gen2 <- SeedHashGenerator$new("reproducibility_test")
  seeds2 <- gen2$generate_seeds(5)
  
  if (identical(seeds1, seeds2)) {
    cat("PASSED\n")
  } else {
    cat("FAILED (seeds not identical)\n")
  }
}, error = function(e) {
  cat("FAILED:", e$message, "\n")
})

# Test 7: Get hash
cat("Test 7: Get hash... ")
tryCatch({
  gen <- SeedHashGenerator$new("test")
  hash <- gen$get_hash()
  if (is.character(hash) && nchar(hash) == 32) {
    cat("PASSED\n")
  } else {
    cat("FAILED\n")
  }
}, error = function(e) {
  cat("FAILED:", e$message, "\n")
})

# Test 8: Invalid count
cat("Test 8: Invalid count error... ")
tryCatch({
  gen <- SeedHashGenerator$new("test")
  seeds <- gen$generate_seeds(-5)
  cat("FAILED (should have thrown error)\n")
}, error = function(e) {
  if (grepl("positive integer", e$message)) {
    cat("PASSED\n")
  } else {
    cat("FAILED (wrong error)\n")
  }
})

# Test 9: Convenience function
cat("Test 9: Convenience function... ")
tryCatch({
  gen <- create_seedhash("convenience_test")
  seeds <- gen$generate_seeds(5)
  if (length(seeds) == 5) {
    cat("PASSED\n")
  } else {
    cat("FAILED\n")
  }
}, error = function(e) {
  cat("FAILED:", e$message, "\n")
})

# Test 10: Seeds within range
cat("Test 10: Seeds within range... ")
tryCatch({
  gen <- SeedHashGenerator$new("range_test", min_value = 10, max_value = 20)
  seeds <- gen$generate_seeds(100)
  if (all(seeds >= 10 & seeds <= 20)) {
    cat("PASSED\n")
  } else {
    cat("FAILED (seeds out of range)\n")
  }
}, error = function(e) {
  cat("FAILED:", e$message, "\n")
})

cat("\n=== All Tests Completed ===\n")
