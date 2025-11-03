# SeedHash Jupyter Notebooks

Welcome to the SeedHash Jupyter notebook tutorials! These interactive notebooks demonstrate all features and use cases of the seedhash library.

## 📚 Notebooks Overview

### 1. **01_Complete_SeedHash_Tutorial.ipynb** (🌟 Start Here!)
**Comprehensive introduction covering all basics**

Topics covered:
- Installation and setup
- Basic usage: `SeedHashGenerator`
- Generating deterministic seeds
- Seeding Python, NumPy, PyTorch, TensorFlow
- Deterministic mode for maximum reproducibility
- Generating multiple random seeds
- Custom ranges and MD5 hashes
- Practical examples: data splitting, model training
- Error handling

**Duration**: ~30 minutes  
**Prerequisites**: None  
**Best for**: First-time users, getting started

---

### 2. **02_Hierarchical_Sampling.ipynb**
**Advanced seed management and experiment tracking**

Topics covered:
- `SeedExperimentManager` introduction
- Hierarchical seed generation (master → seeds → sub-seeds)
- 4 sampling methods:
  - Simple random sampling
  - Stratified random sampling
  - Cluster random sampling
  - Systematic random sampling
- ML experiment tracking
- DataFrame export and analysis
- Regression, classification, clustering metrics

**Duration**: ~45 minutes  
**Prerequisites**: Basic Python, pandas knowledge  
**Best for**: Running systematic ML experiments

---

### 3. **03_Advanced_ML_Paradigms.ipynb**
**Semi-supervised, reinforcement, and federated learning**

Topics covered:
- Semi-supervised learning metrics
  - Label propagation
  - Pseudo-labeling confidence
  - Consistency scores
- Reinforcement learning metrics
  - Episode rewards and success rates
  - Q-value tracking
  - Convergence indicators
- Federated learning metrics
  - Client accuracy distribution
  - Fairness metrics
  - Model divergence tracking
- Complete examples for each paradigm

**Duration**: ~60 minutes  
**Prerequisites**: ML fundamentals, 02_Hierarchical_Sampling.ipynb  
**Best for**: Advanced ML practitioners

---

## 🚀 Quick Start

### Option 1: Run Locally

1. **Clone the repository**:
   ```bash
   git clone https://github.com/melhzy/seedhash.git
   cd seedhash/jupyter
   ```

2. **Install dependencies**:
   ```bash
   pip install jupyter pandas numpy matplotlib seaborn
   pip install "../Python[all]"  # Install seedhash with all dependencies
   ```

3. **Launch Jupyter**:
   ```bash
   jupyter notebook
   ```

4. **Open `01_Complete_SeedHash_Tutorial.ipynb`** and start learning!

### Option 2: Run in Google Colab

Click the badges below to open notebooks directly in Google Colab:

- [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]() **01_Complete_SeedHash_Tutorial.ipynb**
- [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]() **02_Hierarchical_Sampling.ipynb**
- [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]() **03_Advanced_ML_Paradigms.ipynb**

---

## 📋 Learning Path

```
┌─────────────────────────────────────┐
│  START: New to SeedHash?           │
│  → 01_Complete_SeedHash_Tutorial    │
│     (30 mins)                       │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│  Running ML Experiments?            │
│  → 02_Hierarchical_Sampling         │
│     (45 mins)                       │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│  Advanced ML (SSL, RL, FL)?         │
│  → 03_Advanced_ML_Paradigms         │
│     (60 mins)                       │
└─────────────────────────────────────┘
```

---

## 🎯 Use Case Matrix

| Use Case | Notebook | Time | Difficulty |
|----------|----------|------|------------|
| Generate reproducible seeds | #01 | 5 min | ⭐ Beginner |
| Seed PyTorch/TensorFlow | #01 | 10 min | ⭐ Beginner |
| Split data reproducibly | #01 | 15 min | ⭐ Beginner |
| Run multiple experiments | #02 | 20 min | ⭐⭐ Intermediate |
| Track ML metrics | #02 | 30 min | ⭐⭐ Intermediate |
| Hierarchical sampling | #02 | 40 min | ⭐⭐ Intermediate |
| Semi-supervised learning | #03 | 50 min | ⭐⭐⭐ Advanced |
| Reinforcement learning | #03 | 50 min | ⭐⭐⭐ Advanced |
| Federated learning | #03 | 50 min | ⭐⭐⭐ Advanced |

---

## 💡 Key Concepts

### Deterministic Seeding
```python
from seedhash import SeedHashGenerator

# Same input → Same seed (always!)
gen1 = SeedHashGenerator("experiment_1")
gen2 = SeedHashGenerator("experiment_1")

assert gen1.seed_number == gen2.seed_number  # ✅ True
```

### Hierarchical Seeds
```python
from seedhash import SeedExperimentManager

manager = SeedExperimentManager("my_project")
hierarchy = manager.generate_seed_hierarchy(
    n_seeds=10,          # 10 main seeds
    n_sub_seeds=5,       # 5 sub-seeds each
    max_depth=2          # 2 levels deep
)
# Result: master_seed → 10 seeds → 50 sub-seeds
```

### Experiment Tracking
```python
# Run experiments and track results
manager.add_experiment_result(
    seed=12345,
    ml_task="regression",
    metrics={'rmse': 5.23, 'r2': 0.87},
    sampling_method="stratified"
)

# Export to DataFrame
df = manager.get_results_dataframe()
df.to_csv('results.csv')
```

---

## 🛠️ Installation

### Basic Installation
```bash
pip install git+https://github.com/melhzy/seedhash.git#subdirectory=Python
```

### With Deep Learning Support
```bash
# PyTorch
pip install "git+https://github.com/melhzy/seedhash.git#subdirectory=Python[torch]"

# TensorFlow
pip install "git+https://github.com/melhzy/seedhash.git#subdirectory=Python[tensorflow]"

# All frameworks
pip install "git+https://github.com/melhzy/seedhash.git#subdirectory=Python[all]"
```

### With Experiment Management
```bash
pip install "git+https://github.com/melhzy/seedhash.git#subdirectory=Python[experiment]"
```

---

## 📖 Additional Resources

- **Python Examples**: `../Python/examples/`
- **API Documentation**: `../Python/README.md`
- **GitHub Repository**: https://github.com/melhzy/seedhash
- **R Package**: `../R/` (if you use R)

---

## 🤝 Contributing

Found an issue or have a suggestion? Please open an issue on GitHub!

---

## 📜 License

MIT License - see LICENSE file for details

---

**Happy Learning! 🎉**

Start with `01_Complete_SeedHash_Tutorial.ipynb` and work your way through!
