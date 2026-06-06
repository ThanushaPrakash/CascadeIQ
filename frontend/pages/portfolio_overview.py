import streamlit as st
import pandas as pd
import plotly.express as px

from graph.algorithms.risk_score import (
    calculate_risk
)

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Portfolio Overview",
    page_icon="📊",
    layout="wide"
)

st.title("📊 CascadeIQ Portfolio Overview")

st.markdown("""
Executive view of project portfolio health,
risk exposure, and AI activity.
""")

# =====================================
# PROJECT LIST
# =====================================

projects = [
    "P001",
    "P002",
    "P003"
]

# =====================================
# COLLECT RISK DATA
# =====================================

risk_data = []

for project in projects:

    try:

        risk = calculate_risk(
            project
        )

        risk_data.append(
            risk
        )

    except Exception as e:

        st.error(
            f"Failed loading {project}: {e}"
        )

if len(risk_data) == 0:

    st.error(
        "No project data available."
    )

    st.stop()

df = pd.DataFrame(
    risk_data
)

# =====================================
# KPI SECTION
# =====================================

st.subheader(
    "Executive Portfolio KPIs"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Projects",
    len(df)
)

col2.metric(
    "Average Risk",
    round(
        df["risk_score"].mean(),
        2
    )
)

col3.metric(
    "High Risk Projects",
    len(
        df[
            df["risk_score"] >= 80
        ]
    )
)

col4.metric(
    "Critical Tasks",
    int(
        df[
            "critical_tasks"
        ].sum()
    )
)

# =====================================
# PORTFOLIO RISK TABLE
# =====================================

st.subheader(
    "Portfolio Risk Summary"
)

st.dataframe(
    df,
    use_container_width=True
)

# =====================================
# RISK DISTRIBUTION CHART
# =====================================

st.subheader(
    "Portfolio Risk Distribution"
)

fig = px.bar(
    df,
    x="project_id",
    y="risk_score",
    color="risk_score",
    text="risk_score",
    title="Project Risk Scores"
)

fig.update_layout(
    xaxis_title="Project",
    yaxis_title="Risk Score"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================
# HIGH RISK PROJECTS
# =====================================

st.subheader(
    "High Risk Projects"
)

high_risk = df[
    df["risk_score"] >= 80
]

if len(high_risk) > 0:

    st.warning(
        f"{len(high_risk)} high-risk projects detected."
    )

    st.dataframe(
        high_risk,
        use_container_width=True
    )

else:

    st.success(
        "No high-risk projects detected."
    )

# =====================================
# PORTFOLIO ALERTS
# =====================================

st.subheader(
    "Portfolio Alerts"
)

if len(high_risk) > 0:

    for _, row in high_risk.iterrows():

        st.error(
            f"🔴 {row['project_id']} "
            f"has Risk Score "
            f"{row['risk_score']}"
        )

else:

    st.success(
        "No active portfolio alerts."
    )

# =====================================
# RECENT AI ACTIVITY
# =====================================

st.subheader(
    "Recent AI Activity"
)

try:

    logs = pd.read_csv(
        r"D:\cascadeIQ\datasets\processed\audit_log.csv"
    )

    st.dataframe(

        logs.tail(10),

        use_container_width=True

    )

except Exception:

    st.info(
        "No audit logs available."
    )

# =====================================
# PORTFOLIO HEALTH SCORE
# =====================================

st.subheader(
    "Portfolio Health"
)

avg_risk = df[
    "risk_score"
].mean()

if avg_risk >= 80:

    st.error(
        "🔴 Portfolio Health: High Risk"
    )

elif avg_risk >= 50:

    st.warning(
        "🟠 Portfolio Health: Medium Risk"
    )

else:

    st.success(
        "🟢 Portfolio Health: Healthy"
    )