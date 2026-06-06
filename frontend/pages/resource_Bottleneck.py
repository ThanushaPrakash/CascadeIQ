import streamlit as st
from neo4j import GraphDatabase
import pandas as pd

# =====================================
# Neo4j Connection
# =====================================

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "cascade@123"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

st.set_page_config(
    page_title="Resource Bottlenecks",
    page_icon="⚠️",
    layout="wide"
)

st.title("⚠️ Resource Bottleneck Detector")

st.markdown(
    """
    Detect overloaded resources that may create
    project delivery risks.
    """
)

# =====================================
# Resource Utilization Query
# =====================================

query = """
MATCH (r:Resource)-[:ASSIGNED_TO]->(t:Task)

RETURN

r.id AS resource_id,
r.name AS resource_name,

count(t) AS assigned_tasks

ORDER BY assigned_tasks DESC
"""

with driver.session() as session:

    result = session.run(query)

    data = [record.data() for record in result]

df = pd.DataFrame(data)

# =====================================
# Utilization Logic
# =====================================

df["utilization_pct"] = (
    df["assigned_tasks"] * 25
)

# =====================================
# Risk Category
# =====================================

def risk_level(util):

    if util > 100:
        return "🔴 Critical"

    elif util > 75:
        return "🟡 High"

    else:
        return "🟢 Normal"

df["risk"] = df["utilization_pct"].apply(
    risk_level
)

# =====================================
# Metrics
# =====================================

critical_count = len(
    df[df["utilization_pct"] > 100]
)

high_count = len(
    df[
        (df["utilization_pct"] > 75)
        &
        (df["utilization_pct"] <= 100)
    ]
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Resources",
    len(df)
)

col2.metric(
    "Critical Resources",
    critical_count
)

col3.metric(
    "High Risk Resources",
    high_count
)

st.markdown("---")

# =====================================
# Resource Table
# =====================================

st.subheader(
    "Resource Utilization"
)

st.dataframe(
    df,
    use_container_width=True
)

st.markdown("---")

# =====================================
# Resource Detail View
# =====================================

resource_options = (
    df["resource_id"]
    + " - "
    + df["resource_name"]
).tolist()

selected_resource = st.selectbox(
    "Select Resource",
    resource_options
)

resource_id = selected_resource.split(" - ")[0]

# =====================================
# Assigned Tasks
# =====================================

task_query = """
MATCH (r:Resource {id:$resource_id})
      -[:ASSIGNED_TO]->
      (t:Task)

MATCH (t)-[:PART_OF]->(p:Project)

RETURN

t.id AS task_id,
t.name AS task_name,
p.name AS project_name
"""

with driver.session() as session:

    result = session.run(
        task_query,
        resource_id=resource_id
    )

    task_df = pd.DataFrame(
        [record.data() for record in result]
    )

st.subheader(
    "Assigned Tasks"
)

st.dataframe(
    task_df,
    use_container_width=True
)

driver.close()