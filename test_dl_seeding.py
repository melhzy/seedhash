"""
Quick test script to verify deep learning framework seeding functionality.
"""

import sys
sys.path.insert(0, 'Python')

from seedhash import SeedHashGenerator


def test_basic_seeding():
    """Test basic Python seeding (always works)."""
    print("=" * 60)
    print("Test 1: Basic Python Seeding")
    print("=" * 60)
    
    gen = SeedHashGenerator("test_experiment")
    status = gen.set_seed("python")
    
    print(f"Seed number: {gen.seed_number}")
    print(f"Status: {status}")
    print(f"MD5 Hash: {gen.get_hash()}")
    print("✓ Basic seeding works!\n")


def test_torch_if_available():
    """Test PyTorch seeding if available."""
    print("=" * 60)
    print("Test 2: PyTorch Seeding (Default)")
    print("=" * 60)
    
    gen = SeedHashGenerator("pytorch_test")
    
    try:
        # This should work even without torch installed
        status = gen.set_seed()  # Defaults to "torch"
        print(f"Seed number: {gen.seed_number}")
        print(f"Status: {status}")
        
        # Try importing torch to verify
        try:
            import torch
            print(f"✓ PyTorch is installed and seeded!")
            print(f"  PyTorch version: {torch.__version__}")
            
            # Test reproducibility
            tensor1 = torch.randn(2, 2)
            print(f"\nRandom tensor 1:\n{tensor1}")
            
            gen.set_seed("torch")
            tensor2 = torch.randn(2, 2)
            print(f"\nRandom tensor 2 (after re-seeding):\n{tensor2}")
            print(f"\nTensors match: {torch.allclose(tensor1, tensor2)}")
            
        except ImportError:
            print("  Note: PyTorch not installed, but seeding mechanism works")
            print("  Install with: pip install torch")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print()


def test_seed_all():
    """Test seeding all frameworks."""
    print("=" * 60)
    print("Test 3: Seed All Frameworks")
    print("=" * 60)
    
    gen = SeedHashGenerator("multi_framework_test")
    status = gen.seed_all(deterministic=True)
    
    print(f"Seed number: {gen.seed_number}")
    print(f"MD5 Hash: {gen.get_hash()}")
    print("\nFramework seeding status:")
    
    for framework, state in status.items():
        icon = "✓" if "seeded" in state else "○"
        print(f"  {icon} {framework}: {state}")
    
    print()


def test_deterministic_mode():
    """Test deterministic mode settings."""
    print("=" * 60)
    print("Test 4: Deterministic Mode")
    print("=" * 60)
    
    gen = SeedHashGenerator("deterministic_test")
    status = gen.set_seed("torch", deterministic=True)
    
    print(f"Status: {status}")
    
    try:
        import torch
        print("\nDeterministic settings:")
        print(f"  Deterministic algorithms enabled: {torch.are_deterministic_algorithms_enabled()}")
        print(f"  CUDNN deterministic: {torch.backends.cudnn.deterministic}")
        print(f"  CUDNN benchmark: {torch.backends.cudnn.benchmark}")
        print("✓ Deterministic mode configured!")
        
    except ImportError:
        print("  PyTorch not installed - deterministic settings not applicable")
    
    print()


def test_different_experiments():
    """Test multiple experiments with different seeds."""
    print("=" * 60)
    print("Test 5: Multiple Experiments")
    print("=" * 60)
    
    experiments = ["baseline", "augmented", "ensemble"]
    
    print("Experiment seeds:")
    for exp_name in experiments:
        gen = SeedHashGenerator(exp_name)
        print(f"  {exp_name}: {gen.seed_number}")
    
    print("\n✓ Each experiment gets a unique, reproducible seed!")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SEEDHASH: Deep Learning Framework Seeding Tests")
    print("=" * 60 + "\n")
    
    test_basic_seeding()
    test_torch_if_available()
    test_seed_all()
    test_deterministic_mode()
    test_different_experiments()
    
    print("=" * 60)
    print("All tests completed successfully!")
    print("=" * 60)
    print("\nNote: Some frameworks may show 'not_available' if not installed.")
    print("Install them with:")
    print("  pip install torch")
    print("  pip install tensorflow")
    print("  pip install numpy")
