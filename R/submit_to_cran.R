# Submit to CRAN - Final Steps Script
# Run this in R to complete submission

cat("\n╔══════════════════════════════════════════════════╗\n")
cat("║  CRAN Submission - Final Steps for seedhash    ║\n")
cat("╚══════════════════════════════════════════════════╝\n\n")

setwd("d:/Github/seedhash/R")

# Load required packages
library(devtools)

cat("Step 1: Building package for CRAN...\n")
cat("─────────────────────────────────────────────────\n\n")

# Build the package
pkg_file <- devtools::build(manual = TRUE)

cat("\n✓ Package built successfully!\n")
cat("  File:", pkg_file, "\n\n")

cat("Step 2: Testing on CRAN Windows builder...\n")
cat("─────────────────────────────────────────────────\n\n")

cat("Submitting to win-builder (devel)...\n")
devtools::check_win_devel()

cat("\nSubmitting to win-builder (release)...\n")
devtools::check_win_release()

cat("\n✓ Submitted to win-builder!\n")
cat("  You will receive results via email in 30-60 minutes\n")
cat("  Check email:", Sys.getenv("EMAIL"), "\n\n")

cat("Step 3: Package is ready for CRAN submission!\n")
cat("─────────────────────────────────────────────────\n\n")

cat("After win-builder tests pass, submit here:\n")
cat("  📦 https://cran.r-project.org/submit.html\n\n")

cat("Upload this file:\n")
cat("  📄", pkg_file, "\n\n")

cat("Submission details:\n")
cat("  Package: seedhash\n")
cat("  Version: 0.1.0\n")
cat("  Maintainer: melhzy <melhzy@gmail.com>\n\n")

cat("✓ IMPORTANT: Check your email and click confirmation link!\n\n")

cat("╔══════════════════════════════════════════════════╗\n")
cat("║  Wait for win-builder results before submitting ║\n")
cat("╚══════════════════════════════════════════════════╝\n")
