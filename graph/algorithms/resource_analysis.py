from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "cascade@123"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

def get_overloaded_resources():

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

        resources = []

        for row in result:

            resources.append({
                "resource_id": row["resource_id"],
                "resource_name": row["resource_name"],
                "assigned_tasks": row["assigned_tasks"]
            })

        return resources