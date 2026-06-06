from graph.agents.query_parser import parse_query
from graph.agents.intent_router import detect_intent

from graph.agents.recommendation_engine import (
    generate_recommendations
)

from graph.algorithms.delay_propagation import (
    propagate_delay
)

from graph.algorithms.risk_score import (
    calculate_risk
)

from graph.algorithms.monte_carlo import (
    monte_carlo_summary
)

from graph.algorithms.resource_analysis import (
    get_overloaded_resources
)

from graph.agents.narrative_generator import (
    generate_risk_narrative
)
def analyze_query(query):

    intent = detect_intent(query)

    print("=" * 50)
    print("QUERY =", query)
    print("INTENT =", intent)
    print("=" * 50)

    # =================================
    # DELAY ANALYSIS
    # =================================

    if intent == "DELAY":

        parsed = parse_query(query)

        project_id = parsed.get(
            "project_id"
        )

        delay_days = parsed.get(
            "delay_days"
        )

        if not project_id:

            return {
                "intent": "UNKNOWN",
                "message":
                "Project ID not found."
            }

        if delay_days is None:

            return {
                "intent": "UNKNOWN",
                "message":
                "Delay days not found."
            }

        impacts = propagate_delay(
            project_id,
            delay_days
        )

        risk = calculate_risk(
            project_id
        )

        return {

            "intent": "DELAY",

            "project": project_id,

            "delay_days": delay_days,

            "risk": risk,

            "impacts": impacts

        }

    # =================================
    # RISK ANALYSIS
    # =================================

    elif intent == "RISK":

        parsed = parse_query(query)

        project_id = parsed.get(
            "project_id"
        )

        if not project_id:

            return {

                "intent": "UNKNOWN",

                "message":
                "Project ID not found."

            }

        risk = calculate_risk(
            project_id
        )

        recommendations = (
            generate_recommendations(
                risk
            )
        )

        narrative = (
    generate_risk_narrative(
        risk,
        recommendations
    )
)

        return {

            "intent": "RISK",

            "risk": risk,

            "recommendations":
            recommendations,

            "narrative":
            narrative

        }

    # =================================
    # MONTE CARLO
    # =================================

    elif intent == "MONTE_CARLO":

        parsed = parse_query(query)

        project_id = parsed.get(
            "project_id"
        )

        if not project_id:

            return {

                "intent": "UNKNOWN",

                "message":
                "Project ID not found."

            }

        summary = monte_carlo_summary(
            project_id,
            simulations=1000
        )

        return {

            "intent": "MONTE_CARLO",

            **summary

        }

    # =================================
    # RESOURCE ANALYSIS
    # =================================

    elif intent == "RESOURCE":

        resources = (
            get_overloaded_resources()
        )

        return {

            "intent": "RESOURCE",

            "resources":
            resources[:10]

        }

    # =================================
    # UNKNOWN
    # =================================

    return {

        "intent": "UNKNOWN",

        "message":
        "Unable to understand query."

    }


if __name__ == "__main__":

    query = input(
        "\nAsk CascadeIQ: "
    )

    result = analyze_query(
        query
    )

    print("\n")
    print(result)