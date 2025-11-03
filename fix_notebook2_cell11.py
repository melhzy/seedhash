import json

# Load notebook 2
with open('jupyter/02_Hierarchical_Sampling.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print("Fixing Cell 11 in Notebook 2...")

cell_11 = nb['cells'][11]
source = ''.join(cell_11['source'])

if 'stratified_random_sample(' in source:
    # The cell should use SeedSampler, not manager methods
    new_source = """# Stratified sampling ensures balanced coverage
sampler = SeedSampler(master_seed=12345)
samples = sampler.stratified_random_sampling(
    n_samples=100,
    seed_range=(0, 1000),
    n_strata=10
)

print(f"Stratified sample size: {len(samples)}")
print(f"Expected per stratum: ~{100//10}")
print(f"Range: {min(samples)} to {max(samples)}")
print(f"\\nDistribution check (first 30):")
print(sorted(samples)[:30])"""
    
    cell_11['source'] = [new_source]
    print("✅ Fixed Cell 11")

# Save
with open('jupyter/02_Hierarchical_Sampling.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("✅ Notebook 2 saved!")

# Verify
print("\nVerifying...")
with open('jupyter/02_Hierarchical_Sampling.ipynb', 'r', encoding='utf-8') as f:
    nb_check = json.load(f)

deprecated_found = False
for cell in nb_check['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell.get('source', []))
        if 'stratified_random_sample(' in source or 'simple_random_sample(' in source:
            deprecated_found = True

if deprecated_found:
    print("❌ Still has deprecated methods!")
else:
    print("✅ Verification passed! No deprecated methods in source code.")
