# seedhash (development version)

## Breaking changes

* `seed_number` is now the MD5 digest of the UTF-8 encoded input modulo 2^32,
  the same value the Python package produces. It is stored as a double because
  it can exceed R's integer range. Seeds from `generate_seeds()` therefore
  differ from version 0.1.0.
* `SeedHashGenerator$new()` now defaults to the range 0 to 2^31 - 1, like
  `create_seedhash()` and the Python package (it was -1e9 to 1e9).
* `input_string`, `min_value`, `max_value` and `seed_number` are read-only.
* Requires R >= 3.6.0.

## New features

* `set_seed()` seeds R's random number generator from the input string, like
  Python's `set_seed("python")`. Use it instead of `set.seed(gen$seed_number)`,
  which fails when `seed_number` exceeds R's integer range.

## Bug fixes

* `create_seedhash()` with its default range no longer fails in
  `generate_seeds()`; ranges up to the full integer range now work.
* `generate_seeds()` no longer returns NA from integer overflow near
  2^31 - 1, and returns an integer vector.
* `generate_seeds()` no longer depends on `RNGkind()` and restores the caller's
  random number generator state.
* Non-ASCII input is hashed as UTF-8 on every platform.
* Non-whole, NA, length > 1 and -2^31 bounds and counts are rejected with
  clear errors.

# seedhash 0.1.0

## Initial Release

* Initial CRAN release of seedhash
* Deterministic seed generation from string inputs using MD5 hashing
* R6 class-based API with `SeedHashGenerator` class
* Key features:
  - Generate reproducible random seeds from text strings
  - Customizable random number ranges (min_value, max_value)
  - Comprehensive error handling and input validation
  - MD5 hash access via `get_hash()` method
  - Convenience function `create_seedhash()` for quick initialization
* Compatible with R >= 3.5.0
* Dependencies: digest, R6
* Includes comprehensive documentation and examples
* Full test suite included
