# Contributing to SeedHash

Thank you for your interest in contributing to SeedHash! We welcome contributions from the community, whether it's bug reports, feature requests, documentation improvements, or code contributions.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

This project adheres to a Code of Conduct (see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the [issue tracker](https://github.com/melhzy/seedhash/issues) to see if the problem has already been reported. If it has **and the issue is still open**, add a comment to the existing issue instead of opening a new one.

When creating a bug report, please include:

- **A clear and descriptive title**
- **Steps to reproduce** the problem
- **Expected behavior** vs. **actual behavior**
- **Code samples** that demonstrate the issue
- **Version information**: Python/R version, SeedHash version, OS
- **Error messages** and stack traces (if applicable)

**Example bug report:**

```markdown
**Title:** SeedHashGenerator raises TypeError with Unicode strings on Windows

**Description:**
When using Unicode characters in input strings on Windows, the generator raises a TypeError.

**Steps to reproduce:**
1. Install SeedHash 0.1.0 on Windows 10
2. Run: `SeedHashGenerator("experiment_ñ")`
3. Error occurs

**Expected:** Should generate a valid seed
**Actual:** TypeError: ...

**Environment:**
- OS: Windows 10
- Python: 3.9.7
- SeedHash: 0.1.0
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement request, please include:

- **A clear and descriptive title**
- **Detailed description** of the proposed enhancement
- **Use cases** that would benefit from this feature
- **Examples** of how the feature would be used
- **Alternatives considered** (if any)

### Pull Requests

We actively welcome pull requests!

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Add tests** for any new functionality
4. **Update documentation** as needed
5. **Ensure all tests pass** locally
6. **Submit a pull request** with a clear description

**Pull request checklist:**

- [ ] Code follows the project's coding standards
- [ ] Tests added for new functionality
- [ ] All tests pass locally
- [ ] Documentation updated (if applicable)
- [ ] Commit messages are clear and descriptive
- [ ] CHANGELOG.md updated (for significant changes)

## Development Setup

### Python Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/melhzy/seedhash.git
   cd seedhash
   ```

2. **Set up a virtual environment:**
   ```bash
   cd Python
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -e .
   pip install pytest pytest-cov
   ```

4. **Run tests:**
   ```bash
   pytest tests/ -v
   ```

### R Development

1. **Clone the repository** (if not already done)

2. **Install development dependencies:**
   ```r
   install.packages(c("devtools", "testthat", "roxygen2"))
   ```

3. **Load and test:**
   ```r
   devtools::load_all("R")
   devtools::test("R")
   ```

## Coding Standards

### Python

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use meaningful variable and function names
- Write docstrings for all public functions and classes (Google or NumPy style)
- Keep functions focused and modular
- Use type hints where appropriate

**Example:**

```python
def generate_seeds(self, count: int) -> List[int]:
    """Generate a list of random seed numbers.
    
    Parameters
    ----------
    count : int
        The number of random seeds to generate.
        
    Returns
    -------
    List[int]
        A list of random integers within the specified range.
        
    Raises
    ------
    TypeError
        If count is not an integer.
    ValueError
        If count is not positive.
    """
    # Implementation
```

### R

- Follow the [Tidyverse Style Guide](https://style.tidyverse.org/)
- Use roxygen2 for documentation
- Write clear, idiomatic R code
- Use R6 classes for consistency with the package design

**Example:**

```r
#' Generate random seeds
#'
#' @param count Integer. The number of random seeds to generate.
#' @return A numeric vector of random integers.
#' @export
generate_seeds <- function(count) {
  # Implementation
}
```

## Testing

All contributions must include appropriate tests.

### Python Testing

- Use `pytest` for testing
- Place tests in `Python/tests/`
- Aim for high code coverage
- Test edge cases and error conditions

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=seedhash --cov-report=html
```

### R Testing

- Use `testthat` for testing
- Place tests in `R/tests/`
- Test core functionality and edge cases

```r
# Run tests
devtools::test()

# Check package
devtools::check()
```

## Documentation

### Python Documentation

- Update docstrings for any changes to public APIs
- Update README.md for new features
- Update examples in `examples/` directory
- Update Jupyter notebooks if relevant

### R Documentation

- Update roxygen2 comments
- Run `devtools::document()` to regenerate `.Rd` files
- Update README.md and vignettes

## Community

### Getting Help

- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and general discussion

### Communication Guidelines

- Be respectful and constructive
- Stay on topic
- Help others when you can
- Follow the Code of Conduct

### Recognition

Contributors will be acknowledged in:
- The project README
- Release notes for significant contributions
- The JOSS paper (for contributions made before submission)

## Development Workflow

### Branch Naming

- `feature/description` - for new features
- `bugfix/description` - for bug fixes
- `docs/description` - for documentation updates
- `test/description` - for test additions/updates

### Commit Messages

Write clear, descriptive commit messages:

```
Add stratified sampling method to SeedSampler

- Implement stratified_random_sampling() function
- Add tests for stratification correctness
- Update documentation with usage examples
```

### Release Process

1. Update version numbers (`setup.py`, `DESCRIPTION`)
2. Update `CHANGELOG.md`
3. Create a tagged release on GitHub
4. Publish to PyPI (Python) and/or CRAN (R)
5. Update documentation

## Questions?

If you have questions about contributing, please:
1. Check existing documentation
2. Search closed issues
3. Open a new issue with the `question` label

Thank you for contributing to SeedHash! 🎉
