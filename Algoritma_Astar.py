import pandas as pd
import heapq

# 1. Baca matriks ketetanggaan (berbobot)
df = pd.read_excel('matriks-berbobot.xlsx', index_col=0)

# 2. Bangun graf berbobot
raw_graph = {}
for u in df.index:
    raw_graph[u] = {}
    for v in df.columns:
        w = df.loc[u, v]
        if pd.notna(w) and w > 0:
            raw_graph[u][v] = w

# 3. Baca heuristik
heur_df = pd.read_csv('Fungsi_Heuristik_h_n__ke_CL__Versi_Terbaru_.csv')
raw_heuristics = {row['Simpul']: row['h(n) ke CL'] for _, row in heur_df.iterrows()}

# 4. Standarisasi nama simpul ke uppercase agar konsisten
graph = {u.upper(): {v.upper(): w for v, w in nbrs.items()} 
         for u, nbrs in raw_graph.items()}
heuristics = {u.upper(): h for u, h in raw_heuristics.items()}

# 5. Definisi algoritma A*
def astar(graph, heuristics, start, goal):
    open_set = [(heuristics.get(start, float('inf')), 0, start, [start])]
    visited = set()
    while open_set:
        f, g, current, path = heapq.heappop(open_set)
        if current == goal:
            return path, g
        if current in visited:
            continue
        visited.add(current)
        for neighbor, weight in graph.get(current, {}).items():
            if neighbor in visited:
                continue
            g_new = g + weight
            f_new = g_new + heuristics.get(neighbor, float('inf'))
            heapq.heappush(open_set, (f_new, g_new, neighbor, path + [neighbor]))
    return None, float('inf')

# 6. Jalankan A* untuk BW -> CL
start, goal = 'BW', 'CL'
path, cost = astar(graph, heuristics, start.upper(), goal.upper())

# 7. Cetak hasil lengkap
print("Nodes in graph:", list(graph.keys()))
print("Nodes in heuristics:", list(heuristics.keys()))
print(f"\nStart: {start.upper()}, Goal: {goal.upper()}")
print("\nRute terpendek:", " → ".join(path))
print("Total biaya:", cost)


