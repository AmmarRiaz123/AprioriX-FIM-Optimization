"""
Optimized Apriori using Vertical Data Format and Bit-level Parallelism.
Optimization Strategy:
1. Vertical Data Formatting (TID-lists)
2. Bitset Intersection (Bit-level Parallelism)
"""

def load_transactions_bitsets(filepath):
    bitsets = {}
    num_transactions = 0
    with open(filepath, 'r') as file:
        for tid, line in enumerate(file):
            items = line.strip().split()
            for item in items:
                if item not in bitsets:
                    bitsets[item] = 0
                bitsets[item] |= (1 << tid)
            num_transactions += 1
    return bitsets, num_transactions

def vertical_apriori(filepath, min_sup_count):
    bitsets, num_transactions = load_transactions_bitsets(filepath)
    
    # Filter frequent 1-itemsets
    f1_bitsets = {}
    for item, bitset in bitsets.items():
        support = bin(bitset).count('1')
        if support >= min_sup_count:
            f1_bitsets[frozenset([item])] = bitset
            
    frequent_itemsets = {1: set(f1_bitsets.keys())}
    current_itemsets_bitsets = f1_bitsets
    k = 2
    candidates_generated = 0
    
    while current_itemsets_bitsets:
        next_itemsets_bitsets = {}
        itemset_list = list(current_itemsets_bitsets.keys())
        
        for i in range(len(itemset_list)):
            for j in range(i + 1, len(itemset_list)):
                itemset1 = itemset_list[i]
                itemset2 = itemset_list[j]
                
                # Join condition (same prefix)
                l1 = sorted(list(itemset1))[:-1]
                l2 = sorted(list(itemset2))[:-1]
                
                if l1 == l2:
                    candidate = itemset1.union(itemset2)
                    candidates_generated += 1
                    
                    # Optimization: Bitwise AND intersection (Fast)
                    candidate_bitset = current_itemsets_bitsets[itemset1] & current_itemsets_bitsets[itemset2]
                    
                    # Count support using bitset population count
                    support = bin(candidate_bitset).count('1')
                    
                    if support >= min_sup_count:
                        next_itemsets_bitsets[candidate] = candidate_bitset
                        
        if next_itemsets_bitsets:
            frequent_itemsets[k] = set(next_itemsets_bitsets.keys())
            current_itemsets_bitsets = next_itemsets_bitsets
        else:
            break
        k += 1
        
    return frequent_itemsets, candidates_generated
