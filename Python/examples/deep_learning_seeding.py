"""
Deep Learning Framework Seeding Examples

This example demonstrates how to use seedhash with popular deep learning frameworks
to ensure reproducibility in machine learning experiments.
"""

from seedhash import SeedHashGenerator


def example_pytorch_seeding():
    """Example: Seeding PyTorch for reproducible training."""
    print("=" * 60)
    print("PyTorch Seeding Example")
    print("=" * 60)
    
    # Create generator
    gen = SeedHashGenerator("pytorch_experiment_1")
    
    # Seed PyTorch (default framework)
    status = gen.set_seed()  # Defaults to "torch"
    print(f"Seeding status: {status}")
    print(f"Seed number: {gen.seed_number}")
    
    try:
        import torch
        
        # Create reproducible tensors
        tensor1 = torch.randn(3, 3)
        print("\nRandom tensor:")
        print(tensor1)
        
        # Reset with same seed - should get identical results
        gen.set_seed("torch")
        tensor2 = torch.randn(3, 3)
        print("\nTensor after re-seeding (should be identical):")
        print(tensor2)
        print(f"Tensors are equal: {torch.allclose(tensor1, tensor2)}")
        
    except ImportError:
        print("PyTorch not installed. Install with: pip install torch")
    
    print()


def example_tensorflow_seeding():
    """Example: Seeding TensorFlow for reproducible training."""
    print("=" * 60)
    print("TensorFlow Seeding Example")
    print("=" * 60)
    
    # Create generator
    gen = SeedHashGenerator("tensorflow_experiment_1")
    
    # Seed TensorFlow
    status = gen.set_seed("tensorflow")
    print(f"Seeding status: {status}")
    print(f"Seed number: {gen.seed_number}")
    
    try:
        import tensorflow as tf
        
        # Create reproducible tensors
        tensor1 = tf.random.normal([3, 3])
        print("\nRandom tensor:")
        print(tensor1.numpy())
        
        # Reset with same seed - should get identical results
        gen.set_seed("tensorflow")
        tensor2 = tf.random.normal([3, 3])
        print("\nTensor after re-seeding (should be identical):")
        print(tensor2.numpy())
        print(f"Tensors are equal: {tf.reduce_all(tf.equal(tensor1, tensor2)).numpy()}")
        
    except ImportError:
        print("TensorFlow not installed. Install with: pip install tensorflow")
    
    print()


def example_numpy_seeding():
    """Example: Seeding NumPy for reproducible computations."""
    print("=" * 60)
    print("NumPy Seeding Example")
    print("=" * 60)
    
    # Create generator
    gen = SeedHashGenerator("numpy_experiment_1")
    
    # Seed NumPy
    status = gen.set_seed("numpy")
    print(f"Seeding status: {status}")
    print(f"Seed number: {gen.seed_number}")
    
    try:
        import numpy as np
        
        # Create reproducible arrays
        array1 = np.random.randn(3, 3)
        print("\nRandom array:")
        print(array1)
        
        # Reset with same seed - should get identical results
        gen.set_seed("numpy")
        array2 = np.random.randn(3, 3)
        print("\nArray after re-seeding (should be identical):")
        print(array2)
        print(f"Arrays are equal: {np.allclose(array1, array2)}")
        
    except ImportError:
        print("NumPy not installed. Install with: pip install numpy")
    
    print()


def example_seed_all_frameworks():
    """Example: Seed all available frameworks at once."""
    print("=" * 60)
    print("Seed All Frameworks Example")
    print("=" * 60)
    
    # Create generator
    gen = SeedHashGenerator("multi_framework_experiment")
    
    # Seed all available frameworks
    status = gen.seed_all(deterministic=True)
    
    print(f"Seed number: {gen.seed_number}")
    print("Seeding status:")
    for framework, state in status.items():
        print(f"  {framework}: {state}")
    
    print("\nAll frameworks are now seeded for reproducibility!")
    print()


def example_deterministic_mode():
    """Example: Using deterministic mode for maximum reproducibility."""
    print("=" * 60)
    print("Deterministic Mode Example (PyTorch)")
    print("=" * 60)
    
    # Create generator
    gen = SeedHashGenerator("deterministic_experiment")
    
    # Seed with deterministic mode enabled
    status = gen.set_seed("torch", deterministic=True)
    print(f"Seeding status: {status}")
    print(f"Seed number: {gen.seed_number}")
    
    try:
        import torch
        
        print("\nDeterministic settings:")
        print(f"  torch.are_deterministic_algorithms_enabled(): "
              f"{torch.are_deterministic_algorithms_enabled()}")
        print(f"  torch.backends.cudnn.deterministic: "
              f"{torch.backends.cudnn.deterministic}")
        print(f"  torch.backends.cudnn.benchmark: "
              f"{torch.backends.cudnn.benchmark}")
        
        print("\nNote: Deterministic mode ensures maximum reproducibility")
        print("but may reduce performance for some operations.")
        
    except ImportError:
        print("PyTorch not installed. Install with: pip install torch")
    
    print()


def example_different_experiments():
    """Example: Different seeds for different experiments."""
    print("=" * 60)
    print("Multiple Experiments Example")
    print("=" * 60)
    
    experiments = ["baseline", "augmented", "ensemble"]
    
    try:
        import torch
        
        for exp_name in experiments:
            gen = SeedHashGenerator(exp_name)
            gen.set_seed("torch")
            
            # Generate a sample tensor
            sample = torch.randn(2, 2)
            
            print(f"\n{exp_name} (seed: {gen.seed_number}):")
            print(sample)
        
    except ImportError:
        print("PyTorch not installed. Install with: pip install torch")
    
    print()


def example_training_loop_seeding():
    """Example: Seeding in a typical training loop setup."""
    print("=" * 60)
    print("Training Loop Seeding Example")
    print("=" * 60)
    
    # Setup experiment
    experiment_name = "my_model_v1"
    gen = SeedHashGenerator(experiment_name)
    
    # Seed all frameworks before training
    status = gen.seed_all(deterministic=True)
    
    print(f"Experiment: {experiment_name}")
    print(f"Seed: {gen.seed_number}")
    print(f"MD5 Hash: {gen.get_hash()}")
    print(f"\nFrameworks seeded: {list(status.keys())}")
    
    print("\n# Pseudocode for training loop:")
    print("# model = create_model()")
    print("# optimizer = create_optimizer(model.parameters())")
    print("# ")
    print("# for epoch in range(num_epochs):")
    print("#     for batch in dataloader:")
    print("#         # Training code here")
    print("#         pass")
    
    print("\nWith seeding, this training loop will be fully reproducible!")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SEEDHASH: Deep Learning Framework Seeding Examples")
    print("=" * 60 + "\n")
    
    # Run all examples
    example_pytorch_seeding()
    example_tensorflow_seeding()
    example_numpy_seeding()
    example_seed_all_frameworks()
    example_deterministic_mode()
    example_different_experiments()
    example_training_loop_seeding()
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)
