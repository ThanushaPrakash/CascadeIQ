from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "cascade@123"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


def propagate_delay(
        project_id,
        initial_delay):

    query = """
    MATCH (start_task:Task)
          -[:PART_OF]->
          (:Project {id:$project_id})

    WITH start_task
    ORDER BY start_task.id DESC
    LIMIT 1

    MATCH path=
    (start_task)-[:DEPENDS_ON*]->
    (affected:Task)

    MATCH (affected)-[:PART_OF]->
          (p:Project)

    RETURN DISTINCT

    affected.id AS task_id,

    affected.name AS task_name,

    affected.float_days AS float_days,

    affected.on_critical_path AS critical,

    p.id AS project_id,

    p.name AS project_name
    """

    impacted = []

    with driver.session() as session:

        result = session.run(
            query,
            project_id=project_id
        )

        for record in result:

            float_days = (
                record["float_days"]
                if record["float_days"]
                else 0
            )

            critical_bonus = (
                2
                if record["critical"]
                else 0
            )

            propagated_delay = max(
                0,
                initial_delay
                - float_days
                + critical_bonus
            )

            impacted.append({

                "task_id":
                record["task_id"],

                "task_name":
                record["task_name"],

                "project_id":
                record["project_id"],

                "project_name":
                record["project_name"],

                "impact_days":
                propagated_delay,

                "critical":
                record["critical"]
            })

    return impacted


if __name__ == "__main__":

    impacts = propagate_delay(
        "P001",
        15
    )

    print()

    for row in impacts:

        print(row)

