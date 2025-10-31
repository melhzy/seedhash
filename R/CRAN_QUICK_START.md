# CRAN Submission Quick Reference

## 🚀 Quick Commands

```r
# Navigate to package
setwd("d:/Github/seedhash/R")

# 1. Update documentation
devtools::document()

# 2. Check locally (MUST PASS with 0 errors, 0 warnings, 0 notes)
devtools::check()

# 3. Check on Windows
devtools::check_win_devel()
devtools::check_win_release()

# 4. Check on other platforms
rhub::check_for_cran()

# 5. Build package
devtools::build()

# 6. Submit
# Go to: https://cran.r-project.org/submit.html
# Upload: seedhash_0.1.0.tar.gz
```

## ⚠️ CRITICAL: Before Submitting

1. **Update your email in DESCRIPTION**
   - Current: `your.email@example.com`
   - Replace with: Your actual email address

2. **Verify all checks pass**
   - 0 errors
   - 0 warnings  
   - 0 notes

3. **Test on multiple platforms**
   - Windows (win-builder)
   - Linux (R-hub)
   - macOS (R-hub)

## 📋 Files Created for CRAN

✅ `DESCRIPTION` - Updated with proper format, R6 dependency, URLs  
✅ `LICENSE` - MIT license file  
✅ `NEWS.md` - Version changelog  
✅ `cran-comments.md` - Submission notes  
✅ `CRAN_SUBMISSION.md` - Complete submission guide  
✅ `.Rbuildignore` - Build exclusions  
✅ `prepare_cran_submission.R` - Automated checks script  

## 📝 What You Need to Do

### 1. Update Email (REQUIRED)
Edit `DESCRIPTION` file:
```r
Authors@R: person("melhzy", email = "YOUR_REAL_EMAIL@example.com", 
                  role = c("aut", "cre"))
```

### 2. Run Preparation Script
```r
source("prepare_cran_submission.R")
```

This will:
- Validate DESCRIPTION
- Update documentation
- Run R CMD check
- Show checklist

### 3. Fix Any Issues
If checks fail, fix errors/warnings/notes and rerun.

### 4. Platform Testing
```r
# Test on Windows servers
devtools::check_win_devel()   # ~10-20 min, results via email
devtools::check_win_release() # ~10-20 min, results via email

# Test on multiple platforms
rhub::check_for_cran()         # ~20-30 min, results via email
```

### 5. Build Package
```r
devtools::build()
# Creates: seedhash_0.1.0.tar.gz
```

### 6. Final Check on Built Package
```r
rcmdcheck::rcmdcheck("seedhash_0.1.0.tar.gz", args = "--as-cran")
```

### 7. Submit to CRAN
- Go to: https://cran.r-project.org/submit.html
- Upload `seedhash_0.1.0.tar.gz`
- Optionally upload `cran-comments.md`
- Fill out form
- Submit

### 8. Confirm Submission
- Check your email
- Click confirmation link (within 24 hours)

## 🎯 Common CRAN Requirements

| Requirement | Status | Notes |
|-------------|--------|-------|
| Valid DESCRIPTION | ✅ | Updated with proper format |
| LICENSE file | ✅ | MIT license added |
| All dependencies listed | ✅ | R6, digest in Imports |
| 0 errors | ⏳ | Run checks to verify |
| 0 warnings | ⏳ | Run checks to verify |
| 0 notes | ⏳ | Run checks to verify |
| Valid email | ⚠️ | **YOU NEED TO UPDATE** |
| Documentation complete | ✅ | All functions documented |
| Examples work | ✅ | Tested in package |
| NEWS.md | ✅ | Created |
| Tested on multiple platforms | ⏳ | Run win-builder & rhub |

## ⏱️ Timeline

1. **Preparation**: 1-2 hours (fixing any check issues)
2. **Platform tests**: 30-60 minutes (automated, wait for email)
3. **Submission**: 5 minutes (web form)
4. **CRAN automated checks**: ~30 minutes
5. **Manual review**: 1-7 days (typically 2-3 days)
6. **Response required**: Confirm via email within 24 hours
7. **Publication**: Within 24 hours of acceptance

## 🔧 Troubleshooting

### "Object not found" errors
```r
# Regenerate documentation
devtools::document()
```

### "Dependency not available"
```r
# Install missing packages
install.packages(c("R6", "digest"))
```

### "Examples fail"
```r
# Test examples manually
example(SeedHashGenerator)
```

### "Notes about package size"
Usually acceptable if < 5MB

### "Possibly mis-spelled words"
Add to spell-check exceptions or fix spelling

## 📞 Getting Help

- **CRAN Policies**: https://cran.r-project.org/web/packages/policies.html
- **R Packages Book**: https://r-pkgs.org/
- **Stack Overflow**: Tag with `[r]` and `[cran]`
- **R-package-devel mailing list**: For complex questions

## 🎉 After Acceptance

1. Package appears on CRAN within 24 hours
2. Update GitHub with CRAN badge
3. Announce on social media/blog
4. Monitor for any user issues

## 📊 CRAN Submission Workflow

```
Prepare Package
      ↓
Run devtools::check() → Fix issues → Recheck
      ↓
Test on win-builder → Review results
      ↓
Test on R-hub → Review results  
      ↓
Build package (.tar.gz)
      ↓
Submit to CRAN (web form)
      ↓
Confirm via email (within 24h)
      ↓
Wait for review (1-7 days)
      ↓
Fix issues if requested → Resubmit
      ↓
Package published! 🎉
```

## 💡 Pro Tips

1. **First submission takes longer** - Be patient
2. **Read reviewer comments carefully** - They're helping you
3. **Test thoroughly** - Saves resubmission time
4. **Keep description concise** - 2-3 sentences max
5. **Minimize dependencies** - Fewer dependencies = easier maintenance
6. **Respond quickly** - CRAN reviewers appreciate prompt responses
7. **Update only when needed** - Don't spam CRAN with minor updates

## Ready to Submit?

Run this final checklist:

```r
setwd("d:/Github/seedhash/R")

# 1. Email updated?
cat("Email in DESCRIPTION:", desc::desc_get_author(), "\n")

# 2. All checks pass?
devtools::check()

# 3. Built successfully?
devtools::build()

# If all YES → Submit at: https://cran.r-project.org/submit.html
```

Good luck! 🍀
