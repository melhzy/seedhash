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
