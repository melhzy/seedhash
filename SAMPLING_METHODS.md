# 🎲 Random Sampling Techniques in SeedHash

SeedHash provides **4 scientifically-backed random sampling techniques** for generating reproducible seeds. Each method serves different experimental needs and ensures systematic seed selection.

---

## 📚 Overview of the 4 Sampling Methods

| Method | Best For | Key Feature |
|--------|----------|-------------|
| **Simple Random** | Unbiased exploration | Equal probability for all seeds |
| **Stratified Random** | Balanced coverage | Ensures representation across ranges |
| **Cluster Random** | Related seed groups | Seeds clustered around centers |
| **Systematic Random** | Even distribution | Regular intervals across space |

---

## 1️⃣ Simple Random Sampling

**Pure random selection** where each seed has equal probability.

### When to Use
- Baseline experiments
- No prior knowledge about seed space
- Need completely unbiased selection

### Example
```python
from seedhash import SeedSampler

sampler = SeedSampler(master_seed=42)
seeds = sampler.simple_random_sampling(
    n_samples=10,
    seed_range=(0, 1000)
)
print(seeds)
# [654, 114, 25, 759, 281, 250, 228, 142, 754, 104]
```

### Characteristics
- ✅ Completely random
- ✅ No structure or pattern
- ✅ Simple and straightforward
- ⚠️ May miss some regions by chance

---

## 2️⃣ Stratified Random Sampling

**Divides seed space into strata**, samples from each stratum for **balanced coverage**.

### When to Use
- Want to ensure coverage across entire range
- Need representation from all regions
- Testing across different seed magnitudes

### Example
```python
from seedhash import SeedSampler

sampler = SeedSampler(master_seed=42)
seeds = sampler.stratified_random_sampling(
    n_samples=25,
    seed_range=(0, 1000),
    n_strata=5  # Divide into 5 equal strata
)
print(sorted(seeds))
# [6, 28, 70, 163, 189, 226, 235, 257, 262, 388, ...]
# Notice: Evenly distributed across 0-1000 range
```

### Characteristics
- ✅ Ensures balanced coverage
- ✅ No region is over/under-represented
- ✅ More systematic than simple random
- 📊 Each stratum gets proportional samples

### Stratum Distribution
With `n_samples=25` and `n_strata=5`:
- Stratum 1 (0-199): 5 samples
- Stratum 2 (200-399): 5 samples
- Stratum 3 (400-599): 5 samples
- Stratum 4 (600-799): 5 samples
- Stratum 5 (800-999): 5 samples

---

## 3️⃣ Cluster Random Sampling

**Groups seeds into clusters** around random centers.

### When to Use
- Testing related seeds together
- Need to explore "neighborhoods" of seed values
- Studying local seed behavior patterns

### Example
```python
from seedhash import SeedSampler

sampler = SeedSampler(master_seed=42)
seeds = sampler.cluster_random_sampling(
    n_samples=20,
    seed_range=(0, 1000),
    n_clusters=4,
    samples_per_cluster=5
)
print(sorted(seeds))
# [35, 43, 44, 62, 68,           # Cluster 1 (around ~50)
#  234, 236, 271, 275, 275,      # Cluster 2 (around ~250)
#  655, 661, 669, 671, 701,      # Cluster 3 (around ~670)
#  915, 918, 940, 947, 950]      # Cluster 4 (around ~930)
```

### Characteristics
- ✅ Seeds naturally grouped together
- ✅ Good for testing locality effects
- ✅ Efficient for related experiments
- 🎯 Cluster centers randomly selected

### Clustering Visualization
```
Cluster 1: [35, 43, 44, 62, 68]        → Range: 33
Cluster 2: [234, 236, 271, 275, 275]   → Range: 41
Cluster 3: [655, 661, 669, 671, 701]   → Range: 46
Cluster 4: [915, 918, 940, 947, 950]   → Range: 35
```

---

## 4️⃣ Systematic Random Sampling

**Selects seeds at regular intervals** with a random starting point.

### When to Use
- Need evenly spaced seeds
- Want periodic sampling
- Systematic coverage required

### Example
```python
from seedhash import SeedSampler

sampler = SeedSampler(master_seed=42)
seeds = sampler.systematic_random_sampling(
    n_samples=15,
    seed_range=(0, 1000)
)
print(sorted(seeds))
# [14, 80, 146, 212, 278, 344, 410, 476, 542, 608, 674, 740, 806, 872, 938]
# Notice: Perfect 66-unit intervals!
```

### Characteristics
- ✅ Perfectly even distribution
- ✅ Predictable spacing
- ✅ Efficient coverage
- 📏 Interval = `(max - min) / n_samples`

### Interval Calculation
For `seed_range=(0, 1000)` and `n_samples=15`:
- Interval: `1000 / 15 ≈ 66.67` → **66**
- Random start: `14` (within first interval)
- Seeds: `14, 80, 146, 212, ...` (each +66)

---

## 🔬 Comparison & Selection Guide

### Visual Comparison

```
Simple Random:        ●    ●  ●     ●●   ●  ●●     ●
                      Random, no pattern

Stratified:           ●● ●  ●●● ● ●● ●●  ●●● ●● ●
                      Even coverage across range

Cluster:              ●●●      ●●●●     ●●      ●●●
                      Grouped around centers

Systematic:           ●   ●   ●   ●   ●   ●   ●
                      Perfect intervals
```

### Decision Matrix

| Your Need | Recommended Method |
|-----------|-------------------|
| Unbiased baseline | **Simple Random** |
| Ensure full coverage | **Stratified Random** |
| Test seed neighborhoods | **Cluster Random** |
| Even spacing | **Systematic Random** |
| Don't know what you need | **Stratified Random** (safest) |

---

## 🎯 Advanced Usage

### 1. Integration with SeedExperimentManager

All 4 methods work with hierarchical seed generation:

```python
from seedhash import SeedExperimentManager

manager = SeedExperimentManager("my_experiment")

# Use any sampling method
hierarchy = manager.generate_seed_hierarchy(
    n_seeds=10,
    n_sub_seeds=5,
    max_depth=2,
    sampling_method="stratified"  # or "simple", "cluster", "systematic"
)

print(f"Master: {hierarchy[0]}")
print(f"Level 1: {len(hierarchy[1])} seeds")
print(f"Level 2: {len(hierarchy[2])} sub-seeds")
```

### 2. Reproducibility

Same master seed → Same results:

```python
sampler1 = SeedSampler(master_seed=12345)
sampler2 = SeedSampler(master_seed=12345)

seeds1 = sampler1.stratified_random_sampling(10, (0, 100), 5)
seeds2 = sampler2.stratified_random_sampling(10, (0, 100), 5)

assert seeds1 == seeds2  # ✅ Always True!
```

### 3. Combined Approach

Use different methods for different levels:

```python
# Stratified for broad coverage at level 1
manager1 = SeedExperimentManager("level1")
hierarchy1 = manager1.generate_seed_hierarchy(
    n_seeds=10, n_sub_seeds=5, max_depth=1, sampling_method="stratified"
)

# Then cluster for each seed's sub-seeds
for seed in hierarchy1[1]:
    sampler = SeedSampler(seed)
    sub_seeds = sampler.cluster_random_sampling(
        n_samples=5, seed_range=(0, 1000), n_clusters=2
    )
    print(f"Seed {seed} → Sub-seeds: {sub_seeds}")
```

---

## 📊 Statistical Properties

### Simple Random
- **Mean**: Approximately center of range
- **Variance**: High (no structure)
- **Coverage**: Random (may have gaps)

### Stratified Random
- **Mean**: Close to center of range
- **Variance**: Controlled per stratum
- **Coverage**: Guaranteed across all strata

### Cluster Random
- **Mean**: Depends on cluster centers
- **Variance**: High between clusters, low within
- **Coverage**: Grouped in neighborhoods

### Systematic Random
- **Mean**: Exactly center of range
- **Variance**: Low (evenly spaced)
- **Coverage**: Perfect, no gaps

---

## 🧪 Testing

Run comprehensive tests:

```bash
python test_sampling_methods.py
```

Output:
```
✅ 1. Simple Random Sampling - Working
✅ 2. Stratified Random Sampling - Working
✅ 3. Cluster Random Sampling - Working
✅ 4. Systematic Random Sampling - Working
✅ 5. Reproducibility - Verified
✅ 6. SeedExperimentManager Integration - Working
```

---

## 📖 References

### Scientific Background

1. **Simple Random Sampling**: Classical probability theory
2. **Stratified Sampling**: Neyman (1934) - Optimal allocation
3. **Cluster Sampling**: Survey methodology, reduces cost
4. **Systematic Sampling**: Madow & Madow (1944) - Efficient coverage

### Use Cases in ML

- **Simple**: Baseline experiments, Monte Carlo simulations
- **Stratified**: Cross-validation, ensemble methods
- **Cluster**: Batch experiments, hyperparameter search neighborhoods
- **Systematic**: Grid search, learning curves, ablation studies

---

## 🎓 Best Practices

### 1. Choose the Right Method
```python
# DON'T: Always use simple random
seeds = sampler.simple_random_sampling(100)

# DO: Match method to your needs
if need_coverage:
    seeds = sampler.stratified_random_sampling(100, n_strata=10)
elif need_groups:
    seeds = sampler.cluster_random_sampling(100, n_clusters=5)
```

### 2. Document Your Choice
```python
# Good: Explain why
method = "stratified"  # Ensures balanced coverage across seed space
hierarchy = manager.generate_seed_hierarchy(
    n_seeds=10, n_sub_seeds=5, max_depth=2, sampling_method=method
)
```

### 3. Consider Computational Cost

| Method | Computational Cost | Memory Cost |
|--------|-------------------|-------------|
| Simple | O(n) | O(1) |
| Stratified | O(n) | O(k) strata |
| Cluster | O(n) | O(c) clusters |
| Systematic | O(n) | O(1) |

All methods are efficient! ✅

---

## 🚀 Quick Start Examples

### Basic Usage
```python
from seedhash import SeedSampler

# Initialize
sampler = SeedSampler(master_seed=42)

# Get 10 simple random seeds
simple = sampler.simple_random_sampling(10, (0, 1000))

# Get 10 stratified seeds (5 strata)
stratified = sampler.stratified_random_sampling(10, (0, 1000), 5)

# Get 10 clustered seeds (3 clusters)
cluster = sampler.cluster_random_sampling(10, (0, 1000), 3)

# Get 10 systematic seeds
systematic = sampler.systematic_random_sampling(10, (0, 1000))
```

### With Experiment Tracking
```python
from seedhash import SeedExperimentManager
import numpy as np

manager = SeedExperimentManager("my_study")

# Try all methods
for method in ["simple", "stratified", "cluster", "systematic"]:
    hierarchy = manager.generate_seed_hierarchy(
        n_seeds=5, n_sub_seeds=3, max_depth=2, sampling_method=method
    )
    
    for seed in hierarchy[1]:
        # Run your experiment
        np.random.seed(seed)
        accuracy = 0.8 + np.random.rand() * 0.15
        
        # Track results
        manager.add_experiment_result(
            seed=seed,
            ml_task="classification",
            metrics={"accuracy": accuracy},
            sampling_method=method
        )

# Export
df = manager.get_results_dataframe()
print(df.groupby('sampling_method')['metric_accuracy'].mean())
```

---

## ✅ Summary

SeedHash provides **4 complete random sampling techniques**:

1. ✅ **Simple Random Sampling** - Pure randomness
2. ✅ **Stratified Random Sampling** - Balanced coverage
3. ✅ **Cluster Random Sampling** - Grouped seeds
4. ✅ **Systematic Random Sampling** - Even intervals

All methods:
- ✅ Fully reproducible
- ✅ Integrate with `SeedExperimentManager`
- ✅ Tested and verified
- ✅ Documented and ready to use

**Choose the method that fits your experimental design! 🎉**
