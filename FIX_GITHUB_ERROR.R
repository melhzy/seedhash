# FIX: GitHub API Download Error
# The repository is public but devtools has issues with the download

# ═══════════════════════════════════════════════════════════════
# SOLUTION 1: Clear PAT and retry (RECOMMENDED)
# ═══════════════════════════════════════════════════════════════

# The PAT from git credential store may be expired or invalid
# Try without it:

Sys.unsetenv("GITHUB_PAT")
gitcreds::gitcreds_delete()  # Clear stored credentials

# Now try again
devtools::install_github("melhzy/seedhash", subdir = "R")


# ═══════════════════════════════════════════════════════════════
# SOLUTION 2: Use remotes package instead
# ═══════════════════════════════════════════════════════════════

if (!require("remotes")) install.packages("remotes")
remotes::install_github("melhzy/seedhash", subdir = "R")


# ═══════════════════════════════════════════════════════════════
# SOLUTION 3: Direct download and install
# ═══════════════════════════════════════════════════════════════

# Download the repository manually
download.file(
  "https://github.com/melhzy/seedhash/archive/refs/heads/main.zip",
  destfile = "seedhash.zip"
)

# Extract and install
unzip("seedhash.zip")
devtools::install("seedhash-main/R")

# Clean up
file.remove("seedhash.zip")
unlink("seedhash-main", recursive = TRUE)


# ═══════════════════════════════════════════════════════════════
# SOLUTION 4: Just use local path (EASIEST!)
# ═══════════════════════════════════════════════════════════════

# Since you have the code locally, this is simplest:
devtools::install("d:/Github/seedhash/R")

library(seedhash)
gen <- SeedHashGenerator$new("experiment_1")
print(gen$generate_seeds(5))

cat("\n✅ Package installed and working!\n")
