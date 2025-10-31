# CRAN Check Script - Run this to prepare for CRAN submission
# Working directory: d:/Github/seedhash/R

cat("==================================================\n")
cat("  CRAN Submission Check for seedhash Package\n")
cat("==================================================\n\n")

# Set working directory
setwd("d:/Github/seedhash/R")

# Step 1: Load required packages
cat("Step 1: Loading required packages...\n")
required_packages <- c("devtools", "roxygen2", "rcmdcheck")
missing_packages <- required_packages[!sapply(required_packages, requireNamespace, quietly = TRUE)]

if (length(missing_packages) > 0) {
  cat("Installing missing packages:", paste(missing_packages, collapse = ", "), "\n")
  install.packages(missing_packages)
}

library(devtools)
library(roxygen2)
library(rcmdcheck)

cat("✓ All required packages loaded\n\n")

# Step 2: Update documentation with roxygen2
cat("Step 2: Regenerating documentation...\n")
tryCatch({
  devtools::document()
  cat("✓ Documentation regenerated successfully\n\n")
}, error = function(e) {
  cat("✗ Error generating documentation:", e$message, "\n\n")
})

# Step 3: Run R CMD check
cat("Step 3: Running R CMD check (this may take 2-5 minutes)...\n")
cat("-------------------------------------------------------\n\n")

check_results <- rcmdcheck::rcmdcheck(args = c("--as-cran"), error_on = "never")

# Step 4: Display results
cat("\n==================================================\n")
cat("  CHECK RESULTS SUMMARY\n")
cat("==================================================\n\n")

cat("Errors:  ", length(check_results$errors), "\n")
cat("Warnings:", length(check_results$warnings), "\n")
cat("Notes:   ", length(check_results$notes), "\n\n")

# Show details if there are issues
if (length(check_results$errors) > 0) {
  cat("\n=== ERRORS (MUST FIX) ===\n")
  for (i in seq_along(check_results$errors)) {
    cat("\nError", i, ":\n")
    cat(check_results$errors[[i]], "\n")
  }
}

if (length(check_results$warnings) > 0) {
  cat("\n=== WARNINGS (SHOULD FIX) ===\n")
  for (i in seq_along(check_results$warnings)) {
    cat("\nWarning", i, ":\n")
    cat(check_results$warnings[[i]], "\n")
  }
}

if (length(check_results$notes) > 0) {
  cat("\n=== NOTES (REVIEW) ===\n")
  for (i in seq_along(check_results$notes)) {
    cat("\nNote", i, ":\n")
    cat(check_results$notes[[i]], "\n")
  }
}

# Step 5: Provide guidance
cat("\n==================================================\n")
cat("  NEXT STEPS\n")
cat("==================================================\n\n")

if (length(check_results$errors) == 0 && 
    length(check_results$warnings) == 0 && 
    length(check_results$notes) <= 1) {
  
  cat("✓ PACKAGE IS READY FOR CRAN SUBMISSION!\n\n")
  cat("Next steps:\n")
  cat("1. Test on win-builder:\n")
  cat("   devtools::check_win_devel()\n")
  cat("   devtools::check_win_release()\n\n")
  cat("2. Build package:\n")
  cat("   devtools::build()\n\n")
  cat("3. Submit to CRAN:\n")
  cat("   https://cran.r-project.org/submit.html\n\n")
  
} else {
  cat("⚠ ISSUES FOUND - Please fix before submission:\n\n")
  
  if (length(check_results$errors) > 0) {
    cat("• Fix all", length(check_results$errors), "error(s)\n")
  }
  if (length(check_results$warnings) > 0) {
    cat("• Fix all", length(check_results$warnings), "warning(s)\n")
  }
  if (length(check_results$notes) > 1) {
    cat("• Review and address", length(check_results$notes), "note(s)\n")
  }
  
  cat("\nAfter fixing issues, run this script again.\n\n")
}

cat("For detailed guidance, see: CRAN_SUBMISSION.md\n")
cat("==================================================\n")
