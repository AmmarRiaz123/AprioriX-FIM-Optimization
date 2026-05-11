# 9. Design tradeoffs and limitations

This section collects **technical caveats** that belong in any serious discussion of the implementation—not to diminish the project, but to clarify **what is proven vs what is demonstrated**.

## 9.1 Python integer bitsets vs fixed-width bitmaps

**Design:** `1 << tid` stores transaction *tid* in a bit of a Python **arbitrary-precision integer**.

**Implications:**

- **Scale:** For *n* transactions, integers hold *n* bits. Python handles big integers, but **time** for `&` and especially **`bin(x).count('1')`** grows with the **bit length** of `x`. Industrial miners often use **numpy uint64 arrays**, **bitarray**, or **sparse tidsets** for large *n*.
- **Correctness:** For datasets used in this course (thousands of transactions), the approach is **pragmatic** and easy to read.

**Takeaway:** The project compares **algorithms relative to each other** in the same language/runtime, not absolute peak throughput vs optimized C++ miners.

## 9.2 Subset pruning: classical vs vertical loop

Classical `apriori_gen` explicitly enforces: **every (k−1)-subset of a k-candidate must be frequent**.

The vertical join loops (`optimized_apriori`, `huim_algorithm`) emphasize **prefix joins on the current frequent frontier**. In well-formed Apriori/Eclat implementations, these are meant to be **equivalent** when the join strategy matches the closure properties—**but equivalence is a lemma**, not obvious from a quick read.

**Course recommendation:** If asked in defense/viva, either (a) cite the standard result that prefix joins on sorted frequent itemsets generate **all** and **only** viable candidates when paired with correct pruning, or (b) show **output equivalence** on small exhaustive tests vs `apriori.py`.

## 9.3 HUIM faithfulness vs “HUIM-flavored vertical miner”

The repository’s HUIM module:

- Uses **vertical intersections** for occurrence testing.
- Uses a **binary fast path** utility = `|X| × support` when all weights are 1.
- Does **not** implement full **TWU / EUCS / remaining utility** pruning families found in modern HUIM papers.

The separate document [HUIM_ALGORITHM_DOCUMENTATION.md](../../HUIM_ALGORITHM_DOCUMENTATION.md) discusses **SOTA concepts** at survey level; readers should not conflate that survey depth with **every line** of `huim_algorithm.py`.

**Fair messaging:** “We implemented a **utility-aware vertical miner** informed by HUIM literature,” not “We reproduced algorithm X from paper Y verbatim.”

## 9.4 Benchmark fairness: Apriori vs HUIM thresholds

`evaluate.py` sets:

```python
min_utility_threshold = min_sup_count * 1.0
```

On **binary** data, HUIM’s fast-path utility grows with **|X|** and support; Apriori’s filter is **pure support**. The **sets of accepted itemsets** may differ even at “similar” thresholds.

**Fair runtime comparison:** Both touch the dataset with comparable vertical work; **wall times** are still informative as **engineering measurements** under a shared parameter knob, but **output cardinality** comparisons need careful interpretation.

## 9.5 HUIM runtime control

HUIM is run **only** for the strictest support per dataset in the main loop (`j == 0`) to avoid runaway times. Plots therefore often show **HUIM only at one x position** worth of meaningful data unless `run_remaining.py` or manual calls extend coverage.

## 9.6 Memory measurement

RSS deltas from `psutil` capture **process heap growth** coarsely. They **do not** isolate Python allocator arenas, mmap’d files, or OS page cache effects.

## 9.7 `benchmark.py` / `run_experiments.bat` drift

The batch file still targets **`benchmark.py`**, whose example API does not align with `vertical_apriori`’s signature. This is a **maintainability footgun**; the canonical path is **`evaluate.py`**.

## 9.8 Synthetic generator overwriting FIMI names

`scripts/generate_datasets.py` writes to canonical benchmark filenames. Prefer non-colliding names to protect **reproducible** benchmark artifacts.

---

## Closing thought

The project succeeds at its **learning objectives**: implement recognizable FIM baselines, apply a **clear optimization** (vertical + bitwise intersections), introduce **utility**, and **measure** behavior on real and converted data. The limitations above are the **honest boundary** between a strong course artifact and a production mining library.
