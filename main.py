from dotenv import load_dotenv
import os
import requests

load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    raise RuntimeError("GITHUB_TOKEN not set")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
}

def get_owned_repos():
    repos = []
    page = 1

    while True:
        print(f"Fetching repos pages {page}")
        resp = requests.get(
            "https://api.github.com/user/repos",
            headers=HEADERS,
            params={
                "per_page": 100,
                "page": page,
                "affiliation": "owner",
            },
        )
        resp.raise_for_status()
        data = resp.json()

        if not data:
            break

        repos.extend(data)
        page += 1

    return repos

def get_repo_issues(owner, repo):
    issues = []
    page = 1

    while True:
        resp = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/issues",
            headers=HEADERS,
            params={
                "state": "all",
                "per_page": 100,
                "page": page,
            },
        )
        resp.raise_for_status()
        data = resp.json()

        if not data:
            break

        for issue in data:
            if "pull_request" not in issue:
                issues.append(issue)

        page += 1

    return issues

if __name__ == "__main__":
    print("Github Issue Script (GIS) started")

    repos = get_owned_repos()
    print(f"Found {len(repos)} owned repositories")

    all_issues = []

    for repo in repos:
        owner = repo["owner"]["login"]
        name = repo["name"]
        print(f"Fetching issues for {owner}/{name}")
        issues = get_repo_issues(owner, name)
        all_issues.extend(issues)

    print(f"\nFound {len(all_issues)} total issues:\n")

    for issue in all_issues:
        print(
            f"[{issue['repository_url'].split('/')[-2:] }] "
            f"[{issue['number']} - {issue['title']} ({issue['state']})]",
            (issue["html_url"])
        )