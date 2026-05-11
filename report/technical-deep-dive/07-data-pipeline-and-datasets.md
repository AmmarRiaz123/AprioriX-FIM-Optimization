# 7. Data pipeline and datasets

## 7.1 Transaction file format (`.dat`)

Standard inputs are **one transaction per line**, **space-separated** item identifiers (strings of digits or other tokens). Example:

```text
1 5 9 27
3 5 12
```

**HUIM-weighted lines** (produced by conversion) look like:

```text
1,2.50 5,1.00 9,4.25
```

The loader in `huim_algorithm.py` detects commas to split **item,utility** pairs.

## 7.2 Bundled and referenced datasets

| File / asset | Typical use |
|--------------|-------------|
| `datasets/chess.dat`, `connect.dat`, `accidents.dat` | FIMI-style benchmarks named in `evaluate.py`. |
| `datasets/chess.txt` | Alternate export / sanity (not the primary path in `evaluate.py`). |
| `datasets/online_retail_itemids.dat` | Retail baskets as numeric IDs (after conversion). |
| `datasets/online_retail_utility.dat` | Same baskets with price utilities for HUIM. |
| `datasets/item_mapping.txt` | Human-readable **ID → product name** map from conversion. |
| `datasets/Assignment-1_Data.csv` (optional) | Source for `convert_dataset.py` / `analyze_datasets.py` (not always committed due to size/licensing). |

**Naming consistency:** Scripts sometimes mention `accident.dat` vs `accidents.dat` in comments; **`evaluate.py`** expects **`accidents.dat`**. Align filenames when preparing a fresh machine.

## 7.3 `convert_dataset.py` (Online Retail → FIM)

**Goal:** Turn a course-provided **semicolon-separated** retail table into:

1. **`online_retail_itemids.dat`**: one basket (BillNo) per line, **deduplicated** items as sorted numeric string IDs.
2. **`online_retail_utility.dat`**: same structure with **`item,price`** tokens; prices parsed with European comma decimals normalized to dot floats.
3. **`datasets/item_mapping.txt`**: audit trail for interpreting mined IDs.

**Key logic:**

- Filter `Quantity > 0`, drop null `Itemname`.
- Build **`item_to_id`** from sorted unique names for stable IDs.
- **`defaultdict(set)` per BillNo** ensures duplicate line items in the CSV do not duplicate basket entries.
- Utility dict **`defaultdict(dict)`** keeps **one price per item per bill** (first wins if duplicates existed after cleaning).

**Downstream:** `evaluate.py` references **`online_retail_itemids.dat`** for three-way runs on retail.

## 7.4 `analyze_datasets.py`

Read-only **exploratory report**: row counts, unique bills/items, average items per transaction, qualitative checklist (real-world ✓, FIMI format ✗ until converted, etc.). It helps justify **why** conversion was necessary in the writeup.

## 7.5 `download_dataset.py`

Uses **`kagglehub.dataset_download("aslanahmedov/market-basket-analysis")`** to fetch an external market-basket dataset. **Note:** `kagglehub` is **not** pinned in `requirements.txt`; install separately if you rely on this script.

## 7.6 `scripts/generate_datasets.py`

Synthetic generator:

- Random transactions with lengths in `[min_length, max_length]`.
- Items sampled from `1..num_items` without replacement per line, sorted.

**Caution:** Output filenames **`chess.dat`**, **`connect.dat`**, **`accidents.dat`** overlap with **real benchmark names**. Running this script **overwrites** canonical names unless paths are edited—fine for quick stress tests, dangerous for reproducible paper numbers. Prefer writing to `synthetic_chess.dat` etc. if both are needed.

## 7.7 `run_experiments.bat`

Windows helper that `cd`s into `src` and runs **`benchmark.py`**. As discussed in the evaluation doc, **`benchmark.py` APIs may not match** `vertical_apriori`; prefer `python src/evaluate.py` for authoritative runs.


