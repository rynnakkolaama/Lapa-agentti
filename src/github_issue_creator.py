import os
from github import Github

def create_issue(title, body):
    """
    Luo GitHub Issue repositoryyn.
    """

    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPOSITORY")  # esim. "käyttäjä/repo"

    g = Github(token)
    repo = g.get_repo(repo_name)

    repo.create_issue(
        title=title,
        body=body,
        labels=["lausunto", "380-2023"]
    )


if __name__ == "__main__":
    # Testi
    body = """
### Lausuntopyyntö

Tämä on testiviesti AI-agentilta.
"""
    create_issue(
        title="Testi: Lausuntopyyntö 380/2023",
        body=body
    )
