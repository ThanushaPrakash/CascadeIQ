import pandas as pd

FILE_PATH = r"D:\CascadeIQ\datasets\raw\dora_metrics.csv"


def get_dora_metrics(project_id):

    try:

        df = pd.read_csv(FILE_PATH)

    except Exception as e:

        print(
            f"Unable to load DORA file: {e}"
        )

        return None

    project = df[
        df["project_id"] == project_id
    ]

    if len(project) == 0:

        return None

    row = project.iloc[0]

    return {

        "deployment_frequency":
        float(
            row[
                "deployment_frequency"
            ]
        ),

        "lead_time":
        float(
            row[
                "lead_time"
            ]
        ),

        "cfr":
        float(
            row[
                "cfr"
            ]
        ),

        "mttr":
        float(
            row[
                "mttr"
            ]
        )

    }


if __name__ == "__main__":

    print(
        get_dora_metrics(
            "P001"
        )
    )