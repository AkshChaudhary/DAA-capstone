import csv
from pathlib import Path


# ==================================================
# MINI COURIER PLANNER
# PHASE 3: ROUTE MASTER AND TRAFFIC PROCESSING
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

SOURCE = 1


# ==================================================
# 1. LOAD LOCATIONS
# ==================================================

def load_locations():

    locations = {}

    with open(
        DATA_DIR / "locations.csv",
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            locations[int(row["id"])] = row["name"]

    if not locations:
        raise ValueError("No locations found.")

    return locations


# ==================================================
# 2. LOAD ROADS
# ==================================================

def load_roads(locations):

    roads = []

    seen = set()

    with open(
        DATA_DIR / "roads.csv",
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            u = int(row["from"])
            v = int(row["to"])
            w = float(row["distance_km"])

            if u not in locations or v not in locations:
                raise ValueError("Invalid road location.")

            if u == v or w <= 0:
                raise ValueError("Invalid road data.")

            edge = tuple(sorted((u, v)))

            if edge in seen:
                raise ValueError("Duplicate road found.")

            seen.add(edge)
            roads.append((u, v, w))

    return roads


# ==================================================
# 3. CREATE WEIGHTED ADJACENCY LIST
# ==================================================

def create_graph(locations, roads):

    graph = {
        vertex: []
        for vertex in locations
    }

    for u, v, weight in roads:

        graph[u].append((v, weight))
        graph[v].append((u, weight))

    for vertex in graph:
        graph[vertex].sort()

    return graph


# ==================================================
# 4. DIJKSTRA SHORTEST PATH ALGORITHM
# ==================================================

def dijkstra(graph, source):

    vertices = sorted(graph)

    distance = {
        vertex: float("inf")
        for vertex in vertices
    }

    parent = {
        vertex: None
        for vertex in vertices
    }

    visited = set()

    distance[source] = 0

    while len(visited) < len(vertices):

        current = None

        # Select smallest distance.
        # On ties, choose smaller vertex number.

        for vertex in vertices:

            if vertex in visited:
                continue

            if current is None:
                current = vertex

            elif distance[vertex] < distance[current]:
                current = vertex

            elif (
                distance[vertex] == distance[current]
                and vertex < current
            ):
                current = vertex

        if current is None or distance[current] == float("inf"):
            break

        visited.add(current)

        for neighbor, weight in graph[current]:

            if neighbor in visited:
                continue

            new_distance = distance[current] + weight

            if new_distance < distance[neighbor]:

                distance[neighbor] = new_distance
                parent[neighbor] = current

    return distance, parent


# ==================================================
# 5. RECONSTRUCT SHORTEST PATH
# ==================================================

def reconstruct_path(parent, source, destination):

    if destination != source and parent[destination] is None:
        return None

    path = []

    current = destination

    while current is not None:

        path.append(current)

        if current == source:
            break

        current = parent[current]

    path.reverse()

    if not path or path[0] != source:
        return None

    return path


# ==================================================
# 6. BELLMAN-FORD ALGORITHM
# ==================================================

def bellman_ford(n, edges, source):

    distance = [float("inf")] * (n + 1)

    parent = [None] * (n + 1)

    distance[source] = 0

    # Relax all edges exactly n - 1 times

    for _ in range(n - 1):

        for u, v, weight in edges:

            if distance[u] == float("inf"):
                continue

            new_distance = distance[u] + weight

            if new_distance < distance[v]:

                distance[v] = new_distance
                parent[v] = u

    # Detect reachable negative weight cycle

    negative_cycle = False

    for u, v, weight in edges:

        if distance[u] == float("inf"):
            continue

        if distance[u] + weight < distance[v]:

            negative_cycle = True
            break

    return distance, parent, negative_cycle


# ==================================================
# 7. LOAD SELECTED PACKAGES
# ==================================================

def load_selected_packages():

    selected_ids = {
        "P101", "P102", "P105", "P107"
    }

    packages = []

    with open(
        DATA_DIR / "packages.csv",
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["package_id"] in selected_ids:

                packages.append({
                    "id": row["package_id"],
                    "destination": int(row["destination_id"])
                })

    if {p["id"] for p in packages} != selected_ids:
        raise ValueError("Selected packages do not match Phase 2.")

    return packages


# ==================================================
# 8. NEAREST NEIGHBOR APPROXIMATION
# ==================================================

def nearest_neighbor(graph, source, destinations):

    remaining = set(destinations)

    current = source

    route = [source]

    total_distance = 0

    while remaining:

        distance, parent = dijkstra(graph, current)

        reachable = [
            vertex for vertex in remaining
            if distance[vertex] != float("inf")
        ]

        if not reachable:
            raise ValueError("Some delivery locations are unreachable.")

        # Minimum distance, then smaller vertex ID

        next_vertex = min(
            reachable,
            key=lambda vertex: (distance[vertex], vertex)
        )

        segment = reconstruct_path(
            parent,
            current,
            next_vertex
        )

        total_distance += distance[next_vertex]

        route.extend(segment[1:])

        remaining.remove(next_vertex)

        current = next_vertex

    # Return to courier hub

    distance, parent = dijkstra(graph, current)

    if distance[source] == float("inf"):
        raise ValueError("Courier hub is unreachable.")

    return_path = reconstruct_path(
        parent,
        current,
        source
    )

    total_distance += distance[source]

    route.extend(return_path[1:])

    return route, total_distance


# ==================================================
# 9. FORMAT DISTANCE
# ==================================================

def format_distance(value):

    if value == float("inf"):
        return "INF"

    if value == int(value):
        return str(int(value))

    return str(value)


# ==================================================
# 10. GENERATE PHASE 3 REPORT
# ==================================================

def generate_phase3_report():

    locations = load_locations()

    roads = load_roads(locations)

    n = len(locations)
    m = len(roads)

    graph = create_graph(locations, roads)

    result = []

    result.append("=" * 65)
    result.append("       MINI COURIER PLANNER")
    result.append("       PHASE 3: ROUTE MASTER")
    result.append("       AND TRAFFIC PROCESSING")
    result.append("=" * 65)

    # ----------------------------------------------
    # Weighted graph
    # ----------------------------------------------

    result.append("\n1. WEIGHTED GRAPH SUMMARY")

    result.append(f"Total Vertices: {n}")
    result.append(f"Total Roads: {m}")
    result.append("Graph Type: Undirected Weighted Graph")
    result.append("Edge Weight: Distance in Kilometers")

    result.append("\n2. WEIGHTED ADJACENCY LIST")

    for vertex in sorted(graph):

        neighbors = ", ".join(
            f"{v} ({format_distance(w)} km)"
            for v, w in graph[vertex]
        )

        result.append(
            f"{vertex} - {locations[vertex]}: {neighbors or 'None'}"
        )

    # ----------------------------------------------
    # Dijkstra
    # ----------------------------------------------

    result.append("\n3. DIJKSTRA SHORTEST PATH ALGORITHM")

    result.append(f"Source Vertex: {SOURCE} - {locations[SOURCE]}")

    distance, parent = dijkstra(graph, SOURCE)

    result.append("\nVertex | Distance | Shortest Path")

    for vertex in sorted(locations):

        path = reconstruct_path(parent, SOURCE, vertex)

        if path is None:
            path_text = "None"
        else:
            path_text = " -> ".join(
                str(x) for x in path
            )

        result.append(
            f"{vertex} - {locations[vertex]} | "
            f"{format_distance(distance[vertex])} km | "
            f"{path_text}"
        )

    # ----------------------------------------------
    # Bellman-Ford
    # ----------------------------------------------

    result.append("\n4. BELLMAN-FORD ALGORITHM")

    result.append(
        "Demonstration graph: Directed graph with a negative edge."
    )

    # Separate directed test graph.
    # These are algorithm test weights, not actual road distances.

    bf_edges = [
        (1, 2, 4),
        (1, 3, 5),
        (2, 3, -2),
        (3, 4, 3),
        (2, 4, 4)
    ]

    bf_n = 4

    bf_distance, bf_parent, negative = bellman_ford(
        bf_n,
        bf_edges,
        1
    )

    result.append("Source Vertex: 1")
    result.append("Negative Cycle: " + ("Yes" if negative else "No"))

    if negative:

        result.append(
            "Shortest paths are not possible because "
            "the graph contains a reachable negative weight cycle."
        )

    else:

        result.append("\nVertex | Distance | Path")

        for vertex in range(1, bf_n + 1):

            path = reconstruct_path(
                {
                    i: bf_parent[i]
                    for i in range(1, bf_n + 1)
                },
                1,
                vertex
            )

            path_text = (
                "None"
                if path is None
                else " -> ".join(map(str, path))
            )

            result.append(
                f"{vertex} | {format_distance(bf_distance[vertex])} | "
                f"{path_text}"
            )

    # Negative cycle test

    negative_test_edges = [
        (1, 2, 1),
        (2, 3, -2),
        (3, 2, -2)
    ]

    _, _, cycle_detected = bellman_ford(
        3,
        negative_test_edges,
        1
    )

    result.append(
        "\nNegative Cycle Test: "
        + ("Detected" if cycle_detected else "Not Detected")
    )

    # ----------------------------------------------
    # Nearest Neighbor
    # ----------------------------------------------

    result.append("\n5. NEAREST NEIGHBOR ROUTE OPTIMIZATION")

    packages = load_selected_packages()

    destinations = sorted({
        package["destination"]
        for package in packages
    })

    result.append("\nSelected Packages:")

    for package in packages:

        destination = package["destination"]

        result.append(
            f'{package["id"]}: {locations[destination]}'
        )

    result.append(
        "\nUnique Delivery Locations: "
        + ", ".join(
            f"{v} ({locations[v]})"
            for v in destinations
        )
    )

    route, total_distance = nearest_neighbor(
        graph,
        SOURCE,
        destinations
    )

    result.append("\nOptimized Delivery Route:")

    result.append(
        " -> ".join(
            f"{v} ({locations[v]})"
            for v in route
        )
    )

    result.append(
        f"\nTotal Route Distance: {format_distance(total_distance)} km"
    )

    result.append("Courier Returns to Hub: Yes")

    # ----------------------------------------------
    # Complexity
    # ----------------------------------------------

    result.append("\n6. ALGORITHM COMPLEXITY")

    result.append("Dijkstra: O(V^2 + E)")

    result.append("Bellman-Ford: O(V x E)")

    result.append("Nearest Neighbor: O(V x (V^2 + E))")

    result.append("\n7. OBSERVATION")

    result.append(
        "Dijkstra finds shortest paths for non-negative road weights."
    )

    result.append(
        "Bellman-Ford supports negative weights and detects "
        "reachable negative cycles."
    )

    result.append(
        "Nearest Neighbor approximates a delivery tour by "
        "choosing the nearest unvisited delivery location."
    )

    result.append(
        "The route uses shortest road paths between selected stops."
    )

    result.append("\n" + "=" * 65)

    result.append("PHASE 3 COMPLETED SUCCESSFULLY")

    result.append("=" * 65)

    return "\n".join(result)


# ==================================================
# 11. MAIN EXECUTION
# ==================================================

if __name__ == "__main__":

    try:

        report = generate_phase3_report()

        print(report)

        OUTPUT_DIR.mkdir(exist_ok=True)

        report_path = OUTPUT_DIR / "phase3_report.txt"

        with open(
            report_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(report)

        print("\nPhase 3 report saved successfully!")
        print(f"File: {report_path}")

    except (FileNotFoundError, ValueError, KeyError) as error:

        print("\nERROR:", error)