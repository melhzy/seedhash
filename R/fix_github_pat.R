# ULTIMATE FIX: GitHub Installation Issues
# The problem: Git credential store has an invalid/expired PAT

cat("Diagnosing GitHub access issue...\n\n")

# Test 1: Check if we can access GitHub API at all
cat("Test 1: Checking GitHub API access...\n")
api_test <- tryCatch({
  req <- httr::GET("https://api.github.com/rate_limit")
  httr::status_code(req)
}, error = function(e) {
  cat("  Error:", e$message, "\n")
  0
})

if (api_test == 200) {
  cat("  ✓ GitHub API is accessible\n\n")
} else {
  cat("  ✗ Cannot reach GitHub API\n\n")
}

# Test 2: Check the PAT
cat("Test 2: Checking GitHub PAT...\n")
pat <- Sys.getenv("GITHUB_PAT")
if (pat != "") {
  cat("  Found PAT in environment\n")
  cat("  PAT starts with:", substr(pat, 1, 10), "...\n\n")
} else {
  cat("  No PAT in environment\n\n")
}

# SOLUTION: Disable problematic Git credential integration
cat("SOLUTION: Disabling git credential store integration...\n\n")

# Unset all GitHub-related environment variables
Sys.unsetenv("GITHUB_PAT")
Sys.unsetenv("GITHUB_TOKEN")

# Use direct URL download instead
cat("Installing from direct GitHub URL...\n")

temp_file <- tempfile(fileext = ".zip")
download.file(
  url = "https://github.com/melhzy/seedhash/archive/refs/heads/main.zip",
  destfile = temp_file,
  mode = "wb",
  quiet = FALSE
)

cat("Extracting...\n")
temp_dir <- tempdir()
unzip(temp_file, exdir = temp_dir)

cat("Installing...\n")
devtools::install(file.path(temp_dir, "seedhash-main", "R"), upgrade = "never")

cat("\n✅ Installation complete!\n\n")

# Test it
library(seedhash)
gen <- SeedHashGenerator$new("experiment_1")
seeds <- gen$generate_seeds(5)

cat("✅ SUCCESS!\n")
cat("Generated seeds:", paste(seeds, collapse = ", "), "\n")
print(gen)
