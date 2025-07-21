import csv
import timeit
from BTrees.OOBTree import OOBTree

"""
Compare BTrees.OOBTree vs. dict for price range queries.
"""

# Configuration
DATA_FILE   = 'generated_items_data.csv'
MIN_PRICE   = 10.0
MAX_PRICE   = 100.0
ITERATIONS  = 100

def add_item_to_tree(tree: OOBTree, item: dict) -> None:
    """Insert item into OOBTree keyed by price."""
    price = item['Price']
    tree.setdefault(price, []).append(item)

def add_item_to_dict(dct: dict, item: dict) -> None:
    """Insert item into dict keyed by ID."""
    dct[item['ID']] = item

def range_query_tree(tree: OOBTree, min_price: float, max_price: float) -> list:
    """Return all items with price in [min_price, max_price]."""
    result = []
    for price, items in tree.items(min_price, max_price):
        result.extend(items)
    return result

def range_query_dict(dct: dict, min_price: float, max_price: float) -> list:
    """Return all items with price in [min_price, max_price]."""
    return [item for item in dct.values()
            if min_price <= item['Price'] <= max_price]

def load_data(path: str):
    """Load CSV into both an OOBTree (by price) and a dict (by ID)."""
    tree = OOBTree()
    dct  = {}
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            item = {
                'ID':       row['ID'],
                'Name':     row['Name'],
                'Category': row['Category'],
                'Price':    float(row['Price'])
            }
            add_item_to_tree(tree, item)
            add_item_to_dict(dct, item)
    return tree, dct

def main():
    # 1) Load data
    tree, dct = load_data(DATA_FILE)

    # 2) Warm up
    range_query_tree(tree, MIN_PRICE, MAX_PRICE)
    range_query_dict(dct, MIN_PRICE, MAX_PRICE)

    # 3) Measure performance
    t_tree = timeit.timeit(
        lambda: range_query_tree(tree, MIN_PRICE, MAX_PRICE),
        number=ITERATIONS
    )
    t_dict = timeit.timeit(
        lambda: range_query_dict(dct, MIN_PRICE, MAX_PRICE),
        number=ITERATIONS
    )

    # 4) Print results
    print(f"\nTotal range_query time for OOBTree: {t_tree:.6f} seconds")
    print(f"Total range_query time for dict: {t_dict:.6f} seconds\n")

if __name__ == '__main__':
    main()
