---
title: 'SeedHash: Deterministic Random Seed Generation for Reproducible Research'
tags:
  - Python
  - R
  - reproducibility
  - random seeds
  - machine learning
  - Monte Carlo simulation
authors:
  - name: Ziyuan Huang
    orcid: 0000-0002-2215-2473
    affiliation: 1
affiliations:
  - name: University of Massachusetts Chan Medical School
    index: 1
date: 17 February 2026
bibliography: paper.bib
---

# Summary

Reproducibility is a cornerstone of scientific computing, yet managing random seeds across multiple experiments, simulations, and machine learning runs remains a persistent challenge. `SeedHash` is a cross-language library (Python and R) that generates deterministic random seeds from human-readable string identifiers using MD5 hashing. By converting meaningful experiment names (e.g., "model_v2_baseline") into consistent integer seeds, researchers can ensure reproducibility without manually tracking arbitrary numeric values. The library supports four sampling methods (simple random, stratified, cluster, and systematic sampling) and provides hierarchical seed management for complex experimental designs, making it particularly valuable for machine learning workflows, Monte Carlo simulations, and any computational research requiring reproducible randomness.

# Statement of need

Reproducibility in computational research requires careful management of random number generation. Traditional approaches face several challenges: (1) manually assigning numeric seeds is error-prone and lacks semantic meaning, (2) generating independent seeds for multiple experiments or cross-validation folds risks unintentional correlation, and (3) coordinating seeds across programming languages complicates multi-language workflows. While tools like `numpy.random` [@harris2020array] and R's base random number generators provide seeded pseudorandom number generation, they do not address the seed assignment problem itself.

`SeedHash` targets researchers and data scientists who run multiple computational experiments and need to:
- Generate reproducible results with semantically meaningful seed identifiers
- Maintain seed independence across k-fold cross-validation or multiple simulation runs
- Coordinate random states across Python and R environments
- Track experiment lineage through hierarchical seed structures
- Apply scientifically sound sampling strategies for seed selection

The library fills a gap between low-level random number generators and high-level experiment tracking systems, providing a lightweight solution focused specifically on the seed generation problem. Unlike experiment tracking frameworks (e.g., MLflow [@mlflow], Weights & Biases), `SeedHash` addresses only seed management, making it suitable for integration into existing workflows without imposing broader infrastructure requirements.

# State of the field

Several approaches exist for managing reproducibility in computational research, but none specifically address deterministic seed generation from string identifiers with multi-language support.

**Experiment tracking platforms** like MLflow [@mlflow], Weights & Biases, and Sacred [@sacred] provide comprehensive experiment management including seed tracking, but require substantial infrastructure and focus on logging rather than seed generation. These tools are valuable for full-stack ML experimentation but represent overkill for researchers who simply need reliable seed management.

**Random number generation libraries** such as `numpy.random` [@harris2020array], R's base RNG, and `random` from Python's standard library [@python] provide seeded generators but require users to manually select seeds. The `randomstate` package provides multiple RNG algorithms but does not address seed selection.

**Hashing libraries** like Python's `hashlib` and R's `digest` [@digest] provide MD5 and other hash functions but do not specialize them for seed generation use cases or provide sampling strategies.

`SeedHash` was built as an independent package rather than contributed to existing tools because: (1) experiment tracking platforms are comprehensive systems where seed generation is tangential to their core mission of logging and visualization, (2) RNG libraries appropriately focus on generator algorithms rather than seed assignment strategies, and (3) no existing tool bridges both Python and R with identical interfaces for seed generation. The library's focused scope—generating deterministic seeds from strings with scientifically motivated sampling methods—represents a distinct contribution that complements rather than duplicates existing tools.

# Software design

`SeedHash` adopts a modular, object-oriented design with three core components:

**1. Core seed generation (`SeedHashGenerator`)**: Converts arbitrary strings to deterministic integer seeds via MD5 hashing (taking the first 32 bits of the hash). MD5 is appropriate for this non-cryptographic use case due to its speed and determinism. The generator supports configurable seed ranges to accommodate language-specific RNG requirements (e.g., R's 32-bit integer limit).

**2. Sampling methods (`SeedSampler`)**: Implements four sampling strategies for generating multiple seeds from a master seed:
- **Simple random**: Uniform sampling for general use
- **Stratified**: Divides the seed space into strata for balanced coverage
- **Cluster**: Groups seeds for structured experiments
- **Systematic**: Regular intervals for even distribution

These methods are inspired by survey sampling theory [@cochran1977sampling] and provide researchers with statistically sound options for generating seed sets rather than ad-hoc sequential assignment.

**3. Hierarchical experiment management (`SeedExperimentManager`)**: Supports nested experimental designs where experiments have sub-experiments (e.g., models with hyperparameter searches, each with k-fold CV). This addresses the common pattern in ML research of three-level hierarchies: project → model variants → cross-validation folds.

**Cross-language consistency**: Python and R implementations use identical algorithms, ensuring that `SeedHashGenerator("experiment_1")` produces the same seed value in both languages. This enables workflows that span both environments (e.g., data preprocessing in Python, statistical modeling in R) while maintaining reproducibility.

**Design trade-offs**: We chose MD5 over cryptographic hashes (SHA-256) for speed, since seed generation is not security-sensitive. We use object-oriented patterns for extensibility, though this adds slight verbosity compared to functional interfaces. The hierarchical manager uses pandas [@pandas] and R data frames for compatibility with common data science workflows rather than custom formats.

# Research impact statement

`SeedHash` demonstrates credible near-term significance through its design for common research workflows and increasing adoption:

**Current usage**: The package has been publicly available on GitHub since August 2025, with installation support via pip (Python) and GitHub remotes (R). The repository is actively maintained and available for community use and contribution.

**Tutorial materials**: Three Jupyter notebooks provide end-to-end tutorials covering basic usage, hierarchical sampling, and ML paradigms (supervised learning, deep learning, reinforcement learning), facilitating adoption by researchers unfamiliar with systematic seed management.

**Research applications**: The library directly supports reproducible research patterns in:
- **Machine learning**: K-fold cross-validation with independent seeds per fold
- **Monte Carlo simulations**: Large-scale parallel simulations with deterministic seed assignment
- **Sensitivity analysis**: Systematic exploration of random seed effects on model stability
- **Multi-language workflows**: Coordinating reproducibility across Python-R analysis pipelines

**Benchmarking and validation**: The package includes comprehensive unit tests verifying determinism, cross-language consistency, and sampling statistical properties. Test files (`test_sampling_methods.py`, `test_md5_usage.py`, `test_dl_seeding.py`) demonstrate correctness and provide usage examples.

**Community readiness**: Documentation spans multiple formats (README files, Python docstrings, R documentation, Jupyter tutorials) and installation instructions for both package managers. The MIT license and public GitHub hosting enable immediate adoption.

While large-scale citations are not yet available given the package's recent release, the comprehensive tutorials, multi-language support, and clear documentation position `SeedHash` for adoption in computational research communities that value reproducibility.

# AI usage disclosure

Generative AI tools (GitHub Copilot, Claude Sonnet) were used extensively throughout this project for:

**Software development**:
- Code generation for core classes (`SeedHashGenerator`, `SeedSampler`, `SeedExperimentManager`)
- Test scaffolding and test case generation
- R package porting from Python implementation
- Refactoring and code optimization

**Documentation**:
- README file structure and content
- Docstring generation for API documentation
- Jupyter notebook tutorial content
- Installation guides and troubleshooting documentation

**Paper authoring**:
- Initial drafts of paper sections
- Bibliography formatting and reference checking
- Copy-editing and clarity improvements

**Human review and validation**: All AI-generated code was reviewed, tested, and validated by the human author. Core design decisions (choice of MD5 hashing, sampling method algorithms, hierarchical manager interface, cross-language strategy) were made by the human author. All code correctness was verified through manual testing and automated test suites. The author takes full responsibility for accuracy, correctness, and scientific validity of all materials.

# Acknowledgements

We acknowledge the Astropy project [@astropy2013; @astropy2018] for inspiration in cross-language package design and community documentation standards.

# References
