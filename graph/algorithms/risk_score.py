from neo4j import GraphDatabase

from graph.algorithms.dora_metrics import (
    get_dora_metrics
)

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "cascade@123"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


def calculate_risk(project_id):

    query = """
    MATCH (p:Project {id:$project_id})

    OPTIONAL MATCH
    (t:Task)-[:PART_OF]->(p)

    OPTIONAL MATCH
    (t)-[d:DEPENDS_ON]->()

    OPTIONAL MATCH
    (r:Resource)-[:ASSIGNED_TO]->(t)

    RETURN

    count(DISTINCT d)
    AS dependencies,

    count(DISTINCT r)
    AS resources,

    count(
        DISTINCT CASE
        WHEN
        t.on_critical_path = true
        THEN t
        END
    )
    AS critical_tasks
    """

    with driver.session() as session:

        result = session.run(

            query,

            project_id=project_id

        ).single()

    dependencies = (
        result["dependencies"]
        or 0
    )

    resources = (
        result["resources"]
        or 0
    )

    critical_tasks = (
        result["critical_tasks"]
        or 0
    )

    risk_score = (

        dependencies * 3

        +

        resources * 5

        +

        critical_tasks * 10

    )

    # ======================
    # DORA Metrics
    # ======================

    dora = get_dora_metrics(
        project_id
    )

    if dora:

        if dora["lead_time"] > 10:

            risk_score += 20

        if dora["cfr"] > 15:

            risk_score += 25

        if dora["mttr"] > 1:

            risk_score += 15

        if dora[
            "deployment_frequency"
        ] < 10:

            risk_score += 10

    risk_score = min(
        100,
        int(risk_score)
    )

    if risk_score >= 80:

        risk_level = "🔴 High"

    elif risk_score >= 50:

        risk_level = "🟡 Medium"

    else:

        risk_level = "🟢 Low"

    return {

        "project_id":
        project_id,

        "risk_score":
        risk_score,

        "risk_level":
        risk_level,

        "dependencies":
        dependencies,

        "resources":
        resources,

        "critical_tasks":
        critical_tasks,

        "dora":
        dora

    }


if __name__ == "__main__":

    print(

        calculate_risk(
            "P001"
        )

    )