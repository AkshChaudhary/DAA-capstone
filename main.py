import csv
from pathlib import Path
from collections import deque

# ==========================================
# MINI COURIER PLANNER
# PHASE 1: PROBLEM DESIGN AND PLANNING
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# ==========================================
# 1. LOAD LOCATIONS
# ==========================================

def load_locations():
    locations = {}

    file_path = DATA_DIR / "locations.csv"

    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            location_id = int(row["id"])
            name = row["name"].strip()

            if location_id in locations:
                raise ValueError("Duplicate location ID found.")

            if not name:
                raise ValueError("Location name cannot be empty.")

            locations[location_id] = name

    if not locations:
        raise ValueError("No locations found.")

    expected_ids = set(range(1, len(locations) + 1))

    if set(locations.keys()) != expected_ids:
        raise ValueError("Location IDs must start from 1 without gaps.")

    return locations

# ==========================================
# 2. LOAD ROADS
# ==========================================

def load_roads(locations):
    roads = []

    file_path = DATA_DIR / "roads.csv"

    seen_edges = set()

    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            u = int(row["from"])
            v = int(row["to"])
            weight = float(row["distance_km"])

            if u not in locations or v not in locations:
                raise ValueError("Road contains an invalid location ID.")

            if u == v:
                raise ValueError("Self-loops are not allowed.")

            if weight <= 0:
                raise ValueError("Road distance must be positive.")

            edge = tuple(sorted((u, v)))

            if edge in seen_edges:
                raise ValueError("Duplicate road found.")

            seen_edges.add(edge)
            roads.append((u, v, weight))

    return roads

# ==========================================
# 3. CREATE WEIGHTED GRAPH
# ==========================================

def create_graph(n, roads):

    # Weighted adjacency matrix
    matrix = [[0 for _ in range(n)] for _ in range(n)]

    # Weighted adjacency list
    adj_list = {i: [] for i in range(1, n + 1)}

    for u, v, weight in roads:

        matrix[u - 1][v - 1] = weight
        matrix[v - 1][u - 1] = weight

        adj_list[u].append((v, weight))
        adj_list[v].append((u, weight))

    for vertex in adj_list:
        adj_list[vertex].sort()

    return matrix, adj_list

# ==========================================
# 4. CHECK GRAPH CONNECTIVITY
# ==========================================

def check_connectivity(adj_list, n):

    visited = set()
    queue = deque([1])

    visited.add(1)

    while queue:

        current = queue.popleft()

        for neighbor, weight in adj_list[current]:

            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return len(visited) == n

# ==========================================
# 5. CLASSIFY GRAPH
# ==========================================

def classify_graph(n, m):

    max_edges = n * (n - 1) // 2

    if m <= max_edges / 2:
        return (
            "Sparse",
            "Adjacency List",
            "Adjacency List is space efficient for sparse graphs"
        )

    return (
        "Dense",
        "Adjacency Matrix",
        "Adjacency Matrix is suitable for dense graphs and fast edge lookup"
    )

# ==========================================
# 6. ALGORITHM SELECTION
# ==========================================

def get_algorithm_plan():

    return [
        (
            "Adjacency Matrix",
            "Graph representation",
            "Stores road weights for direct edge lookup."
        ),
        (
            "Adjacency List",
            "Graph representation",
            "Stores connected locations and road distances efficiently."
        ),
        (
            "Merge Sort",
            "Package sorting",
            "Sorts packages by priority and deadline."
        ),
        (
            "Greedy Approach",
            "Delivery decisions",
            "Makes locally best delivery choices at each step."
        ),
        (
            "0/1 Knapsack (Dynamic Programming)",
            "Vehicle loading",
            "Selects valuable packages within vehicle capacity."
        ),
        (
            "Dijkstra",
            "Shortest path",
            "Finds shortest routes when road weights are non-negative."
        ),
        (
            "Bellman-Ford",
            "Negative cycle detection",
            "Handles negative edge weights and detects reachable negative cycles."
        ),
        (
            "Nearest Neighbor Approximation",
            "Multiple delivery stops",
            "Builds an approximate delivery tour by repeatedly selecting the nearest unvisited stop."
        )
    ]

# ==========================================
# 7. GENERATE PHASE 1 REPORT
# ==========================================

def generate_report():

    locations = load_locations()
    roads = load_roads(locations)

    n = len(locations)
    m = len(roads)

    matrix, adj_list = create_graph(n, roads)

    graph_type, recommendation, observation = classify_graph(n, m)

    connected = check_connectivity(adj_list, n)

    result = []

    result.append("=" * 60)
    result.append("       MINI COURIER PLANNER")
    result.append("       PHASE 1: DESIGN AND PLANNING")
    result.append("=" * 60)

    result.append("\n1. PROBLEM DEFINITION")

    result.append(
        "The system plans courier deliveries using graph algorithms."
    )

    result.append(
        "Locations represent vertices and roads represent weighted edges."
    )

    result.append(
        "The objective is to find efficient routes and optimize deliveries."
    )

    result.append("\n2. DATASET SUMMARY")

    result.append(f"Total Locations (Vertices): {n}")
    result.append(f"Total Roads (Edges): {m}")

    result.append("\nLOCATION DETAILS")

    for location_id, name in locations.items():
        result.append(f"{location_id}: {name}")

    result.append("\n3. ADJACENCY MATRIX")
    result.append("0 means no direct road; other values represent km.")

    header = "    " + " ".join(str(i) for i in range(1, n + 1))
    result.append(header)

    for i, row in enumerate(matrix, start=1):
        values = " ".join(
            f"{int(value):4}" for value in row
        )
        result.append(f"{i}: {values}")

    result.append("\n4. ADJACENCY LIST")

    for vertex in range(1, n + 1):

        neighbors = adj_list[vertex]

        if neighbors:
            details = ", ".join(
                f"{locations[v]} ({int(w)} km)"
                for v, w in neighbors
            )
        else:
            details = "None"

        result.append(f"{locations[vertex]}: {details}")

    result.append("\n5. GRAPH ANALYSIS")

    result.append(f"Graph Type: {graph_type}")
    result.append(f"Recommended Representation: {recommendation}")

    result.append(
        f"Graph Connected: {'Yes' if connected else 'No'}"
    )

    result.append(
        f"Maximum Possible Edges: {n * (n - 1) // 2}"
    )

    result.append("\n6. SPACE COMPLEXITY")

    result.append("Adjacency Matrix: O(V^2)")
    result.append("Adjacency List: O(V + E)")

    result.append("\n7. ALGORITHM SELECTION")

    for number, algorithm in enumerate(get_algorithm_plan(), start=1):

        name, purpose, explanation = algorithm

        result.append(f"\n{number}. {name}")
        result.append(f"Purpose: {purpose}")
        result.append(f"Reason: {explanation}")

    result.append("\n8. GRAPH REPRESENTATION OBSERVATION")
    result.append(observation)

    result.append("\n9. PROJECT ASSUMPTIONS")

    result.append("- Every location has a unique ID.")
    result.append("- Roads are undirected.")
    result.append("- Road distances are positive.")
    result.append("- Duplicate roads are not allowed.")
    result.append("- All sample distances are demonstration values.")
    result.append("- Actual traffic and delivery times are not included yet.")

    result.append("\n" + "=" * 60)
    result.append("PHASE 1 DESIGN REPORT COMPLETED")
    result.append("=" * 60)

    return "\n".join(result)

# ==========================================
# 8. MAIN EXECUTION
# ==========================================

if __name__ == "__main__":

    try:
        report = generate_report()

        print(report)

        output_dir = BASE_DIR / "output"
        output_dir.mkdir(exist_ok=True)

        report_path = output_dir / "phase1_report.txt"

        with open(report_path, "w", encoding="utf-8") as file:
            file.write(report)

        print("\nReport saved successfully!")
        print(f"File: {report_path}")

    except (FileNotFoundError, ValueError, KeyError) as error:

        print("\nERROR:", error)