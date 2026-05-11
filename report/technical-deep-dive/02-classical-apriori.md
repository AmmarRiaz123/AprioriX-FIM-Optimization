# 2. Classical Apriori (`src/apriori.py`)

## 2.1 Purpose in the project

`apriori.py` is the **reference baseline**. Every optimization claim in the project is ultimately compared against this implementation. It follows the textbook **horizontal database** formulation: each transaction is a **set** of item strings, and candidate supports are computed by testing `candidate ⊆ transaction` across the whole database for each level *k*.

## 2.2 Data loading: `load_transactions`

```1:6:src/apriori.py
def load_transactions(filepath):
    transactions = []
    with open(filepath, 'r') as file:
        for line in file:
            transactions.append(set(line.strip().split()))
    return transactions
```

**Design choices:**

- **Whitespace-separated tokens** per line = one transaction. This matches common **FIMI** `.dat` layouts (integers as strings are fine).
- **`set` per row**: membership tests for candidates are **O(|transaction|)** average case instead of O(length) list scans.
- **All items as strings**: consistent with file I/O; no global reindexing pass (unlike some high-performance miners that remap to dense `0..n-1` integers).

**Tradeoff:** Building many small sets has Python object overhead; the vertical miner avoids per-transaction objects for counting (it never materializes the full horizontal DB in `optimized_apriori.py`).

## 2.3 Frequent 1-itemsets: `get_frequent_1_itemsets`

```8:17:src/apriori.py
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
```

**Thinking:** Level *k=1* is cheap: a single linear scan, counting per item. Outputs **`frozenset` singletons** so itemsets are hashable and can live in `set`/`dict` keys later—important for Apriori’s set algebra.

**Threshold:** `min_sup_count` is an **absolute count** (not a ratio). The caller (`evaluate.py`) converts a ratio × `|D|` to an integer.

## 2.4 Candidate generation: `apriori_gen`

```20:50:src/apriori.py
def apriori_gen(fk_minus_1, k):
    candidates = set()
    fk_list = sorted([sorted(list(itemset)) for itemset in fk_minus_1])
    
    # Group by prefix (first k-2 items)
    for i in range(len(fk_list)):
        for j in range(i + 1, len(fk_list)):
            l1 = fk_list[i][:k-2]
            l2 = fk_list[j][:k-2]
            
            if l1 == l2:
                # Potential candidate
                c1 = frozenset(fk_list[i])
                c2 = frozenset(fk_list[j])
                candidate = c1.union(c2)
                
                # Pruning step (Apriori property)
                is_valid = True
                for item in candidate:
                    subset = candidate - frozenset([item])
                    if subset not in fk_minus_1:
                        is_valid = False
                        break
                if is_valid:
                    candidates.add(candidate)
            else:
                # Since fk_list is sorted, if prefixes don't match, 
                # we can break the inner loop early if we want, 
                # but simple prefix check is already much faster than before.
                break 
    return candidates
```

**Algorithmic idea (join step):** For *k ≥ 2*, sort frequent *(k−1)*-itemsets lexicographically. Pairs with identical **(k−2)-prefix** may join to a size-*k* candidate (standard **Apriori join**).

**Pruning (subset test):** For each candidate *C*, every *(k−1)*-subset must be frequent—otherwise *C* cannot be frequent (anti-monotonicity of support). The code checks each subset’s membership in `fk_minus_1` (as a `set` of `frozenset`s for O(1) lookups).

**Early `break`:** Once `l1 != l2` for sorted `fk_list`, the inner `j` loop breaks. Because rows are sorted lexicographically, further `j` values would only increase the prefix lexicographically; they cannot match `fk_list[i]`’s prefix at position *k−2* in a way that revives equality **for this fixed inner structure**. This is a **micro-optimization** to cut useless inner iterations.

**Complexity sketch:** O(|F_{k-1}|²) join pairs in worst case before pruning; pruning adds O(k) subset checks per surviving join. Dense datasets at low support blow up candidate counts—this is exactly what the project measures empirically.

## 2.5 Main loop: `apriori`

```52:74:src/apriori.py
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
```

**Indexing detail:** After processing level *k*, the code stores results under key **`k-1`** in `frequent_itemsets` (because `f1` was stored when `k` became 2, etc.). Callers that sum `len(v)` across values still get correct **total itemset counts**, but key semantics are “size of itemsets in this bucket.”

**Main performance bottleneck:** Nested loops `for transaction` × `for candidate` with `issubset`. This is **O(|D| × |C_k| × cost_subset)** per level—quadratic-ish behavior when `|C_k|` explodes.

**`total_candidates_generated`:** Accumulates |C_k| across levels for **benchmarking** and narrative in reports (“how hard did the join/prune phase work?”).

## 2.6 How this module interacts with the rest

- **`evaluate.py`** loads the same file once into memory for Apriori, then passes `(transactions, min_sup_count)`.
- **`optimized_apriori.py`** reimplements the **join condition** (prefix equality) but replaces the counting loop with **bitset AND + popcount**.

## 2.7 Pedagogical summary

Strength: **transparent**, easy to map to lecture pseudocode and complexity proofs.  
Weakness: **worst-case counting cost** on dense data and low support—precisely where vertical methods shine.
