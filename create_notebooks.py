#!/usr/bin/env python3
"""
Script to create properly formatted Jupyter notebooks for SeedHash tutorials.
"""

import json
import os

def create_notebook_1():
    """Create Tutorial #1: Complete SeedHash Tutorial"""
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# 🌟 SeedHash: Complete Tutorial\\n",
                    "\\n",
                    "## Reproducible Random Seed Generation for Machine Learning\\n",
                    "\\n",
                    "Welcome to the comprehensive tutorial for **seedhash**!\\n",
                    "\\n",
                    "### What is SeedHash?\\n",
                    "\\n",
                    "SeedHash generates **deterministic random seeds from string inputs** using MD5 hashing.\\n",
                    "\\n",
                    "### Key Features\\n",
                    "\\n",
                    "✅ **String-to-Seed Conversion**\\n",
                    "✅ **Cross-Framework Support**\\n",
                    "✅ **Hierarchical Sampling**\\n",
                    "✅ **ML Experiment Tracking**"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 1. Installation 📦"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Setup\\n",
                    "import sys\\n",
                    "sys.path.insert(0, '../Python')\\n",
                    "\\n",
                    "from seedhash import SeedHashGenerator\\n",
                    "import random\\n",
                    "import numpy as np\\n",
                    "\\n",
                    "print('✅ SeedHash imported!')"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 2. Basic Usage 🚀"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "gen = SeedHashGenerator('my_experiment')\\n",
                    "print(f'Seed: {gen.seed_number}')"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 3. Reproducibility 🔄"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "gen1 = SeedHashGenerator('data_split_v1')\\n",
                    "random.seed(gen1.seed_number)\\n",
                    "sample1 = random.sample(range(100), 10)\\n",
                    "\\n",
                    "gen2 = SeedHashGenerator('data_split_v1')\\n",
                    "random.seed(gen2.seed_number)\\n",
                    "sample2 = random.sample(range(100), 10)\\n",
                    "\\n",
                    "print(f'Same? {sample1 == sample2} ✅')"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 4. Framework Seeding 🧠"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "gen = SeedHashGenerator('python_exp')\\n",
                    "gen.set_seed('python')\\n",
                    "print('Python seeded!')\\n",
                    "\\n",
                    "gen.set_seed('numpy')\\n",
                    "print('NumPy seeded!')\\n",
                    "\\n",
                    "try:\\n",
                    "    gen.set_seed('torch')\\n",
                    "    print('PyTorch seeded!')\\n",
                    "except ImportError:\\n",
                    "    print('PyTorch not available')"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 5. Seed All Frameworks 🔒"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "gen = SeedHashGenerator('all_frameworks')\\n",
                    "status = gen.seed_all(deterministic=True)\\n",
                    "print('All frameworks seeded!')\\n",
                    "for fw, st in status.items():\\n",
                    "    print(f'  {fw}: {st}')"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## Summary 🎉\\n\\nYou learned:\\n- ✅ Basic usage\\n- ✅ Reproducibility\\n- ✅ Framework seeding\\n\\n**Next**: Tutorial #2!"]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    with open('jupyter/01_Complete_SeedHash_Tutorial.ipynb', 'w') as f:
        json.dump(notebook, f, indent=1)
    print("✅ Created Tutorial #1")

def create_notebook_2():
    """Create Tutorial #2: Hierarchical Sampling"""
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["# 📊 Hierarchical Sampling\\n\\n## Tutorial #2\\n\\nLearn about:\\n- SeedExperimentManager\\n- Hierarchical seeds\\n- 4 sampling methods\\n- Experiment tracking"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["import sys\\nsys.path.insert(0, '../Python')\\n\\nimport numpy as np\\nimport pandas as pd\\nfrom seedhash import SeedExperimentManager\\n\\nprint('✅ Ready!')"]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 1. SeedExperimentManager"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["manager = SeedExperimentManager('my_project')\\nprint(f'Master seed: {manager.master_seed}')"]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 2. Hierarchical Seeds 🌳"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["hierarchy = manager.generate_seed_hierarchy(n_seeds=3, n_sub_seeds=2, max_depth=2)\\nprint(f'Master: {hierarchy[0]}')\\nprint(f'Seeds: {hierarchy[1]}')\\nprint(f'Sub-seeds: {hierarchy[2]}')"]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 3. Experiment Tracking"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["for seed in hierarchy[1][:2]:\\n    manager.add_experiment_result(\\n        seed=seed,\\n        ml_task='regression',\\n        metrics={'rmse': 5.0 + np.random.rand()},\\n        sampling_method='simple'\\n    )\\nprint(f'Tracked {len(manager.results)} experiments')"]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 4. DataFrame Export"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["df = manager.get_results_dataframe()\\nprint(df.head())\\ndf.to_csv('results.csv', index=False)"]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## Summary 🎉\\n\\n✅ Hierarchical seeds\\n✅ Experiment tracking\\n✅ DataFrame export"]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    with open('jupyter/02_Hierarchical_Sampling.ipynb', 'w') as f:
        json.dump(notebook, f, indent=1)
    print("✅ Created Tutorial #2")

def create_notebook_3():
    """Create Tutorial #3: Advanced ML Paradigms"""
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["# 🚀 Advanced ML Paradigms\\n\\n## Tutorial #3\\n\\nLearn about:\\n- Semi-supervised learning\\n- Reinforcement learning\\n- Federated learning"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["import sys\\nsys.path.insert(0, '../Python')\\n\\nimport numpy as np\\nfrom seedhash import SeedExperimentManager\\n\\nprint('✅ Ready!')"]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 1. Semi-Supervised Learning 🏷️"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["manager = SeedExperimentManager('ssl_study')\\nhierarchy = manager.generate_seed_hierarchy(n_seeds=3, n_sub_seeds=2, max_depth=2)\\n\\nfor seed in hierarchy[1][:2]:\\n    manager.add_experiment_result(\\n        seed=seed,\\n        ml_task='semi_supervised',\\n        metrics={'labeled_accuracy': 0.85 + np.random.rand()*0.10},\\n        sampling_method='simple'\\n    )\\nprint('SSL experiments done')"]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 2. Reinforcement Learning 🎮"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["rl_manager = SeedExperimentManager('rl_study')\\nhierarchy = rl_manager.generate_seed_hierarchy(n_seeds=3, n_sub_seeds=2, max_depth=2)\\n\\nfor seed in hierarchy[1][:2]:\\n    rewards = np.random.exponential(120, 100)\\n    rl_manager.add_experiment_result(\\n        seed=seed,\\n        ml_task='reinforcement',\\n        metrics={'mean_reward': rewards.mean()},\\n        sampling_method='simple'\\n    )\\nprint('RL experiments done')"]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 3. Federated Learning 🌐"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["fl_manager = SeedExperimentManager('fl_study')\\nhierarchy = fl_manager.generate_seed_hierarchy(n_seeds=3, n_sub_seeds=2, max_depth=2)\\n\\nfor seed in hierarchy[1][:2]:\\n    client_accs = 0.82 + np.random.rand(10)*0.10\\n    fl_manager.add_experiment_result(\\n        seed=seed,\\n        ml_task='federated',\\n        metrics={'global_accuracy': client_accs.mean()},\\n        sampling_method='simple'\\n    )\\nprint('FL experiments done')"]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## Summary 🎉\\n\\n✅ Semi-supervised learning\\n✅ Reinforcement learning\\n✅ Federated learning\\n\\n**Congratulations! You mastered all SeedHash features!**"]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    with open('jupyter/03_Advanced_ML_Paradigms.ipynb', 'w') as f:
        json.dump(notebook, f, indent=1)
    print("✅ Created Tutorial #3")

if __name__ == "__main__":
    create_notebook_1()
    create_notebook_2()
    create_notebook_3()
    print("\\n✅ All 3 notebooks created successfully!")
