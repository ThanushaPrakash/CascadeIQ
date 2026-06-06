import streamlit as st
import pandas as pd

# =====================================
# Page Config
# =====================================

st.set_page_config(
    page_title="DORA Metrics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 DORA Metrics Dashboard")

# =====================================
# Load Data
# =====================================

df = pd.read_csv(
    r"D:\CascadeIQ\datasets\raw\dora_metrics.csv"
)

# =====================================
# KPI Cards
# =====================================

st.subheader(
    "Portfolio Engineering Health"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Avg Deployment Frequency",
    round(
        df["deployment_frequency"].mean(),
        2
    )
)

col2.metric(
    "Avg Lead Time",
    round(
        df["lead_time"].mean(),
        2
    )
)

col3.metric(
    "Avg CFR %",
    round(
        df["cfr"].mean(),
        2
    )
)

col4.metric(
    "Avg MTTR",
    round(
        df["mttr"].mean(),
        2
    )
)

# =====================================
# Data Table
# =====================================

st.subheader(
    "Project DORA Metrics"
)

st.dataframe(
    df,
    use_container_width=True
)

# =====================================
# Deployment Frequency
# =====================================

st.subheader(
    "Deployment Frequency"
)

st.bar_chart(
    df.set_index(
        "project_id"
    )[
        "deployment_frequency"
    ]
)

# =====================================
# Lead Time
# =====================================

st.subheader(
    "Lead Time"
)

st.bar_chart(
    df.set_index(
        "project_id"
    )[
        "lead_time"
    ]
)

# =====================================
# Change Failure Rate
# =====================================

st.subheader(
    "Change Failure Rate"
)

st.bar_chart(
    df.set_index(
        "project_id"
    )[
        "cfr"
    ]
)

# =====================================
# MTTR
# =====================================

st.subheader(
    "Mean Time To Restore"
)

st.bar_chart(
    df.set_index(
        "project_id"
    )[
        "mttr"
    ]
)

# =====================================
# Insights
# =====================================

st.subheader(
    "Portfolio Insights"
)

highest_risk = df.sort_values(
    "cfr",
    ascending=False
).iloc[0]

st.warning(

    f"""
    Highest Engineering Risk:

    Project:
    {highest_risk['project_id']}

    CFR:
    {highest_risk['cfr']}%
    """
)