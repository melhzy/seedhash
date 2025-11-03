import json

nb = json.load(open('jupyter/02_Hierarchical_Sampling.ipynb', encoding='utf-8'))

print("Checking Notebook 2 for deprecated methods in SOURCE code only...")
print("="*70)

deprecated_found = False
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell.get('source', []))
        
        # Check for deprecated patterns
        if 'simple_random_sample(' in source or 'stratified_random_sample(' in source:
            print(f"\n❌ Cell {i} has deprecated method:")
            print(source)
            print()
            deprecated_found = True

if not deprecated_found:
    print("✅ No deprecated methods found in source code!")
else:
    print("\n" + "="*70)
    print("Need to fix the above cells")
