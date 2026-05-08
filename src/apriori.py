def load_transactions(filepath):
    transactions = []
    with open(filepath, 'r') as file:
        for line in file:
            transactions.append(set(line.strip().split()))
    return transactions

def get_frequent_1_itemsets(transactions, min_sup_count):
    item_counts = {}
    for transaction in transactions:
        for item in transaction:
            item_counts[item] = item_counts.get(item, 0) + 1
            
    f1 = []
    for item, count in item_counts.items():
        if count >= min_sup_count:
            f1.append(frozenset([item]))
    return f1

def apriori_gen(fk_minus_1, k):
    candidates = set()
    fk_list = list(fk_minus_1)
    for i in range(len(fk_list)):
        for j in range(i + 1, len(fk_list)):
            l1 = list(fk_list[i])[:k-2]
            l2 = list(fk_list[j])[:k-2]
            l1.sort()
            l2.sort()
            if l1 == l2: 
                candidate = fk_list[i].union(fk_list[j])
                # Pruning step (Apriori property)
                is_valid = True
                for item in candidate:
                    subset = candidate - frozenset([item])
                    if subset not in fk_minus_1:
                        is_valid = False
                        break
                if is_valid:
                    candidates.add(candidate)
    return candidates

def apriori(transactions, min_sup_count):
    frequent_itemsets = {}
    f1 = get_frequent_1_itemsets(transactions, min_sup_count)
    fk = set(f1)
    k = 2
    
    total_candidates_generated = 0
    
    while fk:
        frequent_itemsets[k-1] = fk
        candidates = apriori_gen(fk, k)
        total_candidates_generated += len(candidates)
        
        item_counts = {c: 0 for c in candidates}
        for transaction in transactions:
            for candidate in candidates:
                if candidate.issubset(transaction):
                    item_counts[candidate] += 1
                    
        fk = set(c for c, count in item_counts.items() if count >= min_sup_count)
        k += 1
        
    return frequent_itemsets, total_candidates_generated
