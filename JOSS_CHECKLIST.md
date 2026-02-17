# JOSS Submission Checklist for SeedHash

This checklist tracks preparation for submitting SeedHash to the Journal of Open Source Software (JOSS).

## Required Files ✅

- [x] **paper.md** - JOSS paper with all required sections
- [x] **paper.bib** - BibTeX file with references
- [x] **LICENSE** - OSI-approved license (MIT)
- [x] **README.md** - Comprehensive documentation
- [x] **CONTRIBUTING.md** - Contribution guidelines
- [x] **CODE_OF_CONDUCT.md** - Community guidelines
- [x] **.zenodo.json** - Metadata for DOI archiving

## JOSS Paper Requirements ✅

The paper.md includes all required sections:

- [x] **Summary** - High-level description for diverse audience
- [x] **Statement of Need** - Clear purpose and target audience
- [x] **State of the Field** - Comparison with existing tools and justification
- [x] **Software Design** - Architectural choices and trade-offs
- [x] **Research Impact Statement** - Evidence of use or credible near-term significance
- [x] **AI Usage Disclosure** - Transparent disclosure of AI tool usage
- [x] **References** - Key citations with full venue names

## Software Requirements

### Documentation ✅

- [x] Installation instructions (Python and R)
- [x] Usage examples in README
- [x] API documentation (docstrings/roxygen2)
- [x] Jupyter tutorials (3 notebooks)
- [x] Multiple example files

### Testing ⚠️

- [x] Test files exist (`test_*.py`, `test_seedhash.R`)
- [x] CI workflow created (`.github/workflows/tests.yml`)
- [ ] **TODO**: Verify CI runs successfully on GitHub
- [ ] **TODO**: Add test coverage badge to README

### Repository Requirements ✅

- [x] OSI-approved open source license
- [x] Public GitHub repository (no registration required)
- [x] Readable issue tracker
- [x] Ability to open issues/PRs

### Development History ⚠️

According to JOSS requirements, projects need:

- [ ] **TODO**: At least 6 months of public development history
- [ ] **TODO**: Evidence of releases or version tags
- [ ] **TODO**: Public issues and/or pull requests
- [ ] **TODO**: Evidence of external engagement (optional but helpful)

**Action**: Check git history and create appropriate releases/tags.

## Before Submission Checklist

### Update paper.md

- [ ] **TODO**: Add actual ORCID for author (currently placeholder)
- [ ] **TODO**: Update affiliation if needed
- [ ] **TODO**: Add development start date in Research Impact section
- [ ] **TODO**: Add actual GitHub stars/forks statistics
- [ ] **TODO**: Verify all citations are correct

### Repository Polish

- [ ] **TODO**: Ensure all tests pass
- [ ] **TODO**: Run CI successfully
- [ ] **TODO**: Add badges to README (build status, coverage, license, etc.)
- [ ] **TODO**: Create a release version (e.g., v0.1.0)
- [ ] **TODO**: Tag the release on GitHub
- [ ] **TODO**: Verify installation from GitHub works for both Python and R

### Community Guidelines

- [x] CONTRIBUTING.md with clear guidelines
- [x] CODE_OF_CONDUCT.md
- [ ] **TODO**: Update CODE_OF_CONDUCT contact method (line marked INSERT CONTACT METHOD)

### Documentation Review

- [ ] **TODO**: Verify all links in documentation work
- [ ] **TODO**: Ensure examples run without errors
- [ ] **TODO**: Check that Jupyter notebooks execute successfully
- [ ] **TODO**: Proofread all documentation for clarity

## Submission Process

1. [ ] Complete all items above
2. [ ] Verify repository is publicly accessible
3. [ ] Ensure at least 6 months of public development history
4. [ ] Create a release and tag it
5. [ ] Fill out JOSS submission form: http://joss.theoj.org/papers/new
6. [ ] Wait for pre-review by Associate Editor-in-Chief
7. [ ] Respond to reviewers during review process
8. [ ] After acceptance: create Zenodo archive and get DOI

## Optional Improvements

These are not required but would strengthen the submission:

- [ ] Add code coverage reporting (codecov.io)
- [ ] Add more comprehensive benchmarks
- [ ] Create more usage examples
- [ ] Add R vignettes
- [ ] Publish Python package to PyPI
- [ ] Submit R package to CRAN
- [ ] Add comparison benchmarks with manual seed management
- [ ] Document performance characteristics

## Priority Actions

**Must do before submission:**

1. ✅ ~~Create JOSS paper files~~ (DONE)
2. ⚠️ **Verify 6+ months public development history** (CRITICAL)
3. ⚠️ **Update author ORCID** (CRITICAL)
4. ⚠️ **Fix CODE_OF_CONDUCT contact method** (REQUIRED)
5. ⚠️ **Create and tag a release** (CRITICAL)
6. ⚠️ **Verify CI tests pass** (CRITICAL)
7. Add badges to README
8. Proofread all documentation

## Notes

- JOSS requires at least 6 months of public development history with evidence of releases, issues, and/or PRs
- The paper should be 250-1000 words (our paper is ~1800 words - may need editing)
- References must include full venue names, not abbreviations
- AI usage must be transparently disclosed (already done)
- Upon acceptance, will need to create Zenodo archive and obtain DOI

## Useful Links

- JOSS Submission Guidelines: https://joss.readthedocs.io/en/latest/submitting.html
- Review Criteria: https://joss.readthedocs.io/en/latest/review_criteria.html
- Example Paper: https://joss.readthedocs.io/en/latest/example_paper.html
- Submission Form: http://joss.theoj.org/papers/new
