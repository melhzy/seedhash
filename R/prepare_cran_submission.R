# Quick Start Script for CRAN Submission
# Run this script to prepare seedhash package for CRAN submission

cat("=== seedhash CRAN Submission Preparation ===\n\n")

# Set working directory to package root
setwd("d:/Github/seedhash/R")

cat("Step 1: Installing required packages...\n")
required_packages <- c("devtools", "roxygen2", "rcmdcheck", "rhub", "desc")
for (pkg in required_packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg)
  }
}

cat("\nStep 2: Checking DESCRIPTION file...\n")
tryCatch({
  desc::desc_validate()
  cat("✓ DESCRIPTION is valid\n")
}, error = function(e) {
  cat("✗ DESCRIPTION has issues:", e$message, "\n")
})

cat("\nStep 3: Updating documentation...\n")
tryCatch({
  devtools::document()
  cat("✓ Documentation updated\n")
}, error = function(e) {
  cat("✗ Documentation error:", e$message, "\n")
})

cat("\nStep 4: Installing package locally...\n")
tryCatch({
  devtools::install()
  cat("✓ Package installed locally\n")
}, error = function(e) {
  cat("✗ Installation error:", e$message, "\n")
})

cat("\nStep 5: Running R CMD check...\n")
cat("(This may take a few minutes...)\n")
check_results <- devtools::check()

cat("\nCheck Results Summary:\n")
cat("Errors:  ", length(check_results$errors), "\n")
cat("Warnings:", length(check_results$warnings), "\n")
cat("Notes:   ", length(check_results$notes), "\n")

if (length(check_results$errors) > 0) {
  cat("\n✗ ERRORS found - must fix before submission:\n")
  print(check_results$errors)
}

if (length(check_results$warnings) > 0) {
  cat("\n⚠ WARNINGS found - should fix before submission:\n")
  print(check_results$warnings)
}

if (length(check_results$notes) > 0) {
  cat("\n⚠ NOTES found - review before submission:\n")
  print(check_results$notes)
}

cat("\n=== Pre-Submission Checklist ===\n\n")

cat("Manual checks needed:\n")
cat("[ ] Updated email address in DESCRIPTION (replace your.email@example.com)\n")
cat("[ ] LICENSE file exists and is correct\n")
cat("[ ] NEWS.md is up to date\n")
cat("[ ] cran-comments.md reflects actual test results\n")
cat("[ ] README.md is complete\n")
cat("[ ] All examples run without errors\n")
cat("[ ] Package passes R CMD check with 0 errors, 0 warnings, 0 notes\n\n")

if (length(check_results$errors) == 0 && 
    length(check_results$warnings) == 0 && 
    length(check_results$notes) == 0) {
  
  cat("✓ Package is ready for additional platform checks!\n\n")
  
  cat("Next steps:\n")
  cat("1. Run platform checks:\n")
  cat("   devtools::check_win_devel()\n")
  cat("   devtools::check_win_release()\n")
  cat("   rhub::check_for_cran()\n\n")
  cat("2. Build package:\n")
  cat("   devtools::build()\n\n")
  cat("3. Submit to CRAN:\n")
  cat("   https://cran.r-project.org/submit.html\n\n")
  
} else {
  cat("✗ Please fix all errors, warnings, and notes before proceeding.\n")
  cat("Review the output above and make necessary corrections.\n\n")
}

cat("For detailed instructions, see: CRAN_SUBMISSION.md\n")
