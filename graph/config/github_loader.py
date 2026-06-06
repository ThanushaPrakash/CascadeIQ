import requests

from graph.config.github_config import (
    GITHUB_TOKEN,
    OWNER,
    REPO
)

HEADERS = {
    "Authorization":
    f"Bearer {GITHUB_TOKEN}"
}


def get_repo_metrics():

    url = (
        f"https://api.github.com/repos/"
        f"{OWNER}/{REPO}"
    )

    response = requests.get(
        url,
        headers=HEADERS
    )

    return response.json()


if __name__ == "__main__":

    print(
        get_repo_metrics()
    )
