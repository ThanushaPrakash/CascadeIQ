import streamlit as st
from neo4j import GraphDatabase
from pyvis.network import Network
import streamlit.components.v1 as components

# =====================================================
# Neo4j Connection
# =====================================================

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "cascade@123"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

# =====================================================
# Streamlit Page Config
# =====================================================

st.set_page_config(
    page_title="Dependency Graph",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 CascadeIQ Dependency Graph")

st.markdown("""
### Task Dependency Network

🔴 Critical Path Tasks  
🔵 Normal Tasks
""")

# =====================================================
# Neo4j Query
# =====================================================

query = """
MATCH (a:Task)-[:DEPENDS_ON]->(b:Task)

MATCH (a)-[:PART_OF]->(p1:Project)
MATCH (b)-[:PART_OF]->(p2:Project)

RETURN
a.id AS source_id,
a.name AS source_name,
a.completion_pct AS source_completion,
a.float_days AS source_float,
a.on_critical_path AS source_critical,
p1.name AS source_project,

b.id AS target_id,
b.name AS target_name,
b.completion_pct AS target_completion,
b.float_days AS target_float,
b.on_critical_path AS target_critical,
p2.name AS target_project
"""

# =====================================================
# Create Network
# =====================================================

net = Network(
    height="850px",
    width="100%",
    directed=True,
    bgcolor="#FFFFFF",
    font_color="#000000"
)

added_nodes = set()

# =====================================================
# Load Graph Data
# =====================================================

with driver.session() as session:

    result = session.run(query)

    for record in result:

        source_id = record["source_id"]
        target_id = record["target_id"]

        # -----------------------------
        # Source Node
        # -----------------------------

        if source_id not in added_nodes:

            source_color = (
                "#EF4444"
                if record["source_critical"]
                else "#3B82F6"
            )

            net.add_node(
                source_id,
                label=record["source_name"][:20],
                color=source_color,
                size=25,
                title=f"""
Task Name: {record['source_name']}

Task ID: {source_id}

Project: {record['source_project']}

Completion: {record['source_completion']}%

Float Days: {record['source_float']}

Critical Path: {'Yes' if record['source_critical'] else 'No'}
"""
            )

            added_nodes.add(source_id)

        # -----------------------------
        # Target Node
        # -----------------------------

        if target_id not in added_nodes:

            target_color = (
                "#EF4444"
                if record["target_critical"]
                else "#3B82F6"
            )

            net.add_node(
                target_id,
                label=record["target_name"][:20],
                color=target_color,
                size=25,
                title=f"""
Task Name: {record['target_name']}

Task ID: {target_id}

Project: {record['target_project']}

Completion: {record['target_completion']}%

Float Days: {record['target_float']}

Critical Path: {'Yes' if record['target_critical'] else 'No'}
"""
            )

            added_nodes.add(target_id)

        # -----------------------------
        # Edge
        # -----------------------------

        net.add_edge(
            source_id,
            target_id,
            color="#9CA3AF"
        )

# =====================================================
# Graph Styling
# =====================================================

net.set_options("""
{
  "nodes": {
    "shape": "dot",
    "size": 25,
    "font": {
      "size": 16,
      "face": "Arial"
    },
    "borderWidth": 2
  },

  "edges": {
    "smooth": {
      "enabled": true,
      "type": "continuous"
    },

    "color": {
      "inherit": false
    },

    "arrows": {
      "to": {
        "enabled": true,
        "scaleFactor": 0.8
      }
    }
  },

  "physics": {
    "enabled": false
  }
}
""")

# =====================================================
# Save Graph
# =====================================================

graph_path = "dependency_graph.html"

net.save_graph(graph_path)

# =====================================================
# Display Graph
# =====================================================

with open(
    graph_path,
    "r",
    encoding="utf-8"
) as f:

    html = f.read()

components.html(
    html,
    height=900,
    scrolling=True
)

# =====================================================
# Close Driver
# =====================================================

driver.close()