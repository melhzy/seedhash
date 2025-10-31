# Install seedhash using pak (modern R package installer)
# pak handles GitHub installations better than devtools

cat("Installing pak package manager...\n")
if (!require("pak", quietly = TRUE)) {
  install.packages("pak", repos = "https://r-lib.github.io/p/pak/stable/")
}

cat("\nInstalling seedhash from GitHub using pak...\n")
cat("Repository: https://github.com/melhzy/seedhash/tree/main/R\n\n")

# pak uses a simpler syntax and handles auth better
pak::pkg_install("github::melhzy/seedhash/R", ask = FALSE)

cat("\n✅ Installation complete!\n\n")

# Test it
cat("Testing installation...\n")
library(seedhash)

gen <- SeedHashGenerator$new("experiment_1")
seeds <- gen$generate_seeds(5)

cat("\n✅ Success! Generated seeds:\n")
print(seeds)
cat("\n")
print(gen)
