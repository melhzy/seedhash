#' SeedHash Generator
#'
#' Generate deterministic random seeds from string input using MD5 hashing.
#' This class allows users to generate reproducible sequences of random numbers
#' by hashing an input string and using it as a seed for R's random number generator.
#'
#' @examples
#' \donttest{
#' # Create a generator with default range
#' gen <- SeedHashGenerator$new("Shalini")
#' 
#' # Generate 10 random seeds
#' seeds <- gen$generate_seeds(10)
#' print(seeds)
#' 
#' # Create a generator with custom range
#' gen_custom <- SeedHashGenerator$new("MyProject", min_value = 1, max_value = 100)
#' seeds_custom <- gen_custom$generate_seeds(5)
#' print(seeds_custom)
#' 
#' # Get the MD5 hash
#' hash_value <- gen$get_hash()
#' print(hash_value)
#' }
#'
#' @export
SeedHashGenerator <- R6::R6Class(
  "SeedHashGenerator",
  
  public = list(
    #' @description The input string for seed generation
    input_string = NULL,
    
    #' @description Minimum value for random number range
    min_value = NULL,
    
    #' @description Maximum value for random number range
    max_value = NULL,
    
    #' @description The integer seed derived from hashing
    seed_number = NULL,
    
    #' @description
    #' Initialize the SeedHashGenerator
    #' @param input_string The string to hash for seed generation
    #' @param min_value Minimum value for random number range (default: -1e9)
    #' @param max_value Maximum value for random number range (default: 1e9)
    #' @return A new SeedHashGenerator object
    initialize = function(input_string, 
                         min_value = -1e9, 
                         max_value = 1e9) {
      # Validate input_string
      if (!is.character(input_string) || length(input_string) != 1) {
        stop("input_string must be a single character string")
      }
      
      if (nchar(input_string) == 0) {
        stop("input_string cannot be empty")
      }
      
      self$input_string <- input_string
      
      # Validate range BEFORE converting to integer
      if (!is.numeric(min_value) || !is.numeric(max_value)) {
        stop("min_value and max_value must be numeric")
      }
      
      if (min_value >= max_value) {
        stop(sprintf("min_value (%.0f) must be less than max_value (%.0f)",
                    min_value, max_value))
      }
      
      # Check if values are within R's integer range
      max_int <- 2^31 - 1
      min_int <- -2^31
      
      if (min_value < min_int || min_value > max_int) {
        stop(sprintf("min_value (%.0f) is outside R's integer range [%d, %d]. Use values between -2,147,483,648 and 2,147,483,647",
                    min_value, min_int, max_int))
      }
      
      if (max_value < min_int || max_value > max_int) {
        stop(sprintf("max_value (%.0f) is outside R's integer range [%d, %d]. Use values between -2,147,483,648 and 2,147,483,647",
                    max_value, min_int, max_int))
      }
      
      # Now safe to convert to integer
      self$min_value <- as.integer(min_value)
      self$max_value <- as.integer(max_value)
      
      # Generate the seed from the input string
      self$seed_number <- private$generate_seed()
    },
    
    #' @description
    #' Generate a list of random seed numbers
    #' @param count The number of random seeds to generate
    #' @return A vector of random integers within the specified range
    generate_seeds = function(count) {
      if (!is.numeric(count) || length(count) != 1) {
        stop("count must be a single numeric value")
      }
      
      count <- as.integer(count)
      
      if (count <= 0) {
        stop("count must be a positive integer")
      }
      
      # Set the random seed
      set.seed(self$seed_number)
      
      # Generate random numbers
      # Calculate range size - handle potential integer overflow
      range_size <- as.numeric(self$max_value) - as.numeric(self$min_value) + 1
      
      # Check if range is too large for sample.int
      if (range_size > .Machine$integer.max) {
        stop("Range is too large. Maximum range size is ", .Machine$integer.max)
      }
      
      random_numbers <- sample.int(
        n = as.integer(range_size),
        size = count,
        replace = TRUE
      ) + self$min_value - 1
      
      return(random_numbers)
    },
    
    #' @description
    #' Get the MD5 hash of the input string
    #' @return The MD5 hash as a hexadecimal string
    get_hash = function() {
      return(digest::digest(self$input_string, algo = "md5", serialize = FALSE))
    },
    
    #' @description
    #' Print method for SeedHashGenerator
    #' @param ... Additional arguments (unused)
    print = function(...) {
      cat(sprintf("SeedHashGenerator:\n"))
      cat(sprintf("  Input String: '%s'\n", self$input_string))
      cat(sprintf("  Range: [%d, %d]\n", self$min_value, self$max_value))
      cat(sprintf("  Seed Number: %d\n", self$seed_number))
      cat(sprintf("  MD5 Hash: %s\n", self$get_hash()))
      invisible(self)
    }
  ),
  
  private = list(
    # Generate an integer seed from the input string using MD5 hashing
    # Returns an integer representation of the MD5 hash
    generate_seed = function() {
      # Get MD5 hash
      hash_value <- digest::digest(self$input_string, algo = "md5", serialize = FALSE)
      
      # Convert hexadecimal to integer
      # R's integer range is smaller than Python's, so we'll use modulo to fit
      # Convert first 8 hex characters to avoid overflow
      seed <- strtoi(substr(hash_value, 1, 8), base = 16)
      
      return(seed)
    }
  )
)

#' Create a SeedHash Generator (Convenience Function)
#'
#' This is a convenience function to create a SeedHashGenerator object.
#'
#' @param input_string The string to hash for seed generation
#' @param min_value Minimum value for random number range (default: 0)
#' @param max_value Maximum value for random number range (default: 2^31 - 1)
#' @return A new SeedHashGenerator object
#' 
#' @examples
#' \dontrun{
#' gen <- create_seedhash("Shalini")
#' seeds <- gen$generate_seeds(10)
#' }
#' 
#' @export
create_seedhash <- function(input_string, min_value = 0, max_value = 2^31 - 1) {
  SeedHashGenerator$new(input_string, min_value, max_value)
}
