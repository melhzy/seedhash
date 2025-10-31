# 🔧 GitHub Installation Troubleshooting for seedhash

## ✅ Good News: Package Works Locally!

Your package **is installed and working** locally via:
- ✅ Local source installation
- ✅ Built .tar.gz installation  
- ✅ Direct loading from source

**All methods produced identical, reproducible results!**

---

## ❌ GitHub Installation Issue

**Error**: `cannot open URL 'https://api.github.com/repos/melhzy/seedhash/tarball/HEAD'`

### Possible Causes

1. **Repository Privacy**
   - The repository might be private
   - GitHub API requires authentication for private repos

2. **GitHub API Rate Limiting**
   - Exceeded API calls limit
   - Wait 1 hour and try again

3. **Network/Firewall Issues**
   - Corporate firewall blocking GitHub API
   - VPN or proxy interfering

4. **GitHub Sync Delay**
   - Recent push may not be fully synced
   - Wait 5-10 minutes

---

## 🔍 Check Repository Status

### Step 1: Verify Repository is Public

```r
# Check if you can access the repo URL
browseURL("https://github.com/melhzy/seedhash")
```

If you can't access it without logging in, the repo is private.

### Step 2: Make Repository Public (if needed)

1. Go to: https://github.com/melhzy/seedhash
2. Click **Settings**
3. Scroll to **Danger Zone**
4. Click **Change visibility** → **Make public**

---

## ✅ Working Installation Methods (Use These!)

### Method 1: Install from Local Source (RECOMMENDED)

```r
# Install devtools if needed
if (!require("devtools")) install.packages("devtools")

# Install from local directory
devtools::install("d:/Github/seedhash/R")

# Load and test
library(seedhash)
gen <- SeedHashGenerator$new("test")
print(gen$generate_seeds(5))
```

### Method 2: Install from Built Package

```r
# Install from .tar.gz file
install.packages("d:/Github/seedhash/seedhash_0.1.0.tar.gz", 
                 repos = NULL, 
                 type = "source")

# Load and test
library(seedhash)
gen <- SeedHashGenerator$new("test")
print(gen$generate_seeds(5))
```

### Method 3: Load Directly (Development)

```r
# Install dependencies
install.packages(c("R6", "digest"))

# Source the main file
source("d:/Github/seedhash/R/R/seedhash.R")

# Use immediately (no library() needed)
gen <- SeedHashGenerator$new("test")
print(gen$generate_seeds(5))
```

---

## 🔑 Fix GitHub Installation with Authentication

If repository is private, use a GitHub PAT (Personal Access Token):

### Step 1: Create GitHub PAT

1. Go to: https://github.com/settings/tokens
2. Click **Generate new token** (classic)
3. Select scopes: **repo** (full control)
4. Generate and copy the token

### Step 2: Set PAT in R

```r
# Set PAT for this session
Sys.setenv(GITHUB_PAT = "your_token_here")

# Or save permanently
usethis::edit_r_environ()
# Add line: GITHUB_PAT=your_token_here
# Save and restart R
```

### Step 3: Try Installing Again

```r
devtools::install_github("melhzy/seedhash", subdir = "R")
```

---

## 🌐 Alternative: Install After CRAN Acceptance

Once your package is accepted to CRAN (currently in submission), users can install with:

```r
# Simple CRAN installation (after acceptance)
install.packages("seedhash")
```

---

## 📦 Distribution Options

### For Users Who Can't Access GitHub

**Option 1**: Share the .tar.gz file
```r
# They install with:
install.packages("path/to/seedhash_0.1.0.tar.gz", 
                 repos = NULL, type = "source")
```

**Option 2**: Host on your own server
```r
# They install with:
install.packages("seedhash", 
                 repos = "http://yourserver.com/R/")
```

**Option 3**: Wait for CRAN
- Package currently submitted to CRAN
- Once accepted: `install.packages("seedhash")`

---

## ✅ Verification Tests

### Test 1: Check Installation

```r
# Check if package is installed
"seedhash" %in% installed.packages()[,"Package"]

# Check version
packageVersion("seedhash")

# Check location
find.package("seedhash")
```

### Test 2: Run Basic Functions

```r
library(seedhash)

# Test 1: Basic usage
gen1 <- SeedHashGenerator$new("test")
seeds1 <- gen1$generate_seeds(5)
print(seeds1)

# Test 2: Reproducibility
gen2 <- SeedHashGenerator$new("test")
seeds2 <- gen2$generate_seeds(5)
identical(seeds1, seeds2)  # Should be TRUE

# Test 3: Custom range
gen3 <- SeedHashGenerator$new("custom", min_value = 1, max_value = 100)
seeds3 <- gen3$generate_seeds(10)
all(seeds3 >= 1 & seeds3 <= 100)  # Should be TRUE

# Test 4: Get hash
hash <- gen1$get_hash()
print(hash)
```

---

## 🎯 Current Status

**Package Status**: ✅ Fully functional locally

**Installation Methods Working**:
- ✅ Local source (`devtools::install()`)
- ✅ Built package (`.tar.gz`)
- ✅ Direct source loading

**Installation Methods Not Working**:
- ❌ GitHub (`devtools::install_github()`) - API access issue

**CRAN Status**: ⏳ Submitted, waiting for win-builder results

---

## 💡 Recommended Actions

### For You (Package Maintainer)

1. **Check repository visibility** - Make public if private
2. **Wait for CRAN acceptance** - Best distribution method
3. **Use local installation** - Works perfectly for development

### For Others Wanting to Install

**Before CRAN acceptance**:
```r
# Option 1: If repo is public
devtools::install_github("melhzy/seedhash", subdir = "R")

# Option 2: From shared .tar.gz file
install.packages("seedhash_0.1.0.tar.gz", repos = NULL, type = "source")
```

**After CRAN acceptance** (in ~1 week):
```r
# Simple and recommended
install.packages("seedhash")
```

---

## 📧 Support

If GitHub installation continues to fail after making repo public:

1. **Check GitHub status**: https://www.githubstatus.com/
2. **Try again in 1 hour** (rate limit resets)
3. **Use alternative methods** above
4. **Wait for CRAN release** (easiest solution)

---

## ✨ Bottom Line

**Your package is working perfectly!** The GitHub API issue is just a convenience problem, not a functionality problem. Users can still install and use your package through multiple methods, and once it's on CRAN, this won't be an issue at all.

**Estimated CRAN availability**: 3-10 days from now
