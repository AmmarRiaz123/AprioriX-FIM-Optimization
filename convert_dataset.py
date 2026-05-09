"""
Dataset Conversion Script - SIMPLIFIED
Convert Online Retail CSV to FIM Standard .dat Format
"""

import pandas as pd
import os
from collections import defaultdict

print('='*70)
print('ONLINE RETAIL DATASET CONVERSION (SIMPLIFIED)')
print('='*70)

# Read CSV
csv_path = 'datasets/Assignment-1_Data.csv'
print(f'\nReading: {csv_path}')
df = pd.read_csv(csv_path, sep=';', dtype={'BillNo': str}, low_memory=False)

# Remove cancelled transactions and invalid data
print(f'   Original rows: {len(df):,}')
df = df[df['Quantity'] > 0]
df = df[df['Itemname'].notna()]  # Remove NaN itemnames
print(f'   After cleaning: {len(df):,}')

# Create item ID mapping (sorted for consistency)
print(f'\nCreating item mappings...')
unique_items = sorted(df['Itemname'].dropna().unique())
item_to_id = {item: str(i+1) for i, item in enumerate(unique_items)}
print(f'   Total unique items: {len(item_to_id):,}')

# Group transactions by BillNo using sets to avoid duplicates
print(f'\nGrouping items by transaction...')
transactions = defaultdict(set)
for idx, row in df.iterrows():
    bill_id = str(row['BillNo'])
    item_name = row['Itemname']
    if pd.notna(item_name) and item_name in item_to_id:
        item_id = item_to_id[item_name]
        transactions[bill_id].add(item_id)

# Convert sets to sorted lists
transaction_list = []
for bill_id in sorted(transactions.keys()):
    items = sorted(list(transactions[bill_id]))
    if len(items) > 0:
        transaction_list.append(items)

print(f'   Total unique BillNo: {len(transactions):,}')
print(f'   Non-empty transactions: {len(transaction_list):,}')

# ==== VERSION 1: Standard FIM Format (Numeric IDs) ====
output_path_ids = 'datasets/online_retail_itemids.dat'
print(f'\nWriting: {output_path_ids}')
with open(output_path_ids, 'w') as f:
    for items in transaction_list:
        f.write(' '.join(items) + '\n')
file_size_1 = os.path.getsize(output_path_ids) / 1024
print(f'   - {len(transaction_list):,} transactions written')
print(f'   File size: {file_size_1:.2f} KB')

# ==== VERSION 2: Create with utility values (Price for HUIM) ====
print(f'\nWriting utility-weighted version for HUIM...')
transactions_util = defaultdict(dict)  # bill_id -> {item_id: price}
for idx, row in df.iterrows():
    bill_id = str(row['BillNo'])
    item_name = row['Itemname']
    # Handle European decimal format (2,55 → 2.55)
    price_str = str(row['Price']).replace(',', '.') if pd.notna(row['Price']) else '1.0'
    try:
        price = float(price_str)
    except ValueError:
        price = 1.0
    
    if pd.notna(item_name) and item_name in item_to_id:
        item_id = item_to_id[item_name]
        if item_id not in transactions_util[bill_id]:
            transactions_util[bill_id][item_id] = price

output_path_utility = 'datasets/online_retail_utility.dat'
with open(output_path_utility, 'w') as f:
    for bill_id in sorted(transactions_util.keys()):
        item_prices = transactions_util[bill_id]
        # Format: item1,utility1 item2,utility2 ...
        entries = [f"{item_id},{price:.2f}" for item_id, price in sorted(item_prices.items())]
        if entries:
            f.write(' '.join(entries) + '\n')

file_size_2 = os.path.getsize(output_path_utility) / 1024
print(f'   - Utility file created with price values')
print(f'   File size: {file_size_2:.2f} KB')

# ==== STATISTICS ====
print(f'\n' + '='*70)
print('CONVERSION SUMMARY')
print('='*70)

avg_items = sum(len(items) for items in transaction_list) / len(transaction_list) if transaction_list else 0
min_items = min(len(items) for items in transaction_list) if transaction_list else 0
max_items = max(len(items) for items in transaction_list) if transaction_list else 0
density = avg_items / len(item_to_id) * 100 if len(item_to_id) > 0 else 0

print(f'\nDataset Statistics:')
print(f'   Transactions: {len(transaction_list):,}')
print(f'   Unique Items: {len(item_to_id):,}')
print(f'   Avg items/transaction: {avg_items:.2f}')
print(f'   Min items/transaction: {min_items}')
print(f'   Max items/transaction: {max_items}')
print(f'   Density: {density:.2f}%')

print(f'\nGenerated Files:')
print(f'   1. online_retail_itemids.dat ({file_size_1:.2f} KB)')
print(f'      -> Standard FIM format (numeric item IDs)')
print(f'      -> Use this for Classical Apriori & Optimized Apriori')
print(f'\n   2. online_retail_utility.dat ({file_size_2:.2f} KB)')
print(f'      -> HUIM format (item,utility pairs with prices)')
print(f'      -> Use this for HUIM algorithm testing')

# ==== CREATE ITEM MAPPING REFERENCE ====
print(f'\nCreating item mapping reference...')
mapping_path = 'datasets/item_mapping.txt'
with open(mapping_path, 'w', encoding='utf-8') as f:
    f.write('Online Retail Dataset - Item ID to Product Mapping\n')
    f.write('=' * 80 + '\n\n')
    f.write(f'Total Items: {len(item_to_id)}\n\n')
    f.write('Format: ID -> Product Name\n')
    f.write('-' * 80 + '\n\n')
    for item_name, item_id in sorted(item_to_id.items(), key=lambda x: int(x[1])):
        # Truncate long names for readability
        short_name = item_name[:70]
        f.write(f'{item_id:5s} -> {short_name}\n')

print(f'   - Mapping file created: {mapping_path}')

print(f'\n' + '='*70)
print('CONVERSION COMPLETE!')
print('='*70)

print(f'\nNEXT STEPS:')
print(f'   1. Use "online_retail_itemids.dat" for benchmarking')
print(f'   2. Update evaluate.py to include this dataset')
print(f'   3. Run benchmarks with all 3 algorithms')
print(f'   4. Compare with synthetic datasets (chess, connect, accidents)')
print(f'   5. Use utility version for HUIM advanced testing')

print(f'\nDATASET READY FOR BLOCKER 2 COMPLETION!')
