import streamlit as st
import pandas as pd
import plotly.express as px

from graph.algorithms.monte_carlo import (
    monte_carlo_summary
)

st.set_page_config(
    page_title="Monte Carlo Simulation",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Monte Carlo Simulation")

st.markdown("""
Analyze project schedule uncertainty using Monte Carlo Simulation.
""")

# =====================================
# Inputs
# =====================================

project_id = st.selectbox(
    "Select Project",
    [
        "P001",
        "P002",
        "P003"
    ]
)

simulations = st.slider(
    "Number of Simulations",
    min_value=100,
    max_value=5000,
    value=1000,
    step=100
)

# =====================================
# Run Button
# =====================================

if st.button("Run Simulation"):

    try:

        summary = monte_carlo_summary(
            project_id,
            simulations
        )

        st.success(
            "Simulation Completed Successfully"
        )

        # =====================================
        # Metrics
        # =====================================

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Average Duration",
            summary["average"]
        )

        col2.metric(
            "P50",
            summary["p50"]
        )

        col3.metric(
            "P80",
            summary["p80"]
        )

        col4.metric(
            "P95",
            summary["p95"]
        )

        # =====================================
        # Summary Table
        # =====================================

        st.subheader(
            "Simulation Summary"
        )

        summary_df = pd.DataFrame({

            "Metric": [
                "Average",
                "P50",
                "P80",
                "P95",
                "Simulations"
            ],

            "Value": [
                summary["average"],
                summary["p50"],
                summary["p80"],
                summary["p95"],
                summary["simulations"]
            ]

        })

        st.dataframe(
            summary_df,
            use_container_width=True
        )

        # =====================================
        # Histogram
        # =====================================

        if "results" in summary:

            st.subheader(
                "Simulation Distribution"
            )

            df = pd.DataFrame({

                "Duration":
                summary["results"]

            })

            fig = px.histogram(
                df,
                x="Duration",
                nbins=30,
                title=f"Monte Carlo Distribution - {project_id}"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                """
                Histogram unavailable because
                simulation results were not
                returned by monte_carlo_summary().
                """
            )

        # =====================================
        # Risk Interpretation
        # =====================================

        st.subheader(
            "Risk Interpretation"
        )

        spread = (
            summary["p95"]
            -
            summary["average"]
        )

        if spread > 5:

            st.warning(
                """
                High uncertainty detected.

                The project schedule may vary
                significantly under risk conditions.
                """
            )

        elif spread > 2:

            st.info(
                """
                Moderate uncertainty detected.

                Project monitoring is recommended.
                """
            )

        else:

            st.success(
                """
                Low uncertainty detected.

                Schedule appears stable.
                """
            )

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )

        st.exception(e)