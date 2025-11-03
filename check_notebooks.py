import json

nb1 = json.load(open('jupyter/01_Complete_SeedHash_Tutorial.ipynb', 'r', encoding='utf-8'))
nb2 = json.load(open('jupyter/02_Hierarchical_Sampling.ipynb', 'r', encoding='utf-8'))

print("Notebook 1:")
for i, cell in enumerate(nb1['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell.get('source', []))
        if 'pip install' in source:
            print(f"Cell {i}: {source[:100]}")
            if 'subdirectory=Python[all]' in source:
                print("  ❌ HAS OLD SYNTAX")
            if 'egg=seedhash[all]&subdirectory=Python' in source:
                print("  ✅ HAS NEW SYNTAX")

print("\nNotebook 2:")
for i, cell in enumerate(nb2['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell.get('source', []))
        if 'pip install' in source:
            print(f"Cell {i}: {source[:100]}")
            if 'subdirectory=Python[all]' in source:
                print("  ❌ HAS OLD SYNTAX")
            if 'egg=seedhash[all]&subdirectory=Python' in source:
                print("  ✅ HAS NEW SYNTAX")
