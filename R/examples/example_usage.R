# seedhash R Package - Example Usage
# This file demonstrates various ways to use the seedhash package

# Install required packages if not already installed
if (!require("R6")) install.packages("R6")
if (!require("digest")) install.packages("digest")

# Source the main package file (if not installed as a package)
# source("R/seedhash.R")

# Or if installed as a package:
# library(seedhash)

cat("=== Example 1: Basic Usage with Default Range ===\n")
gen <- SeedHashGenerator$new("Shalini")
seeds <- gen$generate_seeds(10)
cat("Generated seeds:", paste(seeds, collapse = ", "), "\n")
cat("MD5 Hash:", gen$get_hash(), "\n")
cat("Seed Number:", gen$seed_number, "\n\n")

cat("=== Example 2: Custom Range ===\n")
gen_custom <- SeedHashGenerator$new(
  input_string = "MyProject",
  min_value = 1,
  max_value = 100
)
seeds_custom <- gen_custom$generate_seeds(5)
cat("Generated seeds (1-100):", paste(seeds_custom, collapse = ", "), "\n\n")

cat("=== Example 3: Reproducibility ===\n")
# First run
gen1 <- SeedHashGenerator$new("experiment_001")
results1 <- gen1$generate_seeds(5)
cat("Run 1:", paste(results1, collapse = ", "), "\n")

# Second run with same input
gen2 <- SeedHashGenerator$new("experiment_001")
results2 <- gen2$generate_seeds(5)
cat("Run 2:", paste(results2, collapse = ", "), "\n")
cat("Are they identical?", identical(results1, results2), "\n\n")

cat("=== Example 4: Multiple Experiments ===\n")
experiments <- c("exp_A", "exp_B", "exp_C")
for (exp_name in experiments) {
  gen <- SeedHashGenerator$new(exp_name)
  seeds <- gen$generate_seeds(3)
  cat(sprintf("Experiment %s: %s\n", exp_name, paste(seeds, collapse = ", ")))
}
cat("\n")

cat("=== Example 5: Using Convenience Function ===\n")
gen_conv <- create_seedhash("ConvenienceTest")
seeds_conv <- gen_conv$generate_seeds(5)
cat("Seeds:", paste(seeds_conv, collapse = ", "), "\n\n")

cat("=== Example 6: Print Generator Info ===\n")
gen_info <- SeedHashGenerator$new("InfoTest", min_value = 0, max_value = 1000)
print(gen_info)
cat("\n")

cat("=== Example 7: Error Handling ===\n")
cat("Testing empty string:\n")
tryCatch(
  SeedHashGenerator$new(""),
  error = function(e) cat("  Error:", e$message, "\n")
)

cat("Testing invalid range:\n")
tryCatch(
  SeedHashGenerator$new("test", min_value = 100, max_value = 10),
  error = function(e) cat("  Error:", e$message, "\n")
)

cat("Testing invalid count:\n")
gen_err <- SeedHashGenerator$new("test")
tryCatch(
  gen_err$generate_seeds(-5),
  error = function(e) cat("  Error:", e$message, "\n")
)
cat("\n")

cat("=== Example 8: Practical Use Case - Random Sampling ===\n")
# Simulate selecting random samples from a dataset
dataset_size <- 1000
sample_size <- 10

gen_sample <- SeedHashGenerator$new(
  "dataset_v1_sample",
  min_value = 1,
  max_value = dataset_size
)

selected_indices <- gen_sample$generate_seeds(sample_size)
cat(sprintf("Selected %d random indices from dataset of size %d:\n", 
            sample_size, dataset_size))
cat("Indices:", paste(selected_indices, collapse = ", "), "\n\n")

cat("=== Example 9: Comparing Different Strings ===\n")
strings <- c("Alice", "Bob", "Charlie")
for (str in strings) {
  gen <- SeedHashGenerator$new(str)
  cat(sprintf("'%s' -> Hash: %s, Seed: %d\n", 
              str, gen$get_hash(), gen$seed_number))
}
cat("\n")

cat("=== All examples completed successfully! ===\n")
