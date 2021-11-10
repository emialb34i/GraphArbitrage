import math
from collections import defaultdict

def bellmanford(g, s):
    n = len(g.nodes())
    d = defaultdict(lambda: math.inf)
    p = defaultdict(lambda: -1)
    d[s] = 0

    for _ in range(n-1):
        for u,v in g.edges():
            w = g[u][v]["weight"]
            # relaxation
            if d[u] + w < d[v]:
                d[v] = d[u] + w
                p[v] = u
    
    all_cycles = []
    seen = defaultdict(lambda: False)
    
    # check fo negative cycle
    for u,v in g.edges():
        if seen[v]:
            continue
        w = g[u][v]["weight"]
        if d[u] + w < d[v]:
            cycle = []
            x = v
            while True:
                seen[x] = True
                cycle.append(x)
                x = p[x]
                if x == v or x in cycle:
                    break
            idx = cycle(x)
            cycle.append(x)
            all_cycles.append(cycle[idx:][::-1])
    
    return all_cycles
