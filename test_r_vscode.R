# Test R Environment in VS Code
# Run each line with Ctrl+Enter

# 1. Basic R functionality
print("✓ R is working in VS Code!")

# 2. Math operations
x <- 1:10
cat("Mean of 1:10 =", mean(x), "\n")

# 3. Load your seedhash package
setwd("d:/Github/seedhash/R")

# Check if devtools is available
if (!require("devtools", quietly = TRUE)) {
  cat("⚠ Installing devtools...\n")
  install.packages("devtools")
}

# Try loading the package
cat("\n--- Testing seedhash package ---\n")
tryCatch({
  # Source the main file
  source("R/seedhash.R")
  
  # Test the package
  gen <- SeedHashGenerator$new("VSCodeTest")
  seeds <- gen$generate_seeds(5)
  
  cat("✓ Package loaded successfully!\n")
  cat("Generated seeds:", paste(seeds, collapse = ", "), "\n")
  print(gen)
  
}, error = function(e) {
  cat("⚠ Error loading package:", e$message, "\n")
  cat("Make sure R6 and digest are installed:\n")
  cat("  install.packages(c('R6', 'digest'))\n")
})

# 4. Simple plot (optional)
cat("\n--- Testing plotting ---\n")
plot(1:10, main = "Test Plot", col = "blue", pch = 19)
cat("✓ Plot created (check Plots pane if available)\n")

cat("\n✅ All tests complete!\n")
cat("\nNext steps:\n")
cat("1. Press Ctrl+Enter to run each line\n")
cat("2. View results in R terminal\n")
cat("3. Try: gen$generate_seeds(10)\n")
