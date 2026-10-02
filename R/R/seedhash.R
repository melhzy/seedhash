#' SeedHash Generator
#'
#' Generate deterministic random seeds from string input using MD5 hashing.
#' This class allows users to generate reproducible sequences of random numbers
#' by hashing an input string and using it as a seed for R's random number generator.
#'
#' The seed number is the MD5 digest of the UTF-8 encoded input string modulo
#' 2^32, the same algorithm the Python package uses, so a given string has the
#' same \code{seed_number} in both languages. The seeds returned by
#' \code{generate_seeds()} come from R's own random number generator and
#' therefore differ from the ones the Python package returns.
#'
#' \code{generate_seeds()} always uses the Mersenne-Twister generator with the
#' "Rejection" sampler, whatever \code{RNGkind()} is set to, and restores the
#' caller's random number generator state before returning.
#'
#' @examples
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
#'
#' @importFrom R6 R6Class
#' @importFrom digest digest
#' @export
SeedHashGenerator <- R6::R6Class(
  "SeedHashGenerator",

  public = list(
    #' @description
    #' Initialize the SeedHashGenerator
    #' @param input_string The string to hash for seed generation
    #' @param min_value Minimum value for random number range, inclusive (default: 0)
    #' @param max_value Maximum value for random number range, inclusive (default: 2^31 - 1)
    #' @return A new SeedHashGenerator object
    initialize = function(input_string,
                          min_value = 0,
                          max_value = 2^31 - 1) {
      # Validate input_string
      if (!is.character(input_string) || length(input_string) != 1 ||
          is.na(input_string)) {
        stop("input_string must be a single character string")
      }

      if (nchar(input_string) == 0) {
        stop("input_string cannot be empty")
      }

      # Validate range BEFORE converting to integer
      private$check_bound(min_value, "min_value")
      private$check_bound(max_value, "max_value")

      if (min_value >= max_value) {
        stop(sprintf("min_value (%.0f) must be less than max_value (%.0f)",
                     min_value, max_value))
      }

      private$.input_string <- input_string
      private$.min_value <- as.integer(min_value)
      private$.max_value <- as.integer(max_value)

      # Hash the UTF-8 bytes, as Python's input_string.encode('utf-8') does
      private$.hash <- digest::digest(enc2utf8(input_string), algo = "md5",
                                      serialize = FALSE)
      private$.seed_number <- private$hash_to_seed(private$.hash)
    },

    #' @description
    #' Generate a list of random seed numbers
    #' @param count The number of random seeds to generate
    #' @return An integer vector of random seeds within the specified range
    generate_seeds = function(count) {
      if (!is.numeric(count) || length(count) != 1 || !is.finite(count) ||
          count != round(count) || count <= 0) {
        stop("count must be a single positive integer")
      }

      if (count > .Machine$integer.max) {
        stop("count must be at most ", .Machine$integer.max)
      }

      private$with_seed({
        # Work in doubles: the range can hold up to 2^32 - 1 values, and
        # min_value + draw can overflow R's integer type
        range_size <- as.numeric(private$.max_value) - private$.min_value + 1
        draws <- sample.int(range_size, size = count, replace = TRUE)
        as.integer(draws - 1 + private$.min_value)
      })
    },

    #' @description
    #' Seed R's random number generator from the input string, the R
    #' counterpart of Python's \code{set_seed("python")}. Use this instead of
    #' \code{set.seed(seed_number)}: \code{seed_number} can exceed R's integer
    #' range, which \code{set.seed()} rejects, so it is first reinterpreted as
    #' a signed 32-bit integer. The current \code{RNGkind()} is kept.
    #' @return The generator, invisibly
    set_seed = function() {
      set.seed(private$rng_seed())
      invisible(self)
    },

    #' @description
    #' Get the MD5 hash of the input string
    #' @return The MD5 hash as a hexadecimal string
    get_hash = function() {
      return(private$.hash)
    },

    #' @description
    #' Print method for SeedHashGenerator
    #' @param ... Additional arguments (unused)
    print = function(...) {
      cat("SeedHashGenerator:\n")
      cat(sprintf("  Input String: '%s'\n", private$.input_string))
      cat(sprintf("  Range: [%d, %d]\n", private$.min_value, private$.max_value))
      cat(sprintf("  Seed Number: %.0f\n", private$.seed_number))
      cat(sprintf("  MD5 Hash: %s\n", private$.hash))
      invisible(self)
    }
  ),

  active = list(
    #' @field input_string The input string for seed generation (read-only)
    input_string = function(value) {
      if (!missing(value)) stop("input_string is read-only", call. = FALSE)
      private$.input_string
    },

    #' @field min_value Minimum value for random number range, inclusive (read-only)
    min_value = function(value) {
      if (!missing(value)) stop("min_value is read-only", call. = FALSE)
      private$.min_value
    },

    #' @field max_value Maximum value for random number range, inclusive (read-only)
    max_value = function(value) {
      if (!missing(value)) stop("max_value is read-only", call. = FALSE)
      private$.max_value
    },

    #' @field seed_number The seed derived from hashing, a whole number in
    #' [0, 2^32 - 1] stored as a double because it can exceed R's integer
    #' range (read-only)
    seed_number = function(value) {
      if (!missing(value)) stop("seed_number is read-only", call. = FALSE)
      private$.seed_number
    }
  ),

  private = list(
    .input_string = NULL,
    .min_value = NULL,
    .max_value = NULL,
    .hash = NULL,
    .seed_number = NULL,

    # Stop unless value is a single whole number that R can store as an
    # integer. -2^31 is excluded because as.integer(-2^31) is NA in R.
    check_bound = function(value, name) {
      if (!is.numeric(value) || length(value) != 1 || !is.finite(value) ||
          value != round(value)) {
        stop(sprintf("%s must be a single whole number", name))
      }

      if (abs(value) > .Machine$integer.max) {
        stop(sprintf("%s (%.0f) is outside R's integer range [%d, %d]",
                     name, value, -.Machine$integer.max, .Machine$integer.max))
      }
    },

    # The last 8 hex digits of the digest are the digest modulo 2^32, which is
    # how the Python package derives its seed. The value can exceed R's integer
    # range, so it is assembled from two 16-bit halves as a double.
    hash_to_seed = function(hash) {
      high <- strtoi(substr(hash, 25, 28), base = 16L)
      low <- strtoi(substr(hash, 29, 32), base = 16L)
      high * 65536 + low
    },

    # set.seed() needs a value in R's integer range, so reinterpret the
    # unsigned 32-bit seed as a signed one. The single seed 2^31 would become
    # -2^31, which R cannot represent as an integer, so it is mapped to 0.
    rng_seed = function() {
      seed <- private$.seed_number
      if (seed >= 2^31) seed <- seed - 2^32
      if (seed == -2^31) seed <- 0
      as.integer(seed)
    },

    # Evaluate code with the RNG seeded from the hash, then restore the
    # caller's RNG kind and state so their own random stream is unaffected
    with_seed = function(code) {
      env <- globalenv()
      old_kind <- RNGkind()
      old_seed <- if (exists(".Random.seed", envir = env, inherits = FALSE)) {
        get(".Random.seed", envir = env, inherits = FALSE)
      }
      on.exit({
        # Restoring the "Rounding" sampler kind warns; that is the caller's choice
        suppressWarnings(RNGkind(old_kind[1], old_kind[2], old_kind[3]))
        if (is.null(old_seed)) {
          rm(".Random.seed", envir = env)
        } else {
          assign(".Random.seed", old_seed, envir = env)
        }
      })

      set.seed(private$rng_seed(), kind = "Mersenne-Twister",
               normal.kind = "Inversion", sample.kind = "Rejection")
      code
    }
  )
)

#' Create a SeedHash Generator (Convenience Function)
#'
#' This is a convenience function to create a SeedHashGenerator object.
#'
#' @param input_string The string to hash for seed generation
#' @param min_value Minimum value for random number range, inclusive (default: 0)
#' @param max_value Maximum value for random number range, inclusive (default: 2^31 - 1)
#' @return A new SeedHashGenerator object
#'
#' @examples
#' gen <- create_seedhash("Shalini")
#' seeds <- gen$generate_seeds(10)
#'
#' @export
create_seedhash <- function(input_string, min_value = 0, max_value = 2^31 - 1) {
  SeedHashGenerator$new(input_string, min_value, max_value)
}
