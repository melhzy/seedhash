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

## Advanced ML Paradigms 🆕

seedhash now supports advanced machine learning paradigms with specialized metrics:

### Supported Paradigms

#### 1. **Semi-Supervised Learning**
Track experiments with labeled and unlabeled data:

```python
from seedhash import MLMetrics

metrics = MLMetrics.semi_supervised_metrics(
    y_labeled_true=[0, 1, 1, 0, 1],           # True labels for labeled data
    y_labeled_pred=[0, 1, 0, 0, 1],           # Predictions for labeled data
    y_unlabeled_pseudo=[1, 0, 1, 0, ...],     # Pseudo-labels for unlabeled data
    pseudo_confidence=[0.95, 0.87, ...],      # Confidence scores (optional)
    consistency_scores=[0.92, 0.89, ...]      # Consistency across augmentations (optional)
)

# Returns: labeled_accuracy, label_ratio, pseudo_label_diversity,
#          avg_pseudo_confidence, avg_consistency, etc.
```

**Metrics Included:**
- `labeled_accuracy`: Accuracy on labeled data
- `label_ratio`: Ratio of labeled to total data
- `pseudo_label_diversity`: Variety in pseudo-labels
- `avg_pseudo_confidence`: Average confidence in pseudo-labels
- `high_confidence_ratio`: Proportion of high-confidence predictions
- `avg_consistency`: Consistency score across augmentations

#### 2. **Reinforcement Learning**
Track RL training progress across episodes:

```python
from seedhash import MLMetrics

metrics = MLMetrics.reinforcement_learning_metrics(
    episode_rewards=[150.5, 180.2, 195.7, ...],  # Cumulative rewards per episode
    episode_lengths=[100, 95, 105, ...],          # Steps per episode
    success_flags=[False, True, True, ...],       # Success indicators (optional)
    q_values=[50.2, 75.8, 90.1, ...]             # Q-values (optional)
)

# Returns: mean_reward, success_rate, mean_episode_length,
#          improvement_rate, convergence indicators, etc.
```

**Metrics Included:**
- `mean_reward`, `std_reward`: Reward statistics
- `max_reward`, `min_reward`: Best/worst episodes
- `mean_episode_length`: Average episode duration
- `success_rate`: Proportion of successful episodes
- `mean_q_value`: Average Q-value estimates
- `recent_mean_reward`: Recent performance window
- `improvement_rate`: Learning progress indicator

#### 3. **Federated Learning**
Monitor federated training across clients:

```python
from seedhash import MLMetrics

metrics = MLMetrics.federated_learning_metrics(
    client_accuracies=[0.85, 0.87, 0.83, ...],    # Accuracy per client
    communication_rounds=50,                       # Number of rounds completed
    client_losses=[0.15, 0.13, 0.17, ...],        # Loss per client (optional)
    model_divergences=[0.05, 0.03, ...],          # Model drift (optional)
    participation_rates=[0.9, 0.95, ...]          # Client participation (optional)
)

# Returns: global_accuracy, fairness_cv, convergence_indicator,
#          model_divergence, participation metrics, etc.
```

**Metrics Included:**
- `global_accuracy`: Average accuracy across clients
- `accuracy_std`, `accuracy_variance`: Client heterogeneity
- `min/max_client_accuracy`: Performance range
- `fairness_cv`: Coefficient of variation (fairness indicator)
- `global_loss`: Average loss across clients
- `avg_model_divergence`: Model drift from global
- `convergence_indicator`: Convergence quality metric
- `avg_participation_rate`: Client engagement

### Complete Example: Semi-Supervised Learning

```python
from seedhash import SeedExperimentManager, MLMetrics
import random

# Initialize experiment manager
manager = SeedExperimentManager("semi_supervised_study")

# Generate hierarchical seeds
hierarchy = manager.generate_seed_hierarchy(
    n_seeds=5,
    n_sub_seeds=4,
    sampling_method="stratified"
)

# Run experiments with different seeds
for seed in hierarchy[2]:
    random.seed(seed)
    
    # Simulate semi-supervised setup (10% labeled)
    n_labeled, n_unlabeled = 100, 900
    
    y_labeled_true = [random.randint(0, 2) for _ in range(n_labeled)]
    y_labeled_pred = [val if random.random() > 0.15 else random.randint(0, 2) 
                      for val in y_labeled_true]
    y_unlabeled_pseudo = [random.randint(0, 2) for _ in range(n_unlabeled)]
    pseudo_confidence = [random.uniform(0.6, 0.99) for _ in range(n_unlabeled)]
    
    # Calculate metrics
    metrics = MLMetrics.semi_supervised_metrics(
        y_labeled_true, y_labeled_pred, y_unlabeled_pseudo, pseudo_confidence
    )
    
    # Track experiment
    manager.add_experiment_result(
        seed=seed,
        ml_task="semi_supervised",
        metrics=metrics,
        sampling_method="stratified",
        metadata={"algorithm": "pseudo_labeling", "label_ratio": 0.1}
    )

# Analyze results
df = manager.get_results_dataframe()
print(f"Average labeled accuracy: {df['metric_labeled_accuracy'].mean():.3f}")
print(f"Average pseudo confidence: {df['metric_avg_pseudo_confidence'].mean():.3f}")
```

### Complete Example: Reinforcement Learning

```python
from seedhash import SeedExperimentManager, MLMetrics

manager = SeedExperimentManager("rl_cartpole")

hierarchy = manager.generate_seed_hierarchy(
    n_seeds=5,
    n_sub_seeds=3,
    sampling_method="systematic"
)

for seed in hierarchy[2]:
    # Simulate RL training
    episode_rewards = [...]  # Training rewards
    episode_lengths = [...]  # Episode durations
    success_flags = [reward > 195 for reward in episode_rewards]
    
    metrics = MLMetrics.reinforcement_learning_metrics(
        episode_rewards, episode_lengths, success_flags
    )
    
    manager.add_experiment_result(
        seed=seed,
        ml_task="reinforcement",
        metrics=metrics,
        sampling_method="systematic",
        metadata={"environment": "CartPole-v1", "algorithm": "DQN"}
    )

df = manager.get_results_dataframe()
print(f"Average success rate: {df['metric_success_rate'].mean():.1%}")
```

### Complete Example: Federated Learning

```python
from seedhash import SeedExperimentManager, MLMetrics

manager = SeedExperimentManager("federated_mnist")

hierarchy = manager.generate_seed_hierarchy(
    n_seeds=5,
    n_sub_seeds=4,
    sampling_method="cluster"
)

for seed in hierarchy[2]:
    # Simulate federated training
    client_accuracies = [...]  # 10 clients
    communication_rounds = 50
    
    metrics = MLMetrics.federated_learning_metrics(
        client_accuracies,
        communication_rounds
    )
    
    manager.add_experiment_result(
        seed=seed,
        ml_task="federated",
        metrics=metrics,
        sampling_method="cluster",
        metadata={"aggregation": "FedAvg", "n_clients": 10}
    )

df = manager.get_results_dataframe()
print(f"Average global accuracy: {df['metric_global_accuracy'].mean():.3f}")
print(f"Average fairness CV: {df['metric_fairness_cv'].mean():.3f}")
```

### All Supported ML Tasks

1. **regression**: RMSE, MAE, R², MAPE
2. **classification**: Accuracy, Precision, Recall, F1
3. **unsupervised**: Silhouette score, cluster metrics
4. **supervised**: Generic supervised learning
5. **semi_supervised**: Label propagation, pseudo-label quality
6. **reinforcement**: Episode rewards, success rates, Q-values
7. **federated**: Client accuracy, fairness, convergence

Run advanced examples:
```bash
python examples/advanced_ml_paradigms.py
```

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

**Version**: 0.3.0  
**License**: MIT  
**Python**: >=3.7
