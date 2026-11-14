from pathlib import Path
from datetime import datetime


# ==================================================
# MINI COURIER PLANNER
# PHASE 5: FINAL REPORT AND DEMONSTRATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
SCREENSHOT_DIR = BASE_DIR / "screenshots"

PHASE_REPORTS = [
    ("PHASE 1: DESIGN AND PLANNING",
     "phase1_report.txt"),

    ("PHASE 2: PACKAGE PRIORITIZATION AND VEHICLE LOADING",
     "phase2_report.txt"),

    ("PHASE 3: ROUTE MASTER AND TRAFFIC PROCESSING",
     "phase3_report.txt"),

    ("PHASE 4: PERFORMANCE TESTING AND OPTIMIZATION",
     "phase4_report.txt")
]


# ==================================================
# 1. VERIFY PROJECT FILES
# ==================================================

def verify_project():

    required_files = [
        "main.py",
        "phase2.py",
        "phase3.py",
        "phase4.py",
        "phase5.py",
        "data/locations.csv",
        "data/roads.csv",
        "data/packages.csv",
        "PHASE1_DESIGN.md",
        "PHASE2_DESIGN.md",
        "PHASE3_DESIGN.md",
        "PHASE4_DESIGN.md"
    ]

    missing = []

    for file in required_files:

        path = BASE_DIR / file

        if not path.exists():
            missing.append(file)

    return missing


# ==================================================
# 2. COLLECT PHASE REPORTS
# ==================================================

def collect_reports():

    collected = []

    missing_reports = []

    for title, filename in PHASE_REPORTS:

        path = OUTPUT_DIR / filename

        if not path.exists():

            missing_reports.append(filename)
            continue

        content = path.read_text(encoding="utf-8")

        collected.append({
            "title": title,
            "content": content
        })

    return collected, missing_reports


# ==================================================
# 3. GENERATE FINAL PROJECT REPORT
# ==================================================

def generate_final_report():

    missing_files = verify_project()

    reports, missing_reports = collect_reports()

    if missing_files or missing_reports:

        raise FileNotFoundError(
            "Some project files or reports are missing."
        )

    sections = []

    sections.append("=" * 75)

    sections.append(
        "             MINI COURIER PLANNER"
    )

    sections.append(
        "             FINAL PROJECT REPORT"
    )

    sections.append(
        "             DESIGN AND ANALYSIS OF ALGORITHMS"
    )

    sections.append("=" * 75)

    sections.append("\n1. PROJECT INFORMATION")

    sections.append(
        "Project Name: Mini Courier Planner"
    )

    sections.append(
        "Course: Design and Analysis of Algorithms"
    )

    sections.append(
        "Language: Python"
    )

    sections.append(
        "Project Type: Algorithm Based Courier Route Planning System"
    )

    sections.append(
        "Student: Vipin Tanwar"
    )

    sections.append(
        "Roll Number: 2501350071"
    )

    sections.append(
        "\n2. PROJECT OBJECTIVE"
    )

    sections.append(
        "The objective is to develop a courier planning system "
        "that prioritizes packages, optimizes vehicle loading, "
        "calculates shortest routes and plans multiple deliveries."
    )

    sections.append(
        "\n3. TECHNOLOGIES USED"
    )

    sections.append("Programming Language: Python")
    sections.append("Editor: Visual Studio Code")
    sections.append("Data Storage: CSV Files")
    sections.append("Performance Testing: time.perf_counter()")

    sections.append(
        "\n4. ALGORITHMS IMPLEMENTED"
    )

    algorithms = [
        ("Adjacency Matrix", "O(V^2)"),
        ("Adjacency List", "O(V + E)"),
        ("Merge Sort", "O(n log n)"),
        ("Insertion Sort", "O(n^2)"),
        ("Greedy Approach", "Depends on implementation"),
        ("0/1 Knapsack DP", "O(n x W)"),
        ("Dijkstra", "O(V^2 + E)"),
        ("Bellman-Ford", "O(V x E)"),
        ("Nearest Neighbor", "O(V x (V^2 + E))")
    ]

    for name, complexity in algorithms:

        sections.append(
            f"{name}: {complexity}"
        )

    sections.append(
        "\n5. PROJECT PHASES"
    )

    sections.append(
        "Phase 1: Design and Planning"
    )

    sections.append(
        "Phase 2: Package Prioritization and Vehicle Loading"
    )

    sections.append(
        "Phase 3: Route Master and Traffic Processing"
    )

    sections.append(
        "Phase 4: Performance Testing and Optimization"
    )

    sections.append(
        "Phase 5: Final Report and Demonstration"
    )

    sections.append(
        "\n6. FINAL PROJECT RESULTS"
    )

    sections.append(
        "Total Locations: 6"
    )

    sections.append(
        "Total Roads: 7"
    )

    sections.append(
        "Selected Packages: P101, P102, P105, P107"
    )

    sections.append(
        "Vehicle Capacity: 15 kg"
    )

    sections.append(
        "Total Loaded Weight: 14 kg"
    )

    sections.append(
        "Total Package Benefit: 370"
    )

    sections.append(
        "Optimized Delivery Tour: 1 -> 2 -> 6 -> 3 -> 1"
    )

    sections.append(
        "Total Route Distance: 15 km"
    )

    sections.append(
        "\n7. PERFORMANCE TESTING"
    )

    sections.append(
        "Performance results were collected using "
        "multiple input sizes and repeated execution."
    )

    sections.append(
        "Median execution time was used for comparison."
    )

    sections.append(
        "\n8. OPTIMIZATION"
    )

    sections.append(
        "Priority queues can improve Dijkstra performance."
    )

    sections.append(
        "Merge Sort is suitable for large package datasets."
    )

    sections.append(
        "One-dimensional DP can reduce Knapsack memory usage."
    )

    sections.append(
        "Caching can reduce repeated shortest path calculations."
    )

    sections.append(
        "\n9. LIMITATIONS"
    )

    sections.append(
        "The project uses demonstration road distances."
    )

    sections.append(
        "Real-time traffic information is not integrated."
    )

    sections.append(
        "Nearest Neighbor generates an approximate delivery tour."
    )

    sections.append(
        "The system currently uses a predefined sample dataset."
    )

    sections.append(
        "\n10. FUTURE SCOPE"
    )

    sections.append(
        "Integration with live traffic APIs."
    )

    sections.append(
        "Interactive map-based route visualization."
    )

    sections.append(
        "Dynamic vehicle capacity management."
    )

    sections.append(
        "Multiple courier vehicles and delivery zones."
    )

    sections.append(
        "Real-time delivery status tracking."
    )

    sections.append(
        "\n11. CONCLUSION"
    )

    sections.append(
        "The Mini Courier Planner demonstrates the practical "
        "application of graph algorithms, sorting, greedy "
        "techniques and dynamic programming."
    )

    sections.append(
        "The project successfully combines package selection, "
        "vehicle loading, shortest path calculation and "
        "approximate multi-stop delivery planning."
    )

    sections.append(
        "\n12. PHASE-WISE IMPLEMENTATION REPORTS"
    )

    for report in reports:

        sections.append("\n" + "=" * 75)

        sections.append(report["title"])

        sections.append("=" * 75)

        sections.append(report["content"])

    sections.append(
        "\n" + "=" * 75
    )

    sections.append(
        "              END OF FINAL PROJECT REPORT"
    )

    sections.append(
        "=" * 75
    )

    return "\n".join(sections)


# ==================================================
# 4. DEMONSTRATION CHECKLIST
# ==================================================

def generate_demo_checklist():

    checklist = """
MINI COURIER PLANNER
FINAL DEMONSTRATION CHECKLIST

1. Introduce the project and its objective.

2. Explain the courier locations and road network.

3. Demonstrate adjacency matrix and adjacency list.

4. Demonstrate Merge Sort and Insertion Sort.

5. Explain the 0/1 Knapsack DP table.

6. Demonstrate the selected package loading plan.

7. Demonstrate Dijkstra shortest paths.

8. Demonstrate Bellman-Ford negative cycle detection.

9. Demonstrate Nearest Neighbor delivery route.

10. Show performance comparison results.

11. Explain optimization suggestions.

12. Show the final project report and GitHub repository.

13. Explain limitations and future scope.

END OF DEMONSTRATION CHECKLIST
"""

    return checklist


# ==================================================
# 5. MAIN EXECUTION
# ==================================================

if __name__ == "__main__":

    try:

        OUTPUT_DIR.mkdir(exist_ok=True)

        SCREENSHOT_DIR.mkdir(exist_ok=True)

        print("=" * 65)

        print("       MINI COURIER PLANNER")

        print("       PHASE 5: FINAL REPORT")

        print("       AND DEMONSTRATION")

        print("=" * 65)

        print("\n1. VERIFYING PROJECT FILES")

        missing = verify_project()

        if missing:

            print("\nMissing project files:")

            for file in missing:
                print("-", file)

            raise FileNotFoundError(
                "Please complete the missing files first."
            )

        print("All required project files found.")

        print("\n2. COLLECTING PHASE REPORTS")

        reports, missing_reports = collect_reports()

        if missing_reports:

            for file in missing_reports:
                print("Missing report:", file)

            raise FileNotFoundError(
                "Phase reports are incomplete."
            )

        print(
            f"Successfully collected {len(reports)} phase reports."
        )

        print("\n3. GENERATING FINAL REPORT")

        final_report = generate_final_report()

        report_path = (
            OUTPUT_DIR / "final_project_report.txt"
        )

        report_path.write_text(
            final_report,
            encoding="utf-8"
        )

        print("Final project report generated.")

        print("\n4. GENERATING DEMONSTRATION CHECKLIST")

        demo_path = (
            OUTPUT_DIR / "demonstration_checklist.txt"
        )

        demo_path.write_text(
            generate_demo_checklist(),
            encoding="utf-8"
        )

        print("Demonstration checklist generated.")

        print("\n5. PROJECT SUMMARY")

        print("Total Phases Completed: 5")
        print("Phase Reports Collected:", len(reports))

        print("\n6. GENERATED FILES")

        print("output/final_project_report.txt")

        print("output/demonstration_checklist.txt")

        print("\n" + "=" * 65)

        print("PHASE 5 COMPLETED SUCCESSFULLY")

        print("FINAL PROJECT REPORT GENERATED")

        print("=" * 65)

    except (FileNotFoundError, OSError) as error:

        print("\nERROR:", error)
        print("Check the missing files and try again.")