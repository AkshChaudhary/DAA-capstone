# MINI COURIER PLANNER
## Phase 3: Route Master and Traffic Processing

### 1. Introduction

Phase 3 implements route planning algorithms
for the Mini Courier Planner.

The system calculates shortest paths between
delivery locations and creates an approximate
multi-stop delivery tour.

### 2. Weighted Graph

The road network is represented using an
undirected weighted graph.

Vertices represent delivery locations.

Edges represent roads.

Weights represent road distances in kilometers.

### 3. Dijkstra Algorithm

Dijkstra is used to calculate shortest paths
from the Courier Hub to all locations.

Source Vertex: 1

Time Complexity: O(V^2 + E)

### 4. Bellman-Ford Algorithm

Bellman-Ford calculates shortest paths in
directed weighted graphs that may contain
negative edge weights.

It also detects reachable negative weight cycles.

Time Complexity: O(V * E)

A separate directed demonstration graph is
used to test negative weights and cycle detection.

### 5. Nearest Neighbor Approximation

Nearest Neighbor is used to construct an
approximate delivery tour.

It repeatedly selects the nearest unvisited
delivery location.

Selected Delivery Locations:
North Zone, East Zone, Central Zone.

Route:
1 -> 2 -> 6 -> 3 -> 1

Total Route Distance: 15 km

### 6. Results

Dijkstra successfully calculates shortest paths.

Bellman-Ford successfully handles negative
edge weights and detects a negative cycle.

Nearest Neighbor generates a multi-stop
delivery route and returns the vehicle to
the Courier Hub.

### 7. Complexity Analysis

Dijkstra: O(V^2 + E)

Bellman-Ford: O(V * E)

Nearest Neighbor:
O(V * (V^2 + E))

### 8. Conclusion

Phase 3 successfully implements shortest path
calculation, negative cycle detection and
approximate multi-location route optimization.

The algorithms provide the foundation for
the performance testing and optimization
stage of the project.