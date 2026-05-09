"""
High-Utility Itemset Mining (HUIM) Algorithm
Optimized with Bitset Parallelism and Fast-Path Utility Calculation.
Inspired by 2022+ Research on Scalable Utility Mining.
"""

def load_transactions_bitsets(filepath):
    transactions = []
    bitsets = {}
    num_transactions = 0
    with open(filepath, 'r') as file:
        for tid, line in enumerate(file):
            transaction = {}
            items = line.strip().split()
            for item_spec in items:
                if ',' in item_spec:
                    item, utility = item_spec.split(',')
                    transaction[item] = float(utility)
                else:
                    item = item_spec
                    transaction[item] = 1.0
                
                if item not in bitsets:
                    bitsets[item] = 0
                bitsets[item] |= (1 << tid)
                
            if transaction:
                transactions.append(transaction)
                num_transactions += 1
    return transactions, bitsets, num_transactions

def huim_mining_optimized(filepath, min_utility_threshold):
    transactions, bitsets, num_transactions = load_transactions_bitsets(filepath)
    
    # Step 1: Calculate item utilities
    item_utils = {}
    is_binary = True
    for tid, transaction in enumerate(transactions):
        for item, utility in transaction.items():
            item_utils[item] = item_utils.get(item, 0) + utility
            if utility != 1.0:
                is_binary = False
            
    # Filter 1-itemsets
    f1_bitsets = {frozenset([item]): bitsets[item] for item, util in item_utils.items() if util >= min_utility_threshold}
    
    high_utility_itemsets = {1: set(f1_bitsets.keys())}
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
                
                l1 = sorted(list(itemset1))[:-1]
                l2 = sorted(list(itemset2))[:-1]
                
                if l1 == l2:
                    candidate = itemset1.union(itemset2)
                    candidates_generated += 1
                    
                    # Optimization: Bitwise AND intersection
                    candidate_bitset = current_itemsets_bitsets[itemset1] & current_itemsets_bitsets[itemset2]
                    
                    if candidate_bitset == 0:
                        continue
                        
                    # Fast Path for Binary Data (Standard FIM)
                    if is_binary:
                        # Count set bits (support)
                        support = bin(candidate_bitset).count('1')
                        candidate_utility = float(len(candidate) * support)
                    else:
                        # Full Utility Calculation for Weighted Data
                        candidate_utility = 0.0
                        temp_bitset = candidate_bitset
                        tid = 0
                        while temp_bitset > 0:
                            if temp_bitset & 1:
                                transaction = transactions[tid]
                                candidate_utility += sum(transaction[item] for item in candidate)
                            temp_bitset >>= 1
                            tid += 1
                    
                    if candidate_utility >= min_utility_threshold:
                        next_itemsets_bitsets[candidate] = candidate_bitset
                        
        if next_itemsets_bitsets:
            high_utility_itemsets[k] = set(next_itemsets_bitsets.keys())
            current_itemsets_bitsets = next_itemsets_bitsets
        else:
            break
        k += 1
        
    return high_utility_itemsets, candidates_generated
