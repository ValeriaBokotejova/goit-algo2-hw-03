# goit-algo2-hw-03

# 📈 Graphs & Trees Homework 

Two assignments exploring graph & tree data structures.

---

## Assignment 1: Max-Flow Logistics
- **Goal**: Model a supply network (Terminals → Warehouses → Stores) and compute max flow   
- **Algo**: Edmonds–Karp  
- **Output**:
  - Max flow  
  - Terminal→Warehouse & Warehouse→Store flows  
  - Aggregated Terminal→Store flows  
- **Run**: `python max_flow_logistics.py`

---

## Assignment 2: Range-Query Perf
- **Goal**: Compare price-range queries on **BTrees.OOBTree** vs **dict**  
- **Data**: `generated_items_data.csv` (`ID,Name,Category,Price`)  
- **Steps**:
  - Load into OOBTree (key=Price) & dict (key=ID)  
  - Implement `add_item_to_*` + `range_query_*`  
  - Time **100** queries with `timeit`  
- **Output**:
```bash
Total time OOBTree: X.XXXXXXs
Total time dict: Y.YYYYYYs
```
- **Run**: `python range_query_comparison.py`
