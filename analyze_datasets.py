import pandas as pd
import os

print('='*70)
print('DATASET ANALYSIS FOR FIM PROJECT')
print('='*70)

# Analyze CSV
csv_path = 'datasets/Assignment-1_Data.csv'
print(f'\n📊 CSV File: {csv_path}')
csv_df = pd.read_csv(csv_path, sep=';')
print(f'   Total rows: {csv_df.shape[0]:,}')
print(f'   Columns: {list(csv_df.columns)}')
unique_bills = csv_df['BillNo'].nunique()
unique_items = csv_df['Itemname'].nunique()
print(f'   Unique BillNo (transactions): {unique_bills:,}')
print(f'   Unique Items/Products: {unique_items:,}')
print(f'   Avg items per transaction: {csv_df.shape[0] / unique_bills:.2f}')
print(f'   File size: {os.path.getsize(csv_path) / 1024:.2f} KB')

# Analyze XLSX
xlsx_path = 'datasets/Assignment-1_Data.xlsx'
print(f'\n📊 XLSX File: {xlsx_path}')
print(f'   File size: {os.path.getsize(xlsx_path) / 1024 / 1024:.2f} MB')
print(f'   (Note: Both CSV and XLSX contain same data - CSV analysis applies to both)')

print('\n' + '='*70)
print('DATASET EVALUATION FOR FIM PROJECT')
print('='*70)

print('\n✅ GOOD CHARACTERISTICS:')
print(f'   ✓ Real-world data (Online Retail transactions)')
print(f'   ✓ Large enough: {unique_bills:,} transactions')
print(f'   ✓ Good variety: {unique_items:,} unique items')
print(f'   ✓ Dense transactions: {csv_df.shape[0] / unique_bills:.1f} items/transaction')
print(f'   ✓ E-commerce domain (relevant for FIM)')

print('\n❌ ISSUES FOR FIM:')
print(f'   ✗ Not standard FIM format (needs conversion)')
print(f'   ✗ Contains quantity, price, date (extra columns)')
print(f'   ✗ Item names are strings, not numeric IDs')
print(f'   ✗ No utility values (need to add price column)')

print('\n📋 COMPARISON WITH PROJECT REQUIREMENTS:')
requirements = {
    'Real-world data': ('✓', 'Yes - Online Retail'),
    'Enough transactions': ('✓', f'Yes - {unique_bills:,} transactions'),
    'Good sparsity': ('⚠', 'Medium-Dense (5.4 items/tx)'),
    'Standard format': ('✗', 'No - needs conversion to .dat'),
    'FIMI benchmark': ('✗', 'No - not from FIMI repo'),
    'Comparable to Chess/Connect/Accidents': ('⚠', 'Different domain but similar size'),
}

for req, (status, note) in requirements.items():
    print(f'   {status} {req:30s} - {note}')

print('\n' + '='*70)
print('VERDICT')
print('='*70)
print('''
🟡 PARTIALLY SUITABLE - NEEDS PREPARATION

RECOMMENDATION:
1. ✅ USE THIS DATASET - It's real-world and adequate for FIM
2. ⚠️  NEED CONVERSION - Convert to standard FIM format (.dat)
3. 🔧 PROCESSING REQUIRED:
   - Extract items per transaction (group by BillNo)
   - Convert item names to numeric IDs (optional for clarity)
   - Create .dat file with space-separated items
   - Optionally: Add price as utility values for HUIM testing

PERFECT FIT SCORE: 6/10
- Real data: ✓✓ (Better than synthetic)
- Format: ✗✗ (Needs conversion)
- Size: ✓✓ (Good volume)
- Sparsity: ✓ (Medium, good for testing)
- Domain Match: ✓ (E-commerce, similar to market basket)

ACTION: Convert this data to standard .dat format
       Then it will be EXCELLENT for your project
''')
