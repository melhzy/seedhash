# Force clean reinstall of seedhash package
# Run this script to fix the corruption issue

cat("Step 1: Removing all seedhash installations...\n")

# Remove from all possible library locations
lib_paths <- .libPaths()
for (lib in lib_paths) {
  pkg_path <- file.path(lib, "seedhash")
  if (dir.exists(pkg_path)) {
    cat("  Removing:", pkg_path, "\n")
    unlink(pkg_path, recursive = TRUE, force = TRUE)
  }
}

cat("\nStep 2: Installing fresh copy...\n")

# Install using R CMD INSTALL (most reliable method)
install_result <- system2(
  "R",
  args = c("CMD", "INSTALL", "--no-multiarch", "--with-keep.source", 
           "--clean", "d:/Github/seedhash/R"),
  stdout = TRUE,
  stderr = TRUE
)

cat(paste(install_result, collapse = "\n"))

cat("\n\nStep 3: Testing installation...\n")

# Detach if already loaded
if ("package:seedhash" %in% search()) {
  detach("package:seedhash", unload = TRUE)
}

# Fresh load
library(seedhash)

cat("✓ Package loaded!\n\n")

# Test
cat("Step 4: Running test...\n")
gen <- SeedHashGenerator$new("experiment_1")
seeds <- gen$generate_seeds(5)

cat("\n✅ SUCCESS! Package is working correctly.\n\n")
cat("Generated seeds:", paste(seeds, collapse = ", "), "\n")
print(gen)

cat("\n✅ You can now use library(seedhash) in your R console!\n")
