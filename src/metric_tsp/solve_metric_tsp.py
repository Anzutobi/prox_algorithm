import math
import time
import argparse
import itertools


def parse_cities(filepath):
    cities = {}
    order = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            name, x, y = parts[0], float(parts[1]), float(parts[2])
            cities[name] = (x, y)
            order.append(name)
    return cities, order


def euclidean_ceil(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.ceil(math.sqrt(dx * dx + dy * dy))


def build_edges(cities):
    names = list(cities.keys())
    edges = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            u, v = names[i], names[j]
            w = euclidean_ceil(cities[u], cities[v])
            edges.append((w, u, v))
    return edges


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True


def kruskal_mst(cities, edges):
    name_to_idx = {name: i for i, name in enumerate(cities)}
    sorted_edges = sorted(edges, key=lambda e: (e[0], e[1], e[2]))
    uf = UnionFind(len(cities))
    mst_edges = []
    mst_cost = 0
    for w, u, v in sorted_edges:
        if uf.union(name_to_idx[u], name_to_idx[v]):
            mst_edges.append((u, v, w))
            mst_cost += w
    return mst_edges, mst_cost


def build_mst_adj(mst_edges):
    adj = {}
    for u, v, _ in mst_edges:
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    for node in adj:
        adj[node].sort()
    return adj


def dfs_traversal(adj, root):
    order = []
    visited = set()

    def dfs(node):
        visited.add(node)
        order.append(node)
        for neighbor in adj.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)

    dfs(root)
    return order


def compute_tour_cost(tour, cities):
    total = 0
    for i in range(len(tour) - 1):
        total += euclidean_ceil(cities[tour[i]], cities[tour[i + 1]])
    return total


def optimal_tsp(cities, city_order):
    if len(cities) <= 1:
        return city_order[:] + city_order[:1], 0

    start = city_order[0]
    others = city_order[1:]
    n = len(others)
    best_tour = None
    best_cost = float('inf')

    for perm in itertools.permutations(others):
        tour = [start] + list(perm) + [start]
        cost = compute_tour_cost(tour, cities)
        if cost < best_cost:
            best_cost = cost
            best_tour = tour

    return best_tour, best_cost


def format_city_set(cities):
    return ', '.join(f"{name}({x},{y})" for name, (x, y) in cities.items())


def main():
    parser = argparse.ArgumentParser(description="Solve Metric TSP via 2-approximation (MST + DFS)")
    parser.add_argument("--input", "-i", required=True,
                        help="Input city coordinates file")
    parser.add_argument("--root", "-r", type=str, default=None,
                        help="Root node for DFS (default: first city)")
    args = parser.parse_args()

    cities, city_order = parse_cities(args.input)
    root = args.root if args.root is not None else city_order[0]

    t0 = time.perf_counter()

    edges = build_edges(cities)
    mst_edges, mst_cost = kruskal_mst(cities, edges)
    mst_adj = build_mst_adj(mst_edges)
    dfs_order = dfs_traversal(mst_adj, root)
    tsp_tour = dfs_order + [root]
    tsp_cost = compute_tour_cost(tsp_tour, cities)

    elapsed = time.perf_counter() - t0

    opt_tour, opt_cost = optimal_tsp(cities, city_order)
    approx_ratio = tsp_cost / opt_cost if opt_cost > 0 else 1.0

    print(f"城市数量：{len(cities)}")
    print(f"根节点：{root}")
    print("最小生成树 MST 边集：")
    for u, v, w in mst_edges:
        print(f"({u}, {v}, {w})")
    print(f"MST 总代价：{mst_cost}")
    print("DFS 遍历顺序：")
    print(' -> '.join(dfs_order))
    print("TSP 近似回路：")
    print(' -> '.join(tsp_tour))
    print(f"TSP 近似回路总代价：{tsp_cost}")
    print(f"2 * MST 总代价：{2 * mst_cost}")
    print("最优 TSP 回路：")
    print(' -> '.join(opt_tour))
    print(f"最优 TSP 回路总代价：{opt_cost}")
    print(f"近似比例：{tsp_cost} / {opt_cost} = {approx_ratio:.3f}")
    print(f"运行时间：{elapsed:.3f}s")


if __name__ == "__main__":
    main()
