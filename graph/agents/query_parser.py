import re

def parse_query(query):

    project_match = re.search(
        r"(P\d+)",
        query.upper()
    )

    delay_match = re.search(
        r"(\d+)\s*day",
        query.lower()
    )

    project_id = None
    delay_days = None

    if project_match:
        project_id = project_match.group(1)

    if delay_match:
        delay_days = int(
            delay_match.group(1)
        )

    return {
        "project_id": project_id,
        "delay_days": delay_days
    }


if __name__ == "__main__":

    print(
        parse_query(
            "What happens if P001 slips by 20 days?"
        )
    )