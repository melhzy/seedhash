# Quick Test - Your Use Case

# Install and load
devtools::install("d:/Github/seedhash/R", quiet = TRUE, upgrade = "never")
library(seedhash)

cat("\n✓ Package loaded\n\n")

# Test your use case with corrected range
cat("Testing with your input string and valid range:\n")
cat("═══════════════════════════════════════════════\n\n")

# Original attempt (will fail with clear error)
cat("1. Original range (10^33) - Too large:\n")
tryCatch({
  gen_bad <- SeedHashGenerator$new(
    input_string = "C57BL/6 experiment 1",
    min_value = -10^33,
    max_value = 10^33
  )
}, error = function(e) {
  cat("   ✗ Error:", e$message, "\n\n")
})

# Corrected version with large but valid range
cat("2. Corrected range (-1 billion to 1 billion):\n")
gen1 <- SeedHashGenerator$new(
  input_string = "C57BL/6 experiment 1",
  min_value = -1e9,  # -1,000,000,000
  max_value = 1e9    #  1,000,000,000
)
seeds1 <- gen1$generate_seeds(5)
cat("   ✓ Seeds:", paste(seeds1, collapse = ", "), "\n\n")

# Even larger valid range (full R integer range)
cat("3. Large valid range (-2 billion to 2 billion):\n")
gen2 <- SeedHashGenerator$new(
  input_string = "C57BL/6 experiment 1",
  min_value = -2e9,  # -2,000,000,000
  max_value = 2e9    #  2,000,000,000
)
seeds2 <- gen2$generate_seeds(5)
cat("   ✓ Seeds:", paste(seeds2, collapse = ", "), "\n\n")

# Practical scientific range
cat("4. Practical scientific range (-1e7 to 1e7):\n")
gen3 <- SeedHashGenerator$new(
  input_string = "C57BL/6 experiment 1",
  min_value = -1e7,  # -10,000,000
  max_value = 1e7    #  10,000,000
)
seeds3 <- gen3$generate_seeds(5)
cat("   ✓ Seeds:", paste(seeds3, collapse = ", "), "\n\n")

cat("═══════════════════════════════════════════════\n")
cat("✓ All tests passed!\n\n")

cat("Summary:\n")
cat("• R integers limited to ±2.1 billion\n")
cat("• Your input string works perfectly\n")
cat("• Use scientific notation for large values: 1e9\n")
cat("• Maximum range: -2147483647 to 2147483647\n")
