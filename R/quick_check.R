# Quick CRAN Check - Simplified Version
# This runs a basic check without full rcmdcheck complexity

setwd("d:/Github/seedhash/R")

cat("\n========================================\n")
cat("  Quick Package Check for CRAN\n")
cat("========================================\n\n")

# Install/load devtools
if (!require("devtools", quietly = TRUE)) {
  install.packages("devtools")
}
library(devtools)

# Step 1: Document
cat("1. Updating documentation...\n")
devtools::document()
cat("✓ Done\n\n")

# Step 2: Check
cat("2. Running devtools::check()...\n")
cat("   (This takes 2-5 minutes)\n\n")

check_result <- devtools::check(args = c("--as-cran"))

cat("\n========================================\n")
cat("  CHECK COMPLETE\n")
cat("========================================\n\n")

# The check result will print automatically
# devtools::check() prints its own summary

cat("\nIf you see 0 errors, 0 warnings, 0 notes (or 1 note about new submission):\n")
cat("✓ Package is ready for CRAN!\n\n")

cat("Next steps:\n")
cat("1. Test on win-builder: devtools::check_win_devel()\n")
cat("2. Build package: devtools::build()\n")
cat("3. Submit to CRAN: https://cran.r-project.org/submit.html\n\n")
