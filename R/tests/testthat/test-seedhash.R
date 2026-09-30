test_that("defaults match create_seedhash() and the Python package", {
  gen <- SeedHashGenerator$new("test")
  expect_identical(gen$min_value, 0L)
  expect_identical(gen$max_value, .Machine$integer.max)

  conv <- create_seedhash("test")
  expect_identical(conv$min_value, gen$min_value)
  expect_identical(conv$max_value, gen$max_value)
})

test_that("custom range is stored as integers", {
  gen <- SeedHashGenerator$new("test", min_value = 10, max_value = 100)
  expect_identical(gen$min_value, 10L)
  expect_identical(gen$max_value, 100L)
})

test_that("input_string is validated", {
  expect_error(SeedHashGenerator$new(""), "cannot be empty")
  expect_error(SeedHashGenerator$new(NA_character_), "single character string")
  expect_error(SeedHashGenerator$new(c("a", "b")), "single character string")
  expect_error(SeedHashGenerator$new(123), "single character string")
})

test_that("range bounds are validated", {
  expect_error(SeedHashGenerator$new("test", 100, 10), "must be less than")
  expect_error(SeedHashGenerator$new("test", 5, 5), "must be less than")
  expect_error(SeedHashGenerator$new("test", 0.2, 0.8), "whole number")
  expect_error(SeedHashGenerator$new("test", NA_real_, 5), "whole number")
  expect_error(SeedHashGenerator$new("test", c(1, 2), 10), "whole number")
  expect_error(SeedHashGenerator$new("test", "0", 10), "whole number")
  expect_error(SeedHashGenerator$new("test", 0, 2^31), "outside R's integer range")
  # as.integer(-2^31) is NA in R, so -2^31 must be rejected
  expect_error(SeedHashGenerator$new("test", -2^31, 0), "outside R's integer range")
})

test_that("seed_number matches the Python package", {
  # Values from Python: int(hashlib.md5(s.encode('utf-8')).hexdigest(), 16) % 2**32
  expected <- c(
    experiment_1 = 1603554058,
    test = 640136438,
    Shalini = 52639232,
    "café" = 1930968482
  )
  for (s in names(expected)) {
    expect_identical(SeedHashGenerator$new(s)$seed_number, expected[[s]], label = s)
  }
})

test_that("non-ASCII input hashes its UTF-8 bytes whatever the declared encoding", {
  utf8 <- "café"
  latin1 <- iconv(utf8, "UTF-8", "latin1")
  expect_identical(Encoding(latin1), "latin1")
  expect_identical(
    SeedHashGenerator$new(latin1)$get_hash(),
    SeedHashGenerator$new(utf8)$get_hash()
  )
})

test_that("get_hash() returns the MD5 of the input string", {
  gen <- SeedHashGenerator$new("test")
  expect_identical(gen$get_hash(), "098f6bcd4621d373cade4e832627b4f6")
})

test_that("generate_seeds() returns reproducible integers in range", {
  gen <- SeedHashGenerator$new("range_test", min_value = 10, max_value = 20)
  seeds <- gen$generate_seeds(100)
  expect_type(seeds, "integer")
  expect_length(seeds, 100)
  expect_true(all(seeds >= 10 & seeds <= 20))
  expect_identical(
    SeedHashGenerator$new("range_test", 10, 20)$generate_seeds(100),
    seeds
  )
})

test_that("generate_seeds() output is pinned", {
  # Changing these values breaks reproducibility for existing users
  expect_identical(
    SeedHashGenerator$new("test", 1, 100)$generate_seeds(5),
    c(2L, 13L, 54L, 4L, 13L)
  )
  expect_identical(
    create_seedhash("experiment_1")$generate_seeds(3),
    c(860817984L, 1641195952L, 1260949474L)
  )
})

test_that("the default and full integer ranges can generate seeds", {
  expect_length(create_seedhash("convenience_test")$generate_seeds(5), 5)

  full <- SeedHashGenerator$new("test", -.Machine$integer.max, .Machine$integer.max)
  seeds <- full$generate_seeds(1000)
  expect_type(seeds, "integer")
  expect_false(anyNA(seeds))
})

test_that("generate_seeds() does not overflow at the top of the integer range", {
  gen <- SeedHashGenerator$new("x", 2147483600, .Machine$integer.max)
  seeds <- expect_silent(gen$generate_seeds(1000))
  expect_false(anyNA(seeds))
  expect_true(all(seeds >= 2147483600))
})

test_that("count is validated", {
  gen <- SeedHashGenerator$new("test")
  expect_error(gen$generate_seeds(-5), "positive integer")
  expect_error(gen$generate_seeds(0), "positive integer")
  expect_error(gen$generate_seeds(2.9), "positive integer")
  expect_error(gen$generate_seeds(NA_real_), "positive integer")
  expect_error(gen$generate_seeds(c(1, 2)), "positive integer")
  expect_error(gen$generate_seeds("5"), "positive integer")
  expect_error(gen$generate_seeds(3e9), "at most")
})

test_that("generate_seeds() leaves the caller's RNG state alone", {
  gen <- SeedHashGenerator$new("test")

  set.seed(42)
  expected <- runif(3)
  set.seed(42)
  first <- runif(1)
  gen$generate_seeds(3)
  expect_identical(c(first, runif(2)), expected)

  old_kind <- RNGkind()
  on.exit(suppressWarnings(RNGkind(old_kind[1], old_kind[2], old_kind[3])))
  seeds <- gen$generate_seeds(5)
  RNGkind("L'Ecuyer-CMRG")
  expect_identical(gen$generate_seeds(5), seeds)
  expect_identical(RNGkind()[1], "L'Ecuyer-CMRG")
})

test_that("generate_seeds() does not create .Random.seed", {
  env <- globalenv()
  if (exists(".Random.seed", envir = env, inherits = FALSE)) {
    saved <- get(".Random.seed", envir = env, inherits = FALSE)
    on.exit(assign(".Random.seed", saved, envir = env))
    rm(".Random.seed", envir = env)
  }
  SeedHashGenerator$new("test")$generate_seeds(1)
  expect_false(exists(".Random.seed", envir = env, inherits = FALSE))
})

test_that("seeds above R's integer range map to valid set.seed() values", {
  gen <- SeedHashGenerator$new("test")
  private <- gen$.__enclos_env__$private
  private$.seed_number <- 2^32 - 1
  expect_identical(private$rng_seed(), -1L)
  private$.seed_number <- 2^31
  expect_identical(private$rng_seed(), 0L)
  private$.seed_number <- 2^31 - 1
  expect_identical(private$rng_seed(), .Machine$integer.max)
})

test_that("set_seed() seeds R's generator even when seed_number exceeds integer range", {
  gen <- SeedHashGenerator$new("Bob")
  expect_identical(gen$seed_number, 3214761019)

  gen$set_seed()
  first <- runif(3)
  gen$set_seed()
  expect_identical(runif(3), first)

  set.seed(gen$seed_number - 2^32)
  expect_identical(runif(3), first)
})

test_that("fields are read-only", {
  gen <- SeedHashGenerator$new("test")
  expect_error(gen$input_string <- "other", "read-only")
  expect_error(gen$min_value <- 5, "read-only")
  expect_error(gen$max_value <- 5, "read-only")
  expect_error(gen$seed_number <- 5, "read-only")
})

test_that("print() shows seeds beyond R's integer range", {
  expect_output(print(SeedHashGenerator$new("experiment_1")), "Seed Number: 1603554058")
})
