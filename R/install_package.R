# Alternative Installation Methods for seedhash R Package

cat("╔════════════════════════════════════════════════════════╗\n")
cat("║  seedhash R Package - Installation Guide              ║\n")
cat("╚════════════════════════════════════════════════════════╝\n\n")

# Method 1: Install from GitHub (if pushed)
cat("Method 1: Install from GitHub\n")
cat("─────────────────────────────────────────────────────────\n")
cat("Attempting GitHub installation...\n\n")

tryCatch({
  # Make sure devtools is installed
  if (!require("devtools", quietly = TRUE)) {
    install.packages("devtools")
  }
  
  # Try installing from GitHub
  devtools::install_github("melhzy/seedhash", subdir = "R", force = TRUE)
  cat("✓ Successfully installed from GitHub!\n\n")
  
  # Test the installation
  library(seedhash)
  gen <- SeedHashGenerator$new("test")
  cat("✓ Package loaded and working!\n\n")
  
}, error = function(e) {
  cat("✗ GitHub installation failed:", e$message, "\n\n")
  cat("This may be because:\n")
  cat("  1. Repository is private\n")
  cat("  2. Package not yet synced on GitHub\n")
  cat("  3. Network issues\n\n")
  cat("Trying alternative methods...\n\n")
})

# Method 2: Install from local source
cat("Method 2: Install from Local Source\n")
cat("─────────────────────────────────────────────────────────\n")

local_path <- "d:/Github/seedhash/R"
if (dir.exists(local_path)) {
  cat("Installing from:", local_path, "\n")
  
  tryCatch({
    devtools::install(local_path)
    cat("✓ Successfully installed from local source!\n\n")
    
    # Test the installation
    library(seedhash)
    gen <- SeedHashGenerator$new("test")
    seeds <- gen$generate_seeds(5)
    cat("✓ Package working! Generated seeds:", paste(seeds, collapse = ", "), "\n\n")
    
  }, error = function(e) {
    cat("✗ Local installation failed:", e$message, "\n\n")
  })
} else {
  cat("✗ Local path not found\n\n")
}

# Method 3: Install from built package
cat("Method 3: Install from Built Package (.tar.gz)\n")
cat("─────────────────────────────────────────────────────────\n")

pkg_file <- "d:/Github/seedhash/seedhash_0.1.0.tar.gz"
if (file.exists(pkg_file)) {
  cat("Installing from:", pkg_file, "\n")
  
  tryCatch({
    install.packages(pkg_file, repos = NULL, type = "source")
    cat("✓ Successfully installed from .tar.gz!\n\n")
    
    # Test the installation
    library(seedhash)
    gen <- SeedHashGenerator$new("test")
    seeds <- gen$generate_seeds(5)
    cat("✓ Package working! Generated seeds:", paste(seeds, collapse = ", "), "\n\n")
    
  }, error = function(e) {
    cat("✗ .tar.gz installation failed:", e$message, "\n\n")
  })
} else {
  cat("✗ .tar.gz file not found\n\n")
}

# Method 4: Load directly without installation (for development)
cat("Method 4: Load Directly (Development Mode)\n")
cat("─────────────────────────────────────────────────────────\n")

if (dir.exists(local_path)) {
  cat("Loading from source...\n")
  
  tryCatch({
    # Install dependencies first
    if (!require("R6", quietly = TRUE)) install.packages("R6")
    if (!require("digest", quietly = TRUE)) install.packages("digest")
    
    # Source the main file
    source(file.path(local_path, "R", "seedhash.R"))
    
    cat("✓ Loaded successfully!\n\n")
    
    # Test it
    gen <- SeedHashGenerator$new("test")
    seeds <- gen$generate_seeds(5)
    cat("✓ Working! Generated seeds:", paste(seeds, collapse = ", "), "\n\n")
    
  }, error = function(e) {
    cat("✗ Direct loading failed:", e$message, "\n\n")
  })
}

cat("╔════════════════════════════════════════════════════════╗\n")
cat("║  Installation Complete - Try Using the Package        ║\n")
cat("╚════════════════════════════════════════════════════════╝\n\n")

cat("Quick Test:\n")
cat("──────────\n")
cat("library(seedhash)  # or just use it if loaded\n")
cat("gen <- SeedHashGenerator$new('MyProject')\n")
cat("seeds <- gen$generate_seeds(10)\n")
cat("print(seeds)\n\n")

cat("For GitHub installation to work:\n")
cat("1. Ensure repository is public\n")
cat("2. Wait a few minutes for GitHub to sync\n")
cat("3. Use: devtools::install_github('melhzy/seedhash', subdir = 'R')\n")
