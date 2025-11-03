import json

# Fix Notebook 1
print("Fixing Notebook 1...")
with open('jupyter/01_Complete_SeedHash_Tutorial.ipynb', 'r', encoding='utf-8') as f:
    nb1 = json.load(f)

for cell in nb1['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell.get('source', []))
        if 'subdirectory=Python[all]' in source:
            # Replace the old syntax with new syntax
            new_source = source.replace(
                'git+https://github.com/melhzy/seedhash.git#subdirectory=Python[all]',
                'git+https://github.com/melhzy/seedhash.git#egg=seedhash[all]&subdirectory=Python'
            )
            # Update the cell source (maintaining array format)
            cell['source'] = [new_source]
            print("✅ Fixed Cell in Notebook 1")

with open('jupyter/01_Complete_SeedHash_Tutorial.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb1, f, indent=1, ensure_ascii=False)

print("✅ Notebook 1 fixed and saved!")

# Verify
print("\nVerifying...")
with open('jupyter/01_Complete_SeedHash_Tutorial.ipynb', 'r', encoding='utf-8') as f:
    nb1_check = json.load(f)

old_found = False
new_found = False
for cell in nb1_check['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell.get('source', []))
        if 'subdirectory=Python[all]' in source:
            old_found = True
        if 'egg=seedhash[all]&subdirectory=Python' in source:
            new_found = True

if old_found:
    print("❌ Still has old syntax!")
elif new_found:
    print("✅ Verification passed! New syntax present, old syntax removed.")
else:
    print("⚠️  No install command found (might be commented out)")
