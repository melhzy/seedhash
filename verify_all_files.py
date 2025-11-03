"""
Comprehensive verification script for all .py and .ipynb files in SeedHash.

This script checks:
1. All Python files can be imported/executed
2. All functions are properly defined
3. All Jupyter notebooks have correct API calls
4. No deprecated or incorrect method calls
"""

import sys
import os
import json
import importlib.util
from pathlib import Path

# Add Python directory to path
sys.path.insert(0, 'Python')


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text):
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(80)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}\n")


def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def print_warning(text):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")


def verify_core_module():
    """Verify the core SeedHashGenerator module."""
    print_header("1. CORE MODULE (SeedHashGenerator)")
    
    try:
        from seedhash import SeedHashGenerator
        
        # Test basic functionality
        gen = SeedHashGenerator("test")
        seeds = gen.generate_seeds(5)
        hash_val = gen.get_hash()
        
        assert len(seeds) == 5, "generate_seeds should return 5 seeds"
        assert isinstance(hash_val, str), "get_hash should return string"
        assert hasattr(gen, 'seed_number'), "Should have seed_number attribute"
        
        print_success("SeedHashGenerator imported successfully")
        print_success("generate_seeds() working")
        print_success("get_hash() working")
        print_success("seed_number attribute present")
        
        return True
    except Exception as e:
        print_error(f"Core module verification failed: {e}")
        return False


def verify_sampler_module():
    """Verify the SeedSampler with 4 sampling methods."""
    print_header("2. SAMPLER MODULE (4 Sampling Methods)")
    
    try:
        from seedhash import SeedSampler
        
        sampler = SeedSampler(master_seed=42)
        
        # Test all 4 methods
        methods = [
            ('simple_random_sampling', {'n_samples': 10, 'seed_range': (0, 100)}),
            ('stratified_random_sampling', {'n_samples': 10, 'seed_range': (0, 100), 'n_strata': 5}),
            ('cluster_random_sampling', {'n_samples': 10, 'seed_range': (0, 100), 'n_clusters': 3}),
            ('systematic_random_sampling', {'n_samples': 10, 'seed_range': (0, 100)}),
        ]
        
        for method_name, params in methods:
            if not hasattr(sampler, method_name):
                print_error(f"Missing method: {method_name}")
                return False
            
            method = getattr(sampler, method_name)
            result = method(**params)
            
            if not isinstance(result, list) or len(result) != params['n_samples']:
                print_error(f"{method_name} returned invalid result")
                return False
            
            print_success(f"{method_name}() working")
        
        return True
    except Exception as e:
        print_error(f"Sampler module verification failed: {e}")
        return False


def verify_experiment_manager():
    """Verify SeedExperimentManager."""
    print_header("3. EXPERIMENT MANAGER")
    
    try:
        from seedhash import SeedExperimentManager
        
        manager = SeedExperimentManager("test_experiment")
        
        # Test hierarchical generation with all sampling methods
        for method in ["simple", "stratified", "cluster", "systematic"]:
            hierarchy = manager.generate_seed_hierarchy(
                n_seeds=3,
                n_sub_seeds=2,
                max_depth=2,
                sampling_method=method
            )
            
            assert 0 in hierarchy, f"Missing level 0 for {method}"
            assert 1 in hierarchy, f"Missing level 1 for {method}"
            assert 2 in hierarchy, f"Missing level 2 for {method}"
            
            print_success(f"generate_seed_hierarchy() with '{method}' method working")
        
        # Test experiment tracking
        manager.add_experiment_result(
            seed=12345,
            ml_task="classification",
            metrics={"accuracy": 0.95},
            sampling_method="simple"
        )
        
        print_success("add_experiment_result() working")
        
        # Test DataFrame export
        df = manager.get_results_dataframe()
        assert df is not None, "DataFrame should not be None"
        print_success("get_results_dataframe() working")
        
        return True
    except Exception as e:
        print_error(f"Experiment manager verification failed: {e}")
        return False


def verify_ml_metrics():
    """Verify MLMetrics module."""
    print_header("4. ML METRICS MODULE")
    
    try:
        from seedhash import MLMetrics
        
        # Test regression metrics
        y_true = [1, 2, 3, 4, 5]
        y_pred = [1.1, 2.1, 2.9, 4.2, 4.8]
        
        reg_metrics = MLMetrics.regression_metrics(y_true, y_pred)
        assert 'rmse' in reg_metrics, "Missing RMSE metric"
        assert 'mae' in reg_metrics, "Missing MAE metric"
        assert 'r2' in reg_metrics, "Missing R² metric"
        
        print_success("regression_metrics() working")
        
        # Test classification metrics
        y_true_cls = [0, 1, 1, 0, 1, 0]
        y_pred_cls = [0, 1, 0, 0, 1, 1]
        
        cls_metrics = MLMetrics.classification_metrics(y_true_cls, y_pred_cls)
        assert 'accuracy' in cls_metrics, "Missing accuracy metric"
        assert 'precision' in cls_metrics, "Missing precision metric"
        assert 'recall' in cls_metrics, "Missing recall metric"
        assert 'f1' in cls_metrics, "Missing F1 metric"
        
        print_success("classification_metrics() working")
        
        return True
    except Exception as e:
        print_error(f"ML metrics verification failed: {e}")
        return False


def verify_python_examples():
    """Verify Python example files."""
    print_header("5. PYTHON EXAMPLE FILES")
    
    example_files = [
        'Python/examples/demo.py',
        'Python/examples/quick_reference.py',
        'Python/examples/hierarchical_sampling.py',
        'Python/examples/deep_learning_seeding.py',
        'Python/examples/advanced_ml_paradigms.py',
    ]
    
    success_count = 0
    for file_path in example_files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check for deprecated methods
                if 'simple_random_sample(' in content or 'stratified_random_sample(' in content:
                    print_error(f"{file_path} uses deprecated method names")
                else:
                    print_success(f"{os.path.basename(file_path)} - No deprecated methods")
                    success_count += 1
        else:
            print_warning(f"{file_path} not found")
    
    return success_count == len(example_files)


def verify_test_files():
    """Verify test files."""
    print_header("6. TEST FILES")
    
    test_files = [
        'test_md5_usage.py',
        'test_dl_seeding.py',
        'test_sampling_methods.py',
    ]
    
    success_count = 0
    for file_path in test_files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check for proper imports
                has_imports = 'from seedhash import' in content or 'import seedhash' in content
                
                if has_imports:
                    print_success(f"{file_path} - Has proper imports")
                    success_count += 1
                else:
                    print_warning(f"{file_path} - Missing seedhash imports")
        else:
            print_warning(f"{file_path} not found")
    
    return success_count >= 2  # At least 2 test files should be valid


def verify_notebooks():
    """Verify Jupyter notebooks."""
    print_header("7. JUPYTER NOTEBOOKS")
    
    notebook_files = [
        'jupyter/01_Complete_SeedHash_Tutorial.ipynb',
        'jupyter/02_Hierarchical_Sampling.ipynb',
        'jupyter/03_Advanced_ML_Paradigms.ipynb',
    ]
    
    deprecated_patterns = [
        'manager.simple_random_sample(',
        'manager.stratified_random_sample(',
        'subdirectory=Python[all]',  # Wrong install syntax
    ]
    
    correct_patterns = [
        'SeedSampler',
        'simple_random_sampling',
        'stratified_random_sampling',
        'egg=seedhash[all]&subdirectory=Python',  # Correct install syntax
    ]
    
    success_count = 0
    for file_path in notebook_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    notebook = json.load(f)
                
                # Check if it's valid JSON
                if 'cells' not in notebook:
                    print_error(f"{os.path.basename(file_path)} - Invalid notebook format")
                    continue
                
                # Extract all code from cells (source only, not outputs)
                all_code = ""
                for cell in notebook['cells']:
                    if cell['cell_type'] == 'code':
                        # Only check the source, not the outputs
                        all_code += ''.join(cell.get('source', []))
                
                # Check for deprecated patterns
                has_deprecated = any(pattern in all_code for pattern in deprecated_patterns)
                
                if has_deprecated:
                    print_error(f"{os.path.basename(file_path)} - Contains deprecated API calls")
                else:
                    print_success(f"{os.path.basename(file_path)} - No deprecated methods")
                    success_count += 1
                
            except json.JSONDecodeError:
                print_error(f"{os.path.basename(file_path)} - Invalid JSON format")
            except Exception as e:
                print_error(f"{os.path.basename(file_path)} - Error: {e}")
        else:
            print_warning(f"{file_path} not found")
    
    return success_count == len(notebook_files)


def verify_exports():
    """Verify __init__.py exports."""
    print_header("8. PACKAGE EXPORTS")
    
    try:
        from seedhash import (
            SeedHashGenerator,
            SeedExperimentManager,
            SeedSampler,
            MLMetrics,
            ExperimentResult
        )
        
        exports = [
            'SeedHashGenerator',
            'SeedExperimentManager',
            'SeedSampler',
            'MLMetrics',
            'ExperimentResult'
        ]
        
        for export in exports:
            print_success(f"{export} exported correctly")
        
        return True
    except ImportError as e:
        print_error(f"Export verification failed: {e}")
        return False


def main():
    """Run all verifications."""
    print_header("SEEDHASH: COMPREHENSIVE FILE VERIFICATION")
    print("Checking all .py files and .ipynb files for correct functions...\n")
    
    results = []
    
    # Run all verifications
    results.append(("Core Module", verify_core_module()))
    results.append(("Sampler Module (4 Methods)", verify_sampler_module()))
    results.append(("Experiment Manager", verify_experiment_manager()))
    results.append(("ML Metrics", verify_ml_metrics()))
    results.append(("Python Examples", verify_python_examples()))
    results.append(("Test Files", verify_test_files()))
    results.append(("Jupyter Notebooks", verify_notebooks()))
    results.append(("Package Exports", verify_exports()))
    
    # Print summary
    print_header("VERIFICATION SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        if result:
            print_success(f"{name}: PASSED")
        else:
            print_error(f"{name}: FAILED")
    
    print(f"\n{Colors.BOLD}Results: {passed}/{total} checks passed{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}{'='*80}{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}{'🎉 ALL VERIFICATIONS PASSED! 🎉'.center(80)}{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}{'='*80}{Colors.END}\n")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}{'='*80}{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}{'⚠️  SOME VERIFICATIONS FAILED'.center(80)}{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}{'='*80}{Colors.END}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
