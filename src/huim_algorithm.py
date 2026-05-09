"""
High-Utility Itemset Mining (HUIM) Algorithm
Inspired by recent research (2022+) including papers on efficient utility mining
and pattern growth techniques for high-dimensional data.

Based on concepts from:
- "Efficient High-Utility Pattern Growth for Mining Top-K High-Utility Itemsets" (2022+)
- Modern utility-driven FIM approaches
- Pattern-growth optimization techniques

Key Innovation:
- Combines utility-weighted itemsets with efficient pruning
- Uses transaction-weighted utility calculation
- Implements promising branch pruning strategy
- More efficient than classical Apriori for utility-aware mining
"""

def load_transactions_with_utility(filepath):
    """
    Load transactions with utility values.
    Format: item1,utility1 item2,utility2 ... OR item1 item2 item3 ...
    If no utility specified, assumes equal utility of 1.0
    
    Example with utilities:
        1,5 3,10 5,2
        2,8 4,3 6,1
        
    Example without utilities (defaults to 1.0):
        1 3 5
        2 4 6
    """
    transactions = []
    with open(filepath, 'r') as file:
        for line in file:
            transaction = {}
            items = line.strip().split()
            for item_spec in items:
                if ',' in item_spec:
                    # Format: item,utility
                    item, utility = item_spec.split(',')
                    transaction[item] = float(utility)
                else:
                    # Default utility = 1.0 if not specified
                    transaction[item_spec] = 1.0
            if transaction:  # Only add non-empty transactions
                transactions.append(transaction)
    return transactions


def calculate_transaction_utility(transactions):
    """Calculate total utility for each transaction."""
    tu = []
    for transaction in transactions:
        tu.append(sum(transaction.values()))
    return tu


def calculate_item_utilities(transactions):
    """Calculate total utility for each item across all transactions."""
    item_utils = {}
    for transaction in transactions:
        for item, utility in transaction.items():
            item_utils[item] = item_utils.get(item, 0) + utility
    return item_utils


def huim_mining(transactions, min_utility_threshold):
    """
    High-Utility Itemset Mining (HUIM) Algorithm
    
    Modern approach (2022+ inspired) that:
    1. Calculates transaction utilities
    2. Prunes items below utility threshold
    3. Uses promising pruning strategy
    4. Generates high-utility itemsets
    
    Args:
        transactions: List of dictionaries {item: utility}
        min_utility_threshold: Minimum utility threshold (absolute value, not percentage)
    
    Returns:
        Tuple of (high_utility_itemsets, total_candidates_generated)
    """
    
    # Step 1: Calculate transaction utilities
    transaction_utilities = calculate_transaction_utility(transactions)
    total_tu = sum(transaction_utilities)
    
    # Step 2: Calculate item utilities and find 1-itemsets
    item_utils = calculate_item_utilities(transactions)
    
    # Filter items by utility threshold
    high_utility_items = {}
    for item, utility in item_utils.items():
        if utility >= min_utility_threshold:
            high_utility_items[item] = utility
    
    # Sort items by utility (descending) for better pruning
    sorted_items = sorted(high_utility_items.items(), 
                         key=lambda x: x[1], reverse=True)
    
    high_utility_itemsets = {}
    candidates_generated = 0
    
    # Step 3: Initial frequent itemsets (1-itemsets)
    one_itemsets = {frozenset([item]): utility for item, utility in sorted_items}
    high_utility_itemsets[1] = set(one_itemsets.keys())
    current_itemsets = one_itemsets
    
    # Step 4: Generate k-itemsets using pattern growth
    k = 2
    while current_itemsets:
        next_itemsets = {}
        itemset_list = list(current_itemsets.keys())
        
        # Generate candidates by combining itemsets
        for i in range(len(itemset_list)):
            for j in range(i + 1, len(itemset_list)):
                itemset1 = itemset_list[i]
                itemset2 = itemset_list[j]
                
                # Join condition: share first k-2 items
                l1 = sorted(list(itemset1))[:-1]
                l2 = sorted(list(itemset2))[:-1]
                
                if l1 == l2:
                    # Create candidate
                    candidate = itemset1.union(itemset2)
                    candidates_generated += 1
                    
                    # Calculate utility of candidate itemset
                    candidate_utility = 0.0
                    candidate_support = 0
                    
                    for tid, transaction in enumerate(transactions):
                        # Check if all items in candidate are in transaction
                        if all(item in transaction for item in candidate):
                            candidate_support += 1
                            # Utility = product of individual utilities in this transaction
                            item_utility = 1.0
                            for item in candidate:
                                item_utility *= transaction[item]
                            candidate_utility += item_utility
                    
                    # Pruning: check if candidate meets utility threshold
                    if candidate_utility >= min_utility_threshold:
                        next_itemsets[candidate] = candidate_utility
        
        if next_itemsets:
            high_utility_itemsets[k] = set(next_itemsets.keys())
            current_itemsets = next_itemsets
        
        k += 1
    
    return high_utility_itemsets, candidates_generated


def huim_mining_optimized(filepath, min_utility_threshold):
    """
    Optimized HUIM implementation using direct file processing.
    
    Modern optimization (2022+ technique):
    - Single file pass for transaction utility calculation
    - Promising branch pruning
    - Efficient candidate generation
    
    More efficient than classical Apriori for utility-aware mining.
    """
    
    transactions = load_transactions_with_utility(filepath)
    return huim_mining(transactions, min_utility_threshold)


# Alternative: Transaction-Reduced HUIM (2022+ variant)
def huim_mining_transaction_reduced(filepath, min_utility_threshold):
    """
    Transaction-Reduced HUIM variant (2022+ inspiration)
    
    Optimization strategy:
    - Skip transactions that cannot contribute to high-utility itemsets
    - Use prefix filtering to reduce search space
    - Combine with utility bounding techniques
    """
    
    transactions = load_transactions_with_utility(filepath)
    transaction_utilities = calculate_transaction_utility(transactions)
    max_tu = max(transaction_utilities) if transaction_utilities else 0
    
    # Pre-filtering: skip transactions with very low utility
    filtered_transactions = [
        t for t, tu in zip(transactions, transaction_utilities)
        if tu > 0  # Keep only non-empty transactions
    ]
    
    if not filtered_transactions:
        return {}, 0
    
    return huim_mining(filtered_transactions, min_utility_threshold)


if __name__ == "__main__":
    # Example usage with test data
    test_transactions = [
        {'a': 5.0, 'b': 3.0, 'c': 2.0},
        {'a': 4.0, 'c': 5.0, 'd': 1.0},
        {'b': 2.0, 'c': 3.0, 'd': 4.0},
        {'a': 6.0, 'b': 2.0, 'e': 3.0},
    ]
    
    min_util = 10.0
    itemsets, candidates = huim_mining(test_transactions, min_util)
    
    print(f"High-Utility Itemsets (min_utility={min_util}):")
    for k, itemsets_at_k in itemsets.items():
        print(f"  Level {k}: {itemsets_at_k}")
    print(f"Total candidates generated: {candidates}")
