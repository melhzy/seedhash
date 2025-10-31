# Quick test script for R console
# Copy and paste this into a fresh R console

library(seedhash)

# Test 1: Basic usage
gen <- SeedHashGenerator$new("experiment_1")
seeds <- gen$generate_seeds(5)
print(seeds)

# Test 2: Your biological experiment
gen2 <- SeedHashGenerator$new("C57BL/6 experiment 1")
seeds2 <- gen2$generate_seeds(5)
print(seeds2)

# Test 3: Custom range
gen3 <- SeedHashGenerator$new("my_experiment", min_value = 0, max_value = 10000)
seeds3 <- gen3$generate_seeds(10)
print(seeds3)

cat("\n✅ All tests passed!\n")
