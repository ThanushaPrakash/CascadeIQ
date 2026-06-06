import pandas as pd
import numpy as np

# =====================================
# Load Tasks Dataset
# =====================================

tasks = pd.read_csv(
    r"D:\cascadeIQ\datasets\raw\tasks.csv"
)

# =====================================
# Monte Carlo Simulation
# =====================================

def monte_carlo_project(
        project_id,
        simulations=1000):

    project_tasks = tasks[
        tasks["project_id"] == project_id
    ]

    if len(project_tasks) == 0:

        raise ValueError(
            f"No tasks found for project {project_id}"
        )

    results = []

    for _ in range(simulations):

        total_duration = 0

        for _, task in project_tasks.iterrows():

            sampled_duration = np.random.triangular(

                task["duration_optimistic"],

                task["duration_likely"],

                task["duration_pessimistic"]

            )

            total_duration += sampled_duration

        results.append(total_duration)

    return results


# =====================================
# Monte Carlo Summary Statistics
# =====================================

def monte_carlo_summary(
        project_id,
        simulations=1000):

    results = monte_carlo_project(
        project_id,
        simulations
    )

    return {

        "project_id": project_id,

        "average": round(
            float(np.mean(results)),
            2
        ),

        "p50": round(
            float(np.percentile(results, 50)),
            2
        ),

        "p80": round(
            float(np.percentile(results, 80)),
            2
        ),

        "p95": round(
            float(np.percentile(results, 95)),
            2
        ),

        "simulations": simulations,

        # Required for histogram chart
        "results": results

    }


# =====================================
# Testing
# =====================================

if __name__ == "__main__":

    summary = monte_carlo_summary(
        "P001",
        simulations=1000
    )

    print("\nMonte Carlo Results")
    print("-" * 40)

    print(
        f"Project : {summary['project_id']}"
    )

    print(
        f"Average : {summary['average']}"
    )

    print(
        f"P50     : {summary['p50']}"
    )

    print(
        f"P80     : {summary['p80']}"
    )

    print(
        f"P95     : {summary['p95']}"
    )

    print(
        f"Simulations : {summary['simulations']}"
    )

    print(
        f"Generated Results : {len(summary['results'])}"
    )