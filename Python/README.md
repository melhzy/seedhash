# seedhash - Python Package

This directory contains the Python implementation of the seedhash library with support for popular deep learning frameworks.

## Structure

```
Python/
├── base.py                  # Original standalone script
├── seedhash/               # Python package
│   ├── __init__.py         # Package exports
│   └── core.py             # SeedHashGenerator class
├── examples/               # Usage examples
│   ├── basic_usage.py
│   ├── advanced_usage.py
│   ├── deep_learning_seeding.py  # NEW: Deep learning examples
│   └── README.md
├── dist/                   # Built distributions
├── seedhash.egg-info/      # Package metadata
├── setup.py                # Package configuration
├── pyproject.toml          # Modern Python packaging
└── requirements.txt        # Dependencies
```

## Installation

### Basic Installation (No ML frameworks)
```bash
pip install git+https://github.com/melhzy/seedhash.git#subdirectory=Python
```

### With PyTorch Support (Recommended for ML)
```bash
pip install "git+https://github.com/melhzy/seedhash.git#subdirectory=Python[torch]"
```

### With TensorFlow Support
```bash
pip install "git+https://github.com/melhzy/seedhash.git#subdirectory=Python[tensorflow]"
```

### With All Frameworks (PyTorch, TensorFlow, NumPy)
```bash
pip install "git+https://github.com/melhzy/seedhash.git#subdirectory=Python[all]"
```

### Local Installation
```bash
cd Python
pip install .               # Basic
pip install .[torch]        # With PyTorch
pip install .[all]          # With all frameworks
```

## Quick Start

### Basic Usage
```python
from seedhash import SeedHashGenerator

# Create a generator
gen = SeedHashGenerator("my_experiment")

# Generate 5 random seeds
seeds = gen.generate_seeds(5)
print(seeds)

# Get the MD5 hash
print(gen.get_hash())
```

### Deep Learning Framework Seeding 🆕

#### PyTorch (Default)
```python
from seedhash import SeedHashGenerator
import torch

# Create generator and seed PyTorch
gen = SeedHashGenerator("pytorch_experiment")
gen.set_seed()  # Seeds PyTorch by default

# Or explicitly:
gen.set_seed("torch")

# Enable deterministic mode for maximum reproducibility
gen.set_seed("torch", deterministic=True)

# Now all PyTorch operations are reproducible
model = torch.nn.Linear(10, 5)
data = torch.randn(32, 10)
```

#### TensorFlow
```python
from seedhash import SeedHashGenerator
import tensorflow as tf

gen = SeedHashGenerator("tensorflow_experiment")
gen.set_seed("tensorflow")

# Now TensorFlow is seeded
model = tf.keras.Sequential([...])
```

#### NumPy
```python
from seedhash import SeedHashGenerator
import numpy as np

gen = SeedHashGenerator("numpy_experiment")
gen.set_seed("numpy")

# NumPy operations are now reproducible
data = np.random.randn(100, 10)
```

#### Seed All Frameworks
```python
gen = SeedHashGenerator("multi_framework_experiment")

# Seed all available frameworks at once
status = gen.seed_all(deterministic=True)
print(status)  # Shows which frameworks were seeded

# Convenience method (same as seed_all)
status = gen.set_seed("all", deterministic=True)
```

## Features

- **Unlimited integer range** (Python's arbitrary precision integers)
- **Reproducible** seeds based on string input
- **No required dependencies** (uses only Python stdlib)
- **Deep Learning Support** 🆕:
  - PyTorch seeding (CPU and CUDA)
  - TensorFlow seeding
  - NumPy seeding
  - Deterministic mode for maximum reproducibility
  - Seed all frameworks with one command
- **Fast** MD5-based hashing
- **Simple API** with clear error messages

## Supported Frameworks

| Framework | Status | Notes |
|-----------|--------|-------|
| Python random | ✅ Always | Built-in, no extra dependencies |
| PyTorch | ✅ Optional | Install with `pip install torch` |
| TensorFlow | ✅ Optional | Install with `pip install tensorflow` |
| NumPy | ✅ Optional | Install with `pip install numpy` |

## API Reference

### `set_seed(framework="torch", deterministic=True)`

Seed the specified framework(s).

**Parameters:**
- `framework` (str): Which framework to seed:
  - `"torch"` - PyTorch (default)
  - `"tensorflow"` - TensorFlow
  - `"numpy"` - NumPy
  - `"python"` - Python's random module only
  - `"all"` - All available frameworks
- `deterministic` (bool): Enable deterministic algorithms (default: True)

**Returns:** Dictionary with seeding status for each framework

**Examples:**
```python
gen.set_seed()                              # PyTorch (default)
gen.set_seed("tensorflow")                  # TensorFlow
gen.set_seed("all")                         # All frameworks
gen.set_seed("torch", deterministic=False)  # PyTorch, non-deterministic
```

### `seed_all(deterministic=True)`

Convenience method to seed all available frameworks.

**Parameters:**
- `deterministic` (bool): Enable deterministic algorithms (default: True)

**Returns:** Dictionary with seeding status

**Example:**
```python
status = gen.seed_all()
# Returns: {'python': 'seeded', 'torch': 'seeded_deterministic', ...}
```

## Examples

See [examples/deep_learning_seeding.py](examples/deep_learning_seeding.py) for comprehensive examples including:
- PyTorch training setup
- TensorFlow model seeding
- NumPy reproducibility
- Multi-framework experiments
- Deterministic mode usage

Run examples:
```bash
cd Python
python examples/deep_learning_seeding.py
python examples/hierarchical_sampling.py  # NEW: Experiment management examples
```

## Hierarchical Seed Sampling & Experiment Management 🆕

seedhash now supports systematic experiment management with hierarchical seed generation and multiple sampling methods.

### Installation with Experiment Support
```bash
pip install "git+https://github.com/melhzy/seedhash.git#subdirectory=Python[experiment]"
# or
pip install "git+https://github.com/melhzy/seedhash.git#subdirectory=Python[all]"
```

### Features
- **Hierarchical Seeds**: master → seeds → sub-seeds → sub-sub-seeds...
- **4 Sampling Methods**: simple, stratified, cluster, systematic
- **ML Task Tracking**: regression, classification, unsupervised, supervised
- **Automatic Metrics**: RMSE, MAE, R², accuracy, F1, silhouette score
- **DataFrame Export**: CSV, JSON, Excel formats

### Quick Start: Experiment Management

#### Example 1: Simple Random Sampling
```python
from seedhash import SeedExperimentManager, MLMetrics

# Initialize experiment manager
manager = SeedExperimentManager("my_ml_project")

# Generate hierarchical seeds
hierarchy = manager.generate_seed_hierarchy(
    n_seeds=10,          # 10 seeds from master
    n_sub_seeds=5,       # 5 sub-seeds from each seed
    max_depth=2,         # Master → Seeds → Sub-seeds
    sampling_method="simple"
)

print(f"Master seed: {manager.master_seed}")
print(f"Level 1: {len(hierarchy[1])} seeds")
print(f"Level 2: {len(hierarchy[2])} sub-seeds")
```

#### Example 2: Running Experiments with Tracking
```python
from seedhash import SeedExperimentManager, MLMetrics
import random

manager = SeedExperimentManager("regression_study")
hierarchy = manager.generate_seed_hierarchy(n_seeds=5, n_sub_seeds=3, sampling_method="stratified")

# Run experiments with different seeds
for seed in hierarchy[2][:10]:  # Use first 10 sub-seeds
    random.seed(seed)
    
    # Simulate regression model
    y_true = [random.uniform(0, 100) for _ in range(50)]
    y_pred = [val + random.uniform(-10, 10) for val in y_true]
    
    # Calculate metrics automatically
    metrics = MLMetrics.regression_metrics(y_true, y_pred)
    
    # Track experiment
    manager.add_experiment_result(
        seed=seed,
        ml_task="regression",
        metrics=metrics,
        sampling_method="stratified",
        metadata={"model": "random_forest", "n_samples": 50}
    )

# Export results to DataFrame
df = manager.get_results_dataframe()
print(df)

# Get summary statistics
summary = manager.get_summary_statistics()
print(summary)

# Export to files
manager.export_results('results.csv', format='csv')
manager.export_results('results.json', format='json')
```

### Sampling Methods Explained

#### 1. **Simple Random Sampling** (`sampling_method="simple"`)
- Each seed has equal probability
- Pure random selection without structure
- **Best for**: Unbiased random exploration

```python
hierarchy = manager.generate_seed_hierarchy(
    n_seeds=10,
    sampling_method="simple"
)
```

#### 2. **Stratified Random Sampling** (`sampling_method="stratified"`)
- Divides seed space into strata
- Ensures balanced coverage across entire range
- **Best for**: Ensuring representation across seed space

```python
hierarchy = manager.generate_seed_hierarchy(
    n_seeds=20,
    sampling_method="stratified"
)
```

#### 3. **Cluster Random Sampling** (`sampling_method="cluster"`)
- Groups seeds into clusters around random centers
- Tests related seeds together
- **Best for**: Testing groups of similar seeds

```python
hierarchy = manager.generate_seed_hierarchy(
    n_seeds=15,
    sampling_method="cluster"
)
```

#### 4. **Systematic Random Sampling** (`sampling_method="systematic"`)
- Selects seeds at regular intervals
- Evenly distributed with periodic sampling
- **Best for**: Systematic coverage with predictable spacing

```python
hierarchy = manager.generate_seed_hierarchy(
    n_seeds=12,
    sampling_method="systematic"
)
```

### DataFrame Output Structure

The results DataFrame includes:
- **experiment_id**: Unique identifier for each experiment
- **seed_level**: Hierarchy depth (0=master, 1=seed, 2=sub-seed, ...)
- **master_seed**: Root seed for the entire experiment
- **seed, sub_seed**: Seeds at each hierarchy level
- **current_seed**: The actual seed used for this experiment
- **sampling_method**: Which sampling method was used
- **ml_task**: Type of ML task (regression, classification, unsupervised, supervised)
- **metric_***: All metrics (RMSE, MAE, R², accuracy, F1, etc.)
- **meta_***: Metadata fields (model type, hyperparameters, etc.)
- **timestamp**: When the experiment was run

Example DataFrame:
```
experiment_id                              seed_level  master_seed  seed        sub_seed     sampling_method  ml_task       metric_rmse  metric_r2  meta_model
project_regression_seed123                 2           1234567      9876543     123         stratified       regression    5.22         0.968      random_forest
project_classification_seed456             2           1234567      9876543     456         stratified       classification             0.850      xgboost
```

### ML Metrics Support

#### Regression Metrics
```python
from seedhash import MLMetrics

metrics = MLMetrics.regression_metrics(y_true, y_pred)
# Returns: {'rmse': ..., 'mae': ..., 'r2': ..., 'mape': ...}
```

#### Classification Metrics
```python
metrics = MLMetrics.classification_metrics(y_true, y_pred)
# Returns: {'accuracy': ..., 'precision': ..., 'recall': ..., 'f1': ...}
```

#### Clustering/Unsupervised Metrics
```python
metrics = MLMetrics.clustering_metrics(X, labels)
# Returns: {'silhouette': ..., 'n_clusters': ..., 'n_samples': ...}
```

### Complete Example

```python
from seedhash import SeedExperimentManager, MLMetrics
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np

# Initialize manager with experiment name
manager = SeedExperimentManager("housing_price_prediction")

# Generate hierarchical seeds with stratified sampling
hierarchy = manager.generate_seed_hierarchy(
    n_seeds=5,           # 5 main experiment variations
    n_sub_seeds=4,       # 4 sub-experiments per variation
    max_depth=2,
    sampling_method="stratified"
)

# Run experiments with each sub-seed
for seed in hierarchy[2]:
    # Split data with this seed
    np.random.seed(seed)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)
    
    # Train model
    model = RandomForestRegressor(random_state=seed, n_estimators=100)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    metrics = MLMetrics.regression_metrics(y_test, y_pred)
    
    # Track experiment
    manager.add_experiment_result(
        seed=seed,
        ml_task="regression",
        metrics=metrics,
        sampling_method="stratified",
        metadata={
            "model": "RandomForest",
            "n_estimators": 100,
            "test_size": 0.2,
            "features": X.shape[1]
        }
    )

# Analyze results
df = manager.get_results_dataframe()
print(f"Average RMSE: {df['metric_rmse'].mean():.3f}")
print(f"Best R²: {df['metric_r2'].max():.3f}")
print(f"Worst R²: {df['metric_r2'].min():.3f}")

# Export for further analysis
manager.export_results('housing_experiments.csv')
```

## Deterministic Mode

When `deterministic=True` (default), seedhash configures frameworks for maximum reproducibility:

**PyTorch:**
- Sets `torch.use_deterministic_algorithms(True)`
- Sets `torch.backends.cudnn.deterministic = True`
- Sets `torch.backends.cudnn.benchmark = False`
- Sets `CUBLAS_WORKSPACE_CONFIG` environment variable

**TensorFlow:**
- Sets `TF_DETERMINISTIC_OPS=1`
- Sets `TF_CUDNN_DETERMINISTIC=1`

**Note:** Deterministic mode may reduce performance but ensures reproducibility.

## Testing

```bash
cd Python
pytest tests/
```

## Building

```bash
cd Python
python setup.py sdist bdist_wheel
```

## Documentation

See the main repository [README.md](../README.md) for complete documentation.

For converting Python features to R, see [PYTHON_TO_R_GUIDE.md](../PYTHON_TO_R_GUIDE.md).

---

**Version**: 0.2.0  
**License**: MIT  
**Python**: >=3.7
