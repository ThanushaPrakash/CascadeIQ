def validate_output(state):

    errors = []

    if not state.get("risk"):

        errors.append(
            "Missing risk analysis"
        )

    if not state.get(
        "recommendations"
    ):

        errors.append(
            "Missing recommendations"
        )

    if not state.get(
        "narrative"
    ):

        errors.append(
            "Missing narrative"
        )

    if len(errors) == 0:

        state["validation"] = {

            "status":
            "PASSED"

        }

    else:

        state["validation"] = {

            "status":
            "FAILED",

            "errors":
            errors

        }

    return state


if __name__ == "__main__":

    sample = {

        "risk": {},

        "recommendations": [
            "Review dependencies"
        ],

        "narrative":
        "Project is high risk"

    }

    print(
        validate_output(
            sample
        )
    )