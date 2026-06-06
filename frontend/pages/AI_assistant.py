import streamlit as st

from graph.agents.portfolio_agent import (
    analyze_query
)
from graph.utils.audit_logger import (
    log_query
)
st.set_page_config(
    page_title="CascadeIQ AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 CascadeIQ AI Assistant")

st.markdown("""
Ask questions about:

• Risk Analysis

• Delay Impact Analysis

• Monte Carlo Simulation

• Resource Bottlenecks
""")

query = st.text_input(
    "Ask a question",
    placeholder="What is the risk score of P001?"
)

if st.button("Analyze"):

    try:

        result = analyze_query(
            query
        )
        log_query(
            query,
            result
        )
        intent = result["intent"]

        # =====================================
        # RISK ANALYSIS
        # =====================================

        if intent == "RISK":

            risk = result["risk"]

            st.success(
                "Risk Analysis Completed"
            )

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Risk Score",
                risk["risk_score"]
            )

            col2.metric(
                "Dependencies",
                risk["dependencies"]
            )

            col3.metric(
                "Resources",
                risk["resources"]
            )

            col4.metric(
                "Critical Tasks",
                risk["critical_tasks"]
            )

            st.info(
                f"Risk Level: {risk['risk_level']}"
            )

            st.subheader(
                "Recommendations"
            )

            recommendations = result.get(
                "recommendations",
                []
            )

            for rec in recommendations:

                st.write(
                    f"• {rec}"
                )
            st.subheader(
                "Executive Summary"
            )

            st.info(
                result["narrative"]
            )
        # =====================================
        # DELAY ANALYSIS
        # =====================================

        elif intent == "DELAY":

            st.success(
                "Delay Impact Analysis Completed"
            )

            st.subheader(
                f"Project: {result['project']}"
            )

            st.write(
                f"Delay Introduced: {result['delay_days']} Days"
            )

            st.write(
                f"Risk Level: {result['risk']['risk_level']}"
            )

            st.write(
                f"Impacted Tasks: {len(result['impacts'])}"
            )

            st.dataframe(
                result["impacts"],
                use_container_width=True
            )

        # =====================================
        # MONTE CARLO
        # =====================================

        elif intent == "MONTE_CARLO":

            st.success(
                "Monte Carlo Simulation Completed"
            )

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Average",
                result["average"]
            )

            col2.metric(
                "P50",
                result["p50"]
            )

            col3.metric(
                "P80",
                result["p80"]
            )

            col4.metric(
                "P95",
                result["p95"]
            )

        # =====================================
        # RESOURCE ANALYSIS
        # =====================================

        elif intent == "RESOURCE":

            st.success(
                "Resource Analysis Completed"
            )

            st.dataframe(
                result["resources"],
                use_container_width=True
            )

        else:

            st.warning(
                result.get(
                    "message",
                    "Unable to understand query."
                )
            )

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )

        st.exception(e)