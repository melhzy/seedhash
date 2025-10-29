"""Demo script showing various usage examples of the SeedHash library."""

from seedhash import SeedHashGenerator


def basic_example():
    """Basic usage example."""
    print("=" * 60)
    print("BASIC EXAMPLE")
    print("=" * 60)
    
    # Create a generator with an input string
    generator = SeedHashGenerator("Shalini")
    
    # Generate 10 random seeds
    seeds = generator.generate_seeds(10)
    
    print(f"Input string: '{generator.input_string}'")
    print(f"MD5 Hash: {generator.get_hash()}")
    print(f"Seed number: {generator.seed_number}")
    print(f"Generated seeds: {seeds}")
    print()


def custom_range_example():
    """Example with custom range."""
    print("=" * 60)
    print("CUSTOM RANGE EXAMPLE")
    print("=" * 60)
    
    # Custom range for random numbers
    gen = SeedHashGenerator(
        input_string="experiment_42",
        min_value=100,
        max_value=1000
    )
    
    # Generate 5 seeds in the range [100, 1000]
    seeds = gen.generate_seeds(5)
    
    print(f"Input string: '{gen.input_string}'")
    print(f"Range: [{gen.min_value}, {gen.max_value}]")
    print(f"Generated seeds: {seeds}")
    print()


def reproducibility_example():
    """Demonstrate reproducibility."""
    print("=" * 60)
    print("REPRODUCIBILITY EXAMPLE")
    print("=" * 60)
    
    # Same input always produces same output
    gen1 = SeedHashGenerator("experiment_1")
    seeds1 = gen1.generate_seeds(5)
    
    gen2 = SeedHashGenerator("experiment_1")
    seeds2 = gen2.generate_seeds(5)
    
    print(f"First generation:  {seeds1}")
    print(f"Second generation: {seeds2}")
    print(f"Are they equal? {seeds1 == seeds2}")
    print()


def error_handling_example():
    """Demonstrate error handling."""
    print("=" * 60)
    print("ERROR HANDLING EXAMPLES")
    print("=" * 60)
    
    # Test 1: Empty string
    try:
        gen = SeedHashGenerator("")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    
    # Test 2: Invalid range
    try:
        gen = SeedHashGenerator("test", min_value=100, max_value=50)
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    
    # Test 3: Non-positive count
    try:
        gen = SeedHashGenerator("test")
        seeds = gen.generate_seeds(0)
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    
    # Test 4: Non-string input
    try:
        gen = SeedHashGenerator("123")
    except TypeError as e:
        print(f"✓ Caught expected error: {e}")
    
    print()


def machine_learning_example():
    """Example for ML experiments."""
    print("=" * 60)
    print("MACHINE LEARNING USE CASE")
    print("=" * 60)
    
    # Reproducible train/test splits
    experiment_name = "model_v1_baseline"
    gen = SeedHashGenerator(experiment_name)
    seeds = gen.generate_seeds(5)  # For different folds
    
    print(f"Experiment: {experiment_name}")
    print("Seeds for K-fold cross-validation:")
    for i, seed in enumerate(seeds, 1):
        print(f"  Fold {i}: {seed}")
    print()


def simulation_example():
    """Example for Monte Carlo simulations."""
    print("=" * 60)
    print("MONTE CARLO SIMULATION USE CASE")
    print("=" * 60)
    
    # Reproducible simulation runs
    simulation_id = "monte_carlo_sim_2025"
    gen = SeedHashGenerator(simulation_id, min_value=1, max_value=10000)
    
    # Generate seeds for parallel simulation runs
    num_simulations = 10
    simulation_seeds = gen.generate_seeds(num_simulations)
    
    print(f"Simulation ID: {simulation_id}")
    print(f"Number of parallel runs: {num_simulations}")
    print(f"Seeds: {simulation_seeds}")
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("SEEDHASH LIBRARY DEMO")
    print("=" * 60 + "\n")
    
    basic_example()
    custom_range_example()
    reproducibility_example()
    error_handling_example()
    machine_learning_example()
    simulation_example()
    
    print("=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
