import time
import random
import statistics
from pathlib import Path

from phase2 import (
    merge_sort_deadline,
    insertion_sort_priority,
    knapsack_dp
)

from phase3 import (
    dijkstra,
    bellman_ford,
    nearest_neighbor
)


# ==================================================
# MINI COURIER PLANNER
# PHASE 4: PERFORMANCE TESTING AND OPTIMIZATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"

REPEATS = 3


# ==================================================
# 1. GENERATE TEST GRAPH
# ==================================================

def generate_graph(n, extra_edges=0):

    graph = {
        i: [] for i in range(1, n + 1)
    }

    edges = []

    # Create connected ring

    for u in range(1, n + 1):

        v = u + 1 if u < n else 1

        edges.append((u, v, 1))

    # Add extra random edges

    rng = random.Random(n)

    existing = {
        tuple(sorted((u, v)))
        for u, v, w in edges
    }

    attempts = 0

    while len(edges) < n + extra_edges and attempts < n * n:

        attempts += 1

        u = rng.randint(1, n)
        v = rng.randint(1, n)

        if u == v:
            continue

        key = tuple(sorted((u, v)))

        if key in existing:
            continue

        existing.add(key)

        weight = rng.randint(1, 20)

        edges.append((u, v, weight))

    for u, v, weight in edges:

        graph[u].append((v, weight))
        graph[v].append((u, weight))

    for vertex in graph:
        graph[vertex].sort()

    return graph, edges


# ==================================================
# 2. GENERATE TEST PACKAGES
# ==================================================

def generate_packages(n):

    rng = random.Random(n)

    priorities = ["High", "Medium", "Low"]

    packages = []

    for i in range(n):

        minutes = rng.randint(0, 1439)

        hours = minutes // 60
        mins = minutes % 60

        packages.append({
            "id": f"P{i + 1}",
            "destination": 1,
            "weight": rng.randint(1, 10),
            "priority": rng.choice(priorities),
            "deadline": f"{hours:02d}:{mins:02d}",
            "benefit": rng.randint(10, 150)
        })

    return packages


# ==================================================
# 3. MEASURE EXECUTION TIME
# ==================================================

def benchmark(function, repeats=REPEATS):

    times = []

    result = None

    for _ in range(repeats):

        start = time.perf_counter()

        result = function()

        end = time.perf_counter()

        times.append((end - start) * 1000)

    return statistics.median(times), result


# ==================================================
# 4. FORMAT TIME
# ==================================================

def format_time(milliseconds):

    if milliseconds < 1:
        return f"{milliseconds:.4f} ms"

    return f"{milliseconds:.3f} ms"


# ==================================================
# 5. TEST DIJKSTRA
# ==================================================

def test_dijkstra():

    results = []

    for n in [30, 80]:

        graph, edges = generate_graph(n, n * 2)

        runtime, result = benchmark(
            lambda: dijkstra(graph, 1)
        )

        distances, parents = result

        if any(value == float("inf") for value in distances.values()):
            raise RuntimeError("Dijkstra connectivity test failed.")

        results.append(
            ("Dijkstra", n, len(edges), runtime)
        )

    return results


# ==================================================
# 6. TEST BELLMAN-FORD
# ==================================================

def test_bellman_ford():

    results = []

    for n in [30, 80]:

        graph, roads = generate_graph(n, n * 2)

        directed_edges = []

        for u, v, weight in roads:

            directed_edges.append((u, v, weight))
            directed_edges.append((v, u, weight))

        runtime, result = benchmark(
            lambda: bellman_ford(
                n,
                directed_edges,
                1
            )
        )

        distances, parents, negative = result

        if negative:
            raise RuntimeError("Unexpected negative cycle.")

        if any(
            distances[i] == float("inf")
            for i in range(1, n + 1)
        ):
            raise RuntimeError("Bellman-Ford connectivity test failed.")

        results.append(
            ("Bellman-Ford", n, len(directed_edges), runtime)
        )

    return results


# ==================================================
# 7. TEST MERGE SORT AND INSERTION SORT
# ==================================================

def test_sorting():

    results = []

    for n in [500, 2000]:

        packages = generate_packages(n)

        merge_time, merge_result = benchmark(
            lambda: merge_sort_deadline(packages)
        )

        insertion_time, insertion_result = benchmark(
            lambda: insertion_sort_priority(packages)
        )

        if merge_result != sorted(
            packages,
            key=lambda p: p["deadline"]
        ):
            raise RuntimeError("Merge Sort validation failed.")

        def priority_key(p):
            rank = {"High": 3, "Medium": 2, "Low": 1}
            return (-rank[p["priority"]], p["deadline"])

        if insertion_result != sorted(
            packages,
            key=priority_key
        ):
            raise RuntimeError("Insertion Sort validation failed.")

        results.append(
            ("Merge Sort", n, 0, merge_time)
        )

        results.append(
            ("Insertion Sort", n, 0, insertion_time)
        )

    return results


# ==================================================
# 8. TEST 0/1 KNAPSACK
# ==================================================

def test_knapsack():

    results = []

    test_cases = [
        (25, 100),
        (50, 200)
    ]

    for n, capacity in test_cases:

        packages = generate_packages(n)

        runtime, result = benchmark(
            lambda: knapsack_dp(packages, capacity)
        )

        dp, selected = result

        total_weight = sum(
            p["weight"] for p in selected
        )

        if total_weight > capacity:
            raise RuntimeError("Knapsack capacity validation failed.")

        results.append(
            ("0/1 Knapsack", n, capacity, runtime)
        )

    return results


# ==================================================
# 9. TEST NEAREST NEIGHBOR
# ==================================================

def test_nearest_neighbor():

    results = []

    for n in [30, 80]:

        graph, edges = generate_graph(n, n * 2)

        # Test a fixed number of delivery stops

        destinations = sorted({
            max(2, (i * (n - 1) // 9) + 1)
            for i in range(1, 9)
        })

        destinations = [
            v for v in destinations
            if v != 1
        ]

        runtime, result = benchmark(
            lambda: nearest_neighbor(
                graph,
                1,
                destinations
            )
        )

        route, total_distance = result

        if route[0] != 1 or route[-1] != 1:
            raise RuntimeError("Nearest Neighbor route validation failed.")

        if not isinstance(total_distance, (int, float)):
            raise RuntimeError("Invalid route distance.")

        results.append(
            ("Nearest Neighbor", n, len(destinations), runtime)
        )

    return results


# ==================================================
# 10. GENERATE REPORT
# ==================================================

def generate_phase4_report():

    all_results = []

    all_results.extend(test_dijkstra())
    all_results.extend(test_bellman_ford())
    all_results.extend(test_sorting())
    all_results.extend(test_knapsack())
    all_results.extend(test_nearest_neighbor())

    report = []

    report.append("=" * 70)
    report.append("       MINI COURIER PLANNER")
    report.append("       PHASE 4: PERFORMANCE TESTING")
    report.append("       AND OPTIMIZATION")
    report.append("=" * 70)

    report.append("\n1. TESTING ENVIRONMENT")

    report.append("Language: Python")
    report.append("Timer: time.perf_counter()")
    report.append(f"Repetitions per test: {REPEATS}")
    report.append("Reported time: Median execution time")

    report.append("\n2. PERFORMANCE TEST RESULTS")

    report.append(
        f"{'Algorithm':22} {'Input':>8} "
        f"{'Extra':>8} {'Runtime':>15}"
    )

    report.append("-" * 60)

    for name, size, extra, runtime in all_results:

        report.append(
            f"{name:22} {size:8} "
            f"{extra:8} {format_time(runtime):>15}"
        )

    report.append("\n3. PERFORMANCE ANALYSIS")

    report.append(
        "Dijkstra uses O(V^2 + E) time with the current "
        "array-based vertex selection."
    )

    report.append(
        "Bellman-Ford uses O(V x E) time."
    )

    report.append(
        "Merge Sort uses O(n log n) time."
    )

    report.append(
        "Insertion Sort uses O(n^2) worst-case time."
    )

    report.append(
        "0/1 Knapsack uses O(n x W) time and space "
        "with the current DP table."
    )

    report.append(
        "Nearest Neighbor repeatedly calls Dijkstra "
        "to choose delivery stops."
    )

    report.append("\n4. OPTIMIZATION SUGGESTIONS")

    report.append(
        "1. Use a Min Heap or Priority Queue for Dijkstra."
    )

    report.append(
        "2. Use an efficient adjacency list for sparse graphs."
    )

    report.append(
        "3. Use Merge Sort instead of Insertion Sort "
        "for large package datasets."
    )

    report.append(
        "4. Use a one-dimensional DP array to reduce "
        "Knapsack memory usage."
    )

    report.append(
        "5. Avoid repeated shortest path calculations "
        "when cached distances can be reused."
    )

    report.append(
        "6. Use larger and realistic datasets for further testing."
    )

    report.append("\n5. VALIDATION")

    report.append(
        "All algorithm test executions completed successfully."
    )

    report.append(
        "Shortest path, sorting, capacity and route "
        "validation checks passed."
    )

    report.append("\n6. CONCLUSION")

    report.append(
        "The Mini Courier Planner was tested using "
        "multiple dataset sizes."
    )

    report.append(
        "Execution times were recorded and "
        "optimization opportunities were identified."
    )

    report.append("\n" + "=" * 70)

    report.append("PHASE 4 COMPLETED SUCCESSFULLY")

    report.append("=" * 70)

    return "\n".join(report)


# ==================================================
# 11. MAIN EXECUTION
# ==================================================

if __name__ == "__main__":

    try:

        report = generate_phase4_report()

        print(report)

        OUTPUT_DIR.mkdir(exist_ok=True)

        report_path = OUTPUT_DIR / "phase4_report.txt"

        with open(
            report_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(report)

        print("\nPhase 4 report saved successfully!")
        print(f"File: {report_path}")

    except (
        FileNotFoundError,
        ValueError,
        KeyError,
        RuntimeError
    ) as error:

        print("\nERROR:", error)