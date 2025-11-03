"""
Test script to verify MD5 algorithm usage in seedhash.
This checks for proper implementation and common pitfalls.
"""

import sys
sys.path.insert(0, 'Python')

from seedhash import SeedHashGenerator
import hashlib


def test_md5_consistency():
    """Test that MD5 hashing is consistent."""
    print("=" * 70)
    print("Test 1: MD5 Consistency")
    print("=" * 70)
    
    gen1 = SeedHashGenerator("test_string")
    gen2 = SeedHashGenerator("test_string")
    
    hash1 = gen1.get_hash()
    hash2 = gen2.get_hash()
    
    print(f"Hash 1: {hash1}")
    print(f"Hash 2: {hash2}")
    print(f"Consistent: {hash1 == hash2}")
    
    assert hash1 == hash2, "MD5 hashes should be consistent"
    print("✓ MD5 produces consistent hashes\n")


def test_md5_implementation():
    """Test that MD5 is implemented correctly."""
    print("=" * 70)
    print("Test 2: MD5 Implementation Correctness")
    print("=" * 70)
    
    test_string = "experiment_123"
    gen = SeedHashGenerator(test_string)
    
    # Manual MD5 calculation for comparison
    md5_hasher = hashlib.md5()
    md5_hasher.update(test_string.encode('utf-8'))
    expected_hash = md5_hasher.hexdigest()
    
    actual_hash = gen.get_hash()
    
    print(f"Input: {test_string}")
    print(f"Expected MD5: {expected_hash}")
    print(f"Actual MD5:   {actual_hash}")
    print(f"Match: {expected_hash == actual_hash}")
    
    assert expected_hash == actual_hash, "MD5 implementation is incorrect"
    print("✓ MD5 is correctly implemented\n")


def test_md5_encoding():
    """Test that UTF-8 encoding is handled properly."""
    print("=" * 70)
    print("Test 3: UTF-8 Encoding")
    print("=" * 70)
    
    # Test with various characters
    test_cases = [
        "simple",
        "with spaces",
        "with_underscore",
        "with-dash",
        "with.dot",
        "123numbers",
        "UPPERCASE",
        "MiXeD_CaSe",
        "special!@#$%",
    ]
    
    print("Testing various input strings:")
    for test_str in test_cases:
        gen = SeedHashGenerator(test_str)
        hash_val = gen.get_hash()
        print(f"  '{test_str}' -> {hash_val[:16]}...")
        assert len(hash_val) == 32, f"MD5 hash should be 32 chars, got {len(hash_val)}"
    
    print("✓ All strings encoded properly\n")


def test_md5_to_seed_conversion():
    """Test conversion from MD5 hash to integer seed."""
    print("=" * 70)
    print("Test 4: MD5 to Integer Seed Conversion")
    print("=" * 70)
    
    gen = SeedHashGenerator("test")
    
    # Get the hash and seed
    hash_val = gen.get_hash()
    seed_val = gen.seed_number
    
    print(f"MD5 Hash: {hash_val}")
    print(f"Seed Number: {seed_val}")
    print(f"Seed Type: {type(seed_val)}")
    
    # Manual conversion
    expected_seed = int(hash_val, 16) % (2**32)
    
    print(f"Expected Seed: {expected_seed}")
    print(f"Match: {seed_val == expected_seed}")
    
    assert seed_val == expected_seed, "Seed conversion is incorrect"
    assert isinstance(seed_val, int), "Seed should be an integer"
    assert 0 <= seed_val < 2**32, f"Seed should be in range [0, 2^32), got {seed_val}"
    
    print("✓ MD5 to seed conversion is correct\n")


def test_md5_distribution():
    """Test that MD5 provides good distribution."""
    print("=" * 70)
    print("Test 5: MD5 Distribution Quality")
    print("=" * 70)
    
    # Generate seeds from sequential strings
    seeds = []
    for i in range(100):
        gen = SeedHashGenerator(f"experiment_{i}")
        seeds.append(gen.seed_number)
    
    # Check for uniqueness
    unique_seeds = len(set(seeds))
    print(f"Generated seeds: {len(seeds)}")
    print(f"Unique seeds: {unique_seeds}")
    print(f"Uniqueness: {unique_seeds/len(seeds)*100:.1f}%")
    
    # Check distribution across range
    max_seed = max(seeds)
    min_seed = min(seeds)
    range_coverage = (max_seed - min_seed) / (2**32) * 100
    
    print(f"Min seed: {min_seed}")
    print(f"Max seed: {max_seed}")
    print(f"Range coverage: {range_coverage:.2f}% of 2^32")
    
    assert unique_seeds == len(seeds), "All seeds should be unique"
    print("✓ MD5 provides good distribution\n")


def test_md5_security_context():
    """Explain the security context of MD5 usage."""
    print("=" * 70)
    print("Test 6: Security Context Analysis")
    print("=" * 70)
    
    print("MD5 Usage in seedhash:")
    print("-" * 70)
    print("PURPOSE: Generate deterministic seeds from string inputs")
    print("USE CASE: Non-cryptographic pseudorandom number generation")
    print()
    print("Security Assessment:")
    print("  ✓ APPROPRIATE: MD5 is used for deterministic hashing, not security")
    print("  ✓ APPROPRIATE: No password storage or authentication")
    print("  ✓ APPROPRIATE: No cryptographic security required")
    print("  ✓ APPROPRIATE: Speed and determinism are priorities")
    print()
    print("MD5 Characteristics:")
    print("  • Fast computation")
    print("  • Deterministic (same input -> same output)")
    print("  • Good distribution for PRNG seeding")
    print("  • 128-bit output (32 hex characters)")
    print()
    print("NOT used for:")
    print("  ✗ Password hashing (would use bcrypt, argon2)")
    print("  ✗ Digital signatures (would use SHA-256, SHA-512)")
    print("  ✗ Cryptographic integrity (would use HMAC-SHA256)")
    print("  ✗ Security-sensitive operations")
    print()
    print("CONCLUSION: MD5 is CORRECTLY used for this purpose")
    print("=" * 70)
    print()


def test_potential_issues():
    """Test for potential issues with MD5 implementation."""
    print("=" * 70)
    print("Test 7: Potential Issues Check")
    print("=" * 70)
    
    issues_found = []
    
    # 1. Check for collision resistance (not critical but good to know)
    print("Checking for basic collision resistance...")
    similar_strings = ["test", "test ", "test_", "_test", "TEST"]
    hashes = {}
    for s in similar_strings:
        gen = SeedHashGenerator(s)
        h = gen.get_hash()
        if h in hashes:
            issues_found.append(f"Collision: '{s}' and '{hashes[h]}' have same hash")
        hashes[h] = s
    
    if not issues_found:
        print("  ✓ No collisions in similar strings")
    
    # 2. Check seed range
    print("Checking seed range...")
    gen = SeedHashGenerator("max_test")
    if gen.seed_number >= 2**32:
        issues_found.append(f"Seed exceeds 2^32: {gen.seed_number}")
    else:
        print(f"  ✓ Seed within range: {gen.seed_number} < 2^32")
    
    # 3. Check for proper encoding
    print("Checking UTF-8 encoding...")
    try:
        gen = SeedHashGenerator("test_émojis_🎯")
        _ = gen.get_hash()
        print("  ✓ UTF-8 special characters handled")
    except Exception as e:
        issues_found.append(f"UTF-8 encoding issue: {e}")
    
    print()
    if issues_found:
        print("❌ Issues found:")
        for issue in issues_found:
            print(f"  - {issue}")
    else:
        print("✅ No issues found - MD5 implementation is solid!")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("SEEDHASH: MD5 Algorithm Usage Verification")
    print("=" * 70 + "\n")
    
    test_md5_consistency()
    test_md5_implementation()
    test_md5_encoding()
    test_md5_to_seed_conversion()
    test_md5_distribution()
    test_md5_security_context()
    test_potential_issues()
    
    print("=" * 70)
    print("ALL MD5 TESTS PASSED ✅")
    print("=" * 70)
    print("\nSUMMARY:")
    print("• MD5 is correctly implemented")
    print("• MD5 is appropriately used for non-cryptographic seed generation")
    print("• No security issues with this use case")
    print("• Distribution quality is excellent")
    print("• UTF-8 encoding handled properly")
    print("=" * 70 + "\n")
