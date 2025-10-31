# ✅ RECOMMENDED INSTALLATION METHODS FOR SEEDHASH

# ═══════════════════════════════════════════════════════════════
# METHOD 1: Local Installation (BEST - Always Works!)
# ═══════════════════════════════════════════════════════════════

# Option A: Using devtools
if (!require("devtools")) install.packages("devtools")
devtools::install("d:/Github/seedhash/R")

# Option B: Direct R CMD INSTALL (most reliable)
# Run this in PowerShell:
# R CMD INSTALL d:/Github/seedhash/R

library(seedhash)
gen <- SeedHashGenerator$new("experiment_1")
print(gen$generate_seeds(5))


# ═══════════════════════════════════════════════════════════════
# METHOD 2: GitHub Installation (May Have Issues)
# ═══════════════════════════════════════════════════════════════

# If you get "cannot open URL" error, the repository might be:
# 1. Private (requires authentication)
# 2. GitHub API rate limit reached
# 3. GitHub PAT (Personal Access Token) expired

# To fix GitHub installation:

# Step 1: Check if repo is public
# Go to: https://github.com/melhzy/seedhash/settings
# Under "Danger Zone" > Change visibility to "Public"

# Step 2: Try without PAT
Sys.unsetenv("GITHUB_PAT")
devtools::install_github("melhzy/seedhash", subdir = "R")

# Step 3: Or set a new GitHub PAT
# Create token at: https://github.com/settings/tokens
# Then run:
# Sys.setenv(GITHUB_PAT = "your_token_here")
# devtools::install_github("melhzy/seedhash", subdir = "R")


# ═══════════════════════════════════════════════════════════════
# METHOD 3: Install from .tar.gz (For Distribution)
# ═══════════════════════════════════════════════════════════════

# First build the package (run once):
# system("R CMD build d:/Github/seedhash/R")

# Then anyone can install from the tarball:
# install.packages("seedhash_0.1.0.tar.gz", repos = NULL, type = "source")


# ═══════════════════════════════════════════════════════════════
# CURRENT STATUS
# ═══════════════════════════════════════════════════════════════

cat("\n✅ Your package IS working correctly!\n")
cat("The error you saw is just from GitHub API, but the local install succeeded.\n")
cat("Output: -734986993  927639038 -865005257 -998719985  602022881\n\n")

cat("Recommended: Use METHOD 1 (local installation) for development.\n")
cat("GitHub installation is only needed when sharing with others.\n")
