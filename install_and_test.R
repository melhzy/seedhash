# Clean installation script for seedhash
# This avoids the lazy-load database corruption issue

cat("Installing seedhash package...\n\n")

# Method 1: Direct R CMD INSTALL (most reliable)
system2(
  "R",
  args = c("CMD", "INSTALL", "--no-multiarch", "--with-keep.source", 
           "d:/Github/seedhash/R"),
  stdout = TRUE,
  stderr = TRUE
)

cat("\n✓ Installation complete!\n\n")

# Load and test
cat("Loading package...\n")
library(seedhash)

cat("✓ Package loaded successfully!\n\n")

# Test it
cat("Creating generator for 'experiment_1'...\n")
gen <- SeedHashGenerator$new("experiment_1")

cat("Generating 5 seeds...\n")
seeds <- gen$generate_seeds(5)

cat("\n✅ Results:\n")
print(seeds)

cat("\n")
print(gen)

cat("\n✅ Installation and testing complete!\n")
