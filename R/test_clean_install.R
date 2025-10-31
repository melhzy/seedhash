# Test clean installation
library(seedhash)

cat("✓ Package loaded successfully!\n\n")

# Test 1: Default parameters
cat("Test 1: Default range (-1e9 to 1e9)\n")
gen1 <- SeedHashGenerator$new("C57BL/6 experiment 1")
seeds1 <- gen1$generate_seeds(5)
cat("Generated seeds:", paste(seeds1, collapse = ", "), "\n")
print(gen1)

cat("\n---\n\n")

# Test 2: Custom small range
cat("Test 2: Custom range (0 to 10000)\n")
gen2 <- SeedHashGenerator$new("C57BL/6 experiment 1", 0, 10000)
seeds2 <- gen2$generate_seeds(5)
cat("Generated seeds:", paste(seeds2, collapse = ", "), "\n")
print(gen2)

cat("\n---\n\n")

# Test 3: Error handling - values too large
cat("Test 3: Error handling (10^33 should fail)\n")
tryCatch({
  gen3 <- SeedHashGenerator$new("test", -10^33, 10^33)
  cat("❌ Should have thrown an error!\n")
}, error = function(e) {
  cat("✓ Correctly caught error:", e$message, "\n")
})

cat("\n✅ All tests completed!\n")
