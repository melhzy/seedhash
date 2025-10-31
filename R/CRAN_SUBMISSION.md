# CRAN Submission Guide for seedhash

This guide provides step-by-step instructions for submitting the seedhash package to CRAN (Comprehensive R Archive Network).

## Prerequisites

Before submitting to CRAN, ensure you have:

1. **R** (latest version recommended)
2. **RStudio** (optional but helpful)
3. **Required R packages**:
   ```r
   install.packages(c("devtools", "roxygen2", "testthat", "rcmdcheck", "rhub"))
   ```

## Pre-Submission Checklist

### 1. Update Package Metadata

✅ **DESCRIPTION file**:
- [ ] Valid email address in `Authors@R`
- [ ] Description is clear and properly formatted (no leading/trailing whitespace)
- [ ] All dependencies listed in `Imports`
- [ ] License file exists
- [ ] URL and BugReports fields point to GitHub

✅ **Version number**: Currently `0.1.0` (appropriate for first CRAN release)

✅ **Documentation**:
- [ ] All exported functions have proper documentation
- [ ] Examples run without errors
- [ ] README.md exists

### 2. Add Required Files

Create these files if missing:

#### NEWS.md
```r
# Create NEWS.md
cat("# seedhash 0.1.0

* Initial CRAN release
* Deterministic seed generation from strings using MD5
* R6 class-based API
* Customizable random number ranges
* Comprehensive error handling
", file = "NEWS.md")
```

#### cran-comments.md
```r
# Create cran-comments.md
cat("## Test environments
* local Windows install, R 4.3.0
* win-builder (devel and release)
* R-hub (ubuntu-gcc-release)

## R CMD check results
There were no ERRORs, WARNINGs, or NOTEs.

## Downstream dependencies
There are currently no downstream dependencies for this package.
", file = "cran-comments.md")
```

### 3. Check DESCRIPTION File

**Current DESCRIPTION needs updating:**

```r
# Open R in the package directory
setwd("d:/Github/seedhash/R")

# Update email in DESCRIPTION
# Replace "your.email@example.com" with your actual email
```

**Required fields:**
- `Authors@R`: Use person() format with valid email
- `Description`: 2+ complete sentences, properly formatted
- `License`: MIT + file LICENSE (ensure LICENSE file exists)
- `Imports`: List R6 (currently missing!)

### 4. Create/Update LICENSE File

```r
# Create LICENSE file
cat("YEAR: 2025
COPYRIGHT HOLDER: melhzy
", file = "LICENSE")
```

### 5. Run R CMD Check

This is the most important step. Your package must pass with **0 errors, 0 warnings, 0 notes**.

```r
# Install required packages
install.packages(c("devtools", "rcmdcheck"))

# Set working directory to package root
setwd("d:/Github/seedhash/R")

# Run check
devtools::check()

# Or use rcmdcheck
rcmdcheck::rcmdcheck()
```

### 6. Check on Multiple Platforms

CRAN tests on multiple platforms. Use these services:

#### Win-builder (Windows)
```r
devtools::check_win_devel()  # Development version
devtools::check_win_release() # Release version
```

#### R-hub (Multiple platforms)
```r
# Check on multiple platforms
rhub::check_for_cran()

# Or specific platforms
rhub::check(platform = "ubuntu-gcc-release")
rhub::check(platform = "fedora-clang-devel")
rhub::check(platform = "macos-highsierra-release-cran")
```

### 7. Fix Common Issues

#### Issue: Missing R6 in Imports
**Fix**: Already added in updated DESCRIPTION

#### Issue: Invalid email
**Fix**: Update `Authors@R` field with real email

#### Issue: Examples fail
**Fix**: Wrap long-running examples in `\donttest{}`
```r
#' @examples
#' \donttest{
#'   gen <- SeedHashGenerator$new("test")
#'   seeds <- gen$generate_seeds(10)
#' }
```

#### Issue: No return value documented
**Fix**: Add `@return` to all functions

### 8. Build the Package

```r
# Build source package (.tar.gz)
devtools::build()

# This creates: seedhash_0.1.0.tar.gz
```

### 9. Final Checks

```r
# Check the built package
R CMD check --as-cran seedhash_0.1.0.tar.gz

# Or in R
rcmdcheck::rcmdcheck("seedhash_0.1.0.tar.gz", args = "--as-cran")
```

### 10. Submit to CRAN

#### Method 1: Web Form (Recommended for first submission)

1. Go to: https://cran.r-project.org/submit.html
2. Fill out the form:
   - Package name: `seedhash`
   - Version: `0.1.0`
   - Maintainer email: (your email from DESCRIPTION)
3. Upload `seedhash_0.1.0.tar.gz`
4. Upload `cran-comments.md` (optional but recommended)
5. Submit

#### Method 2: Using devtools
```r
devtools::submit_cran()
```

## Post-Submission Process

### What Happens Next

1. **Automated checks** (~30 minutes)
   - CRAN will run automated checks
   - You'll receive email if there are issues

2. **Manual review** (1-7 days typically)
   - CRAN maintainer reviews your package
   - May ask for changes

3. **Confirmation email**
   - You must confirm submission via email link

4. **Publication** (if accepted)
   - Package appears on CRAN
   - Usually within 24 hours of acceptance

### Common CRAN Feedback

Be prepared to address:

1. **Description field**: Must be properly formatted
2. **Examples**: Must run successfully
3. **License**: Must be standard CRAN license
4. **Dependencies**: Minimize them
5. **Title**: Should be in title case
6. **No internet access**: Examples/tests can't require internet

## Responding to CRAN

If CRAN requests changes:

1. Make the requested changes
2. Increment version (e.g., 0.1.0 → 0.1.1)
3. Update NEWS.md
4. Rerun all checks
5. Resubmit with note about changes made

Example response:
```
Thanks for the review. I have made the following changes:

* Fixed DESCRIPTION formatting
* Updated examples to use \donttest{}
* Added R6 to Imports

The package now passes R CMD check with 0 errors, 0 warnings, 0 notes.
```

## Step-by-Step Commands

Here's the complete workflow:

```r
# 1. Set working directory
setwd("d:/Github/seedhash/R")

# 2. Update documentation
devtools::document()

# 3. Install dependencies
install.packages(c("R6", "digest"))

# 4. Local check
devtools::check()

# 5. Check on Windows
devtools::check_win_devel()
devtools::check_win_release()

# 6. Check on other platforms
rhub::check_for_cran()

# 7. Build package
pkg_file <- devtools::build()

# 8. Final check on built package
rcmdcheck::rcmdcheck(pkg_file, args = "--as-cran")

# 9. Submit
devtools::submit_cran()
# Or manually at: https://cran.r-project.org/submit.html
```

## Important CRAN Policies

1. **First submission**: Be patient, may take longer
2. **Resubmission**: Wait at least 2 weeks between submissions
3. **Updates**: Only submit updates with substantial changes
4. **Maintainer**: Must respond to emails within 2 weeks
5. **Archive**: Packages may be archived if issues aren't fixed

## Helpful Resources

- **CRAN Repository Policy**: https://cran.r-project.org/web/packages/policies.html
- **Writing R Extensions**: https://cran.r-project.org/doc/manuals/r-release/R-exts.html
- **R Packages Book**: https://r-pkgs.org/
- **CRAN Submission Checklist**: https://cran.r-project.org/web/packages/submission_checklist.html

## Troubleshooting

### "Package has been archived"
- Your package was archived due to issues
- Fix issues and resubmit

### "Invalid DESCRIPTION"
- Check formatting carefully
- No leading/trailing spaces
- Proper indentation (4 spaces for continuation)

### "Examples fail"
- Wrap problematic examples in `\donttest{}`
- Ensure all examples run in < 5 seconds

### "Missing documentation"
- All exported functions need `@export` and documentation
- Run `devtools::document()` to regenerate

## Before First Submission - Complete Checklist

Run this complete check:

```r
# Complete pre-submission checklist
setwd("d:/Github/seedhash/R")

cat("1. Checking DESCRIPTION...\n")
desc::desc_validate()

cat("2. Checking documentation...\n")
devtools::document()

cat("3. Running local check...\n")
devtools::check()

cat("4. Checking spelling...\n")
devtools::spell_check()

cat("5. Building package...\n")
pkg <- devtools::build()

cat("6. Checking built package...\n")
rcmdcheck::rcmdcheck(pkg, args = "--as-cran")

cat("\nIf all checks pass, you're ready to submit!\n")
cat("Visit: https://cran.r-project.org/submit.html\n")
```

## Quick Fixes Needed for This Package

Based on current state, you need to:

1. ✅ **Update DESCRIPTION** - Add R6 to Imports (done)
2. ⚠️ **Add valid email** - Replace "your.email@example.com"
3. ⚠️ **Create LICENSE file** - Add MIT license text
4. ⚠️ **Create NEWS.md** - Document version changes
5. ⚠️ **Create cran-comments.md** - Submission notes
6. ⚠️ **Run checks** - Ensure 0 errors, warnings, notes

## Next Steps

1. Update your email in DESCRIPTION
2. Create missing files (LICENSE, NEWS.md, cran-comments.md)
3. Run `devtools::check()` and fix any issues
4. Test on win-builder and R-hub
5. Build package with `devtools::build()`
6. Submit to CRAN

Good luck with your submission! 🚀
