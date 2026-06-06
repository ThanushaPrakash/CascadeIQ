def generate_recommendations(risk):

    recommendations = []

    # High Risk

    if risk["risk_score"] >= 80:

        recommendations.append(
            "Immediate intervention required."
        )

        recommendations.append(
            "Schedule executive review."
        )

    # Dependency Risk

    if risk["dependencies"] > 5:

        recommendations.append(
            "Reduce dependency bottlenecks."
        )

        recommendations.append(
            "Review cross-project dependencies."
        )

    # Resource Risk

    if risk["resources"] > 5:

        recommendations.append(
            "Reassign overloaded resources."
        )

        recommendations.append(
            "Increase resource capacity."
        )

    # Critical Tasks

    if risk["critical_tasks"] > 3:

        recommendations.append(
            "Review critical path tasks."
        )

        recommendations.append(
            "Prioritize critical deliverables."
        )

    if len(recommendations) == 0:

        recommendations.append(
            "No major action required."
        )

    return recommendations


if __name__ == "__main__":

    sample_risk = {

        "project_id": "P001",

        "risk_score": 100,

        "risk_level": "🔴 High",

        "dependencies": 10,

        "resources": 10,

        "critical_tasks": 4

    }

    recs = generate_recommendations(
        sample_risk
    )

    print()

    for rec in recs:

        print(rec)