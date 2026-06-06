import streamlit as st
from neo4j import GraphDatabase
import pandas as pd

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "cascade@123"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

st.set_page_config(
    page_title="Project Drilldown",
    layout="wide"
)

st.title("📋 Project Drilldown")

# ======================================
# Project Dropdown
# ======================================

with driver.session() as session:

    projects = session.run(
        """
        MATCH (p:Project)
        RETURN p.id AS id,
               p.name AS name
        ORDER BY p.id
        """
    )

    project_list = [
        f"{r['id']} - {r['name']}"
        for r in projects
    ]

selected = st.selectbox(
    "Select Project",
    project_list
)

project_id = selected.split(" - ")[0]

# ======================================
# Project Info
# ======================================

query = """
MATCH (p:Project {id:$project_id})

OPTIONAL MATCH (t:Task)-[:PART_OF]->(p)

OPTIONAL MATCH (r:Resource)-[:ASSIGNED_TO]->(t)

RETURN
p.name AS name,
p.status AS status,
p.owner AS owner,
p.health_score AS health_score,

count(DISTINCT t) AS task_count,
count(DISTINCT r) AS resource_count
"""

with driver.session() as session:

    result = session.run(
        query,
        project_id=project_id
    ).single()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Health Score",
    result["health_score"]
)

col2.metric(
    "Tasks",
    result["task_count"]
)

col3.metric(
    "Resources",
    result["resource_count"]
)

col4.metric(
    "Status",
    result["status"]
)

st.markdown("---")

st.subheader("Project Details")

st.write(
    f"**Project:** {result['name']}"
)

st.write(
    f"**Owner:** {result['owner']}"
)

# ======================================
# Tasks Table
# ======================================

tasks_query = """
MATCH (t:Task)-[:PART_OF]->(:Project {id:$project_id})

RETURN
t.id AS task_id,
t.name AS task_name,
t.completion_pct AS completion,
t.float_days AS float_days,
t.on_critical_path AS critical
"""

with driver.session() as session:

    task_data = session.run(
        tasks_query,
        project_id=project_id
    )

    df = pd.DataFrame(
        [record.data() for record in task_data]
    )

st.subheader("Tasks")

st.dataframe(
    df,
    use_container_width=True
)

driver.close()