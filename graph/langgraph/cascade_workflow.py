from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    END
)

from graph.algorithms.risk_score import (
    calculate_risk
)

from graph.agents.recommendation_engine import (
    generate_recommendations
)

from graph.agents.narrative_generator import (
    generate_risk_narrative
)

from graph.langgraph.validation_node import (
    validate_output
)


# =====================================
# STATE
# =====================================

class PortfolioState(TypedDict):

    project_id: str

    risk: dict

    recommendations: list

    narrative: str

    validation: dict


# =====================================
# NODE 1
# RISK ANALYSIS
# =====================================

def risk_node(state):

    risk = calculate_risk(
        state["project_id"]
    )

    state["risk"] = risk

    return state


# =====================================
# NODE 2
# RECOMMENDATIONS
# =====================================

def recommendation_node(state):

    recommendations = (
        generate_recommendations(
            state["risk"]
        )
    )

    state["recommendations"] = (
        recommendations
    )

    return state


# =====================================
# NODE 3
# EXECUTIVE NARRATIVE
# =====================================

def narrative_node(state):

    narrative = (
        generate_risk_narrative(
            state["risk"],
            state["recommendations"]
        )
    )

    state["narrative"] = (
        narrative
    )

    return state


# =====================================
# NODE 4
# VALIDATION
# =====================================

def validation_node(state):

    state = validate_output(
        state
    )

    return state


# =====================================
# BUILD LANGGRAPH WORKFLOW
# =====================================

workflow = StateGraph(
    PortfolioState
)

# Add Nodes

workflow.add_node(
    "risk",
    risk_node
)

workflow.add_node(
    "recommendation",
    recommendation_node
)

workflow.add_node(
    "narrative",
    narrative_node
)

workflow.add_node(
    "validation",
    validation_node
)

# Entry Point

workflow.set_entry_point(
    "risk"
)

# Flow

workflow.add_edge(
    "risk",
    "recommendation"
)

workflow.add_edge(
    "recommendation",
    "narrative"
)

workflow.add_edge(
    "narrative",
    "validation"
)

workflow.add_edge(
    "validation",
    END
)

# Compile

app = workflow.compile()


# =====================================
# TERMINAL TESTING
# =====================================

if __name__ == "__main__":

    project_id = input(
        "\nEnter Project ID: "
    )

    result = app.invoke({

        "project_id":
        project_id

    })

    print("\n")

    print("=" * 60)
    print("CASCADEIQ LANGGRAPH RESULT")
    print("=" * 60)

    print(result)