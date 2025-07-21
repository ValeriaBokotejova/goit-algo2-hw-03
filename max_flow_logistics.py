import copy
from collections import deque, defaultdict
from colorama import init, Fore

init(autoreset=True)

def edmonds_karp(capacity, adj, source, sink):
    """Compute max flow using Edmonds-Karp (BFS-based Ford-Fulkerson)."""
    flow = 0
    parent = {}
    while True:
        # find one augmenting path
        queue = deque([source])
        parent.clear()
        parent[source] = None
        while queue and sink not in parent:
            u = queue.popleft()
            for v in adj[u]:
                if v not in parent and capacity[u][v] > 0:
                    parent[v] = u
                    queue.append(v)
        if sink not in parent:
            break

        # find path bottleneck
        bottleneck = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            bottleneck = min(bottleneck, capacity[u][v])
            v = u

        # augment flow along that path
        v = sink
        while v != source:
            u = parent[v]
            capacity[u][v] -= bottleneck
            capacity[v][u] += bottleneck
            v = u

        flow += bottleneck

    return flow

def build_logistics_network():
    """Builds the graph: SOURCE → T1/T2 → W1-W4 → S1-S14 → SINK with given capacities."""
    terminals = ['T1','T2']
    warehouses = ['W1','W2','W3','W4']
    stores = [f'S{i}' for i in range(1,15)]
    source, sink = 'SOURCE', 'SINK'

    # (u, v, capacity)
    edges = [
        ('T1','W1',25), ('T1','W2',20), ('T1','W3',15),
        ('T2','W2',10), ('T2','W3',15), ('T2','W4',30),
        ('W1','S1',15), ('W1','S2',10), ('W1','S3',20),
        ('W2','S4',15), ('W2','S5',10), ('W2','S6',25),
        ('W3','S7',20), ('W3','S8',15), ('W3','S9',10),
        ('W4','S10',20),('W4','S11',10),('W4','S12',15),
        ('W4','S13',5), ('W4','S14',10)
    ]

    capacity = defaultdict(lambda: defaultdict(int))
    adj = defaultdict(list)

    def add_edge(u, v, cap):
        capacity[u][v] = cap
        capacity[v][u] = 0
        adj[u].append(v)
        adj[v].append(u)

    # super-source → terminals
    for t in terminals:
        total = sum(c for u,v,c in edges if u == t)
        add_edge(source, t, total)

    # terminal→warehouse & warehouse→store
    for u, v, c in edges:
        add_edge(u, v, c)

    # stores → super-sink
    for s in stores:
        total = sum(c for u,v,c in edges if v == s)
        add_edge(s, sink, total)

    return source, sink, terminals, warehouses, stores, capacity, adj

def main():
    source, sink, terms, whs, stores, cap, adj = build_logistics_network()
    orig = copy.deepcopy(cap)

    # 1) Max flow
    max_flow = edmonds_karp(cap, adj, source, sink)
    print(Fore.MAGENTA + f"\nMax flow: {max_flow} units\n")

    # 2) Terminal → Warehouse
    print(Fore.GREEN + "Terminal → Warehouse flows:")
    for t in terms:
        for w in whs:
            orig_c = orig[t].get(w, 0)
            if orig_c:
                used = orig_c - cap[t][w]
                print(f"  {t}→{w}: {used}")

    # 3) Warehouse → Store
    print(Fore.GREEN + "\nWarehouse → Store flows:")
    for w in whs:
        for s in stores:
            orig_c = orig[w].get(s, 0)
            if orig_c:
                used = orig_c - cap[w][s]
                print(f"  {w}→{s}: {used}")

    # 4) Aggregated Terminal → Store
    term_store = defaultdict(lambda: defaultdict(int))
    for t in terms:
        for w in whs:
            f_tw = orig[t][w] - cap[t][w]
            if f_tw <= 0:
                continue
            for s in stores:
                f_ws = orig[w][s] - cap[w][s]
                if f_ws > 0:
                    alloc = min(f_tw, f_ws)
                    term_store[t][s] += alloc
                    f_tw -= alloc
                    if f_tw == 0:
                        break

    print(Fore.BLUE + "\nTerminal → Store flows:")
    print(f"{'Terminal':<8} {'Store':<5} {'Flow':>5}")
    for t in terms:
        for s in stores:
            f = term_store[t][s]
            if f:
                print(f"{t:<8} {s:<5} {f:>5}")

if __name__ == "__main__":
    main()
