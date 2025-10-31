# Quick fix: Install using remotes package instead of devtools
# This often works better with GitHub API

if (!require("remotes")) {
  install.packages("remotes")
}

cat("Attempting to install from GitHub using remotes...\n\n")

# Clear any problematic PAT
Sys.unsetenv("GITHUB_PAT")

# Try with remotes
remotes::install_github("melhzy/seedhash", subdir = "R", force = TRUE)

cat("\n✅ Installation complete!\n\n")

# Test it
library(seedhash)
gen <- SeedHashGenerator$new("experiment_1")
seeds <- gen$generate_seeds(5)
cat("Generated seeds:", paste(seeds, collapse = ", "), "\n")
