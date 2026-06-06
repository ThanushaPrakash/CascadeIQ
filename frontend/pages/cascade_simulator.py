import streamlit as st
from neo4j import GraphDatabase
import pandas as pd

# -----------------------------
# Neo4j Connection
# -----------------------------

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "cascade@123"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

# -----------------------------
# Get Projects
# -----------------------------

def get_projects():

    query = """
    MATCH (p:Project)
    RETURN p.id AS id, p.name AS name
    ORDER BY p.id
    """

    with driver.session() as session:

        result = session.run(query)

        return [
            f"{record['id']} - {record['name']}"
            for record in result
        ]


# -----------------------------
# Impact Analysis
# -----------------------------

def find_impacted_projects(project_id):

    query = """
    MATCH (start_task:Task)-[:PART_OF]->(:Project {id:$project_id})

    WITH start_task
    ORDER BY start_task.id DESC
    LIMIT 1

    MATCH (start_task)-[:DEPENDS_ON*]->(affected:Task)

    MATCH (affected)-[:PART_OF]->(p:Project)

    RETURN DISTINCT
           p.id AS project_id,
           p.name AS project_name
    """

    with driver.session() as session:

        result = session.run(
            query,
            project_id=project_id
        )

        return pd.DataFrame(
            [record.data() for record in result]
        )


# -----------------------------
# UI
# -----------------------------

st.set_page_config(
    page_title="Cascade Simulator",
    layout="wide"
)

st.title("🚨 CascadeIQ Simulator")

st.markdown(
    "Simulate project delays and identify downstream impact."
)

projects = get_projects()

selected_project = st.selectbox(
    "Select Project",
    projects
)

delay_days = st.slider(
    "Delay Days",
    1,
    60,
    10
)

if st.button("Run Simulation"):

    project_id = selected_project.split(" - ")[0]

    impacted = find_impacted_projects(
        project_id
    )

    st.success(
        f"{project_id} delayed by {delay_days} days"
    )

    if impacted.empty:

        st.info(
            "No impacted downstream projects."
        )

    else:

        st.subheader(
            "Impacted Projects"
        )

        st.dataframe(
            impacted,
            use_container_width=True
        )

        st.metric(
            "Projects Impacted",
            len(impacted)
        )