from app.config import GITHUB_API_BASE
from app.utils.http_client import github_get, github_post


def fetch_user_repos(token: str) -> list:
    url = f"{GITHUB_API_BASE}/user/repos"
    return github_get(url, token, params={"per_page": 100, "sort": "pushed"})


def fetch_repos_by_owner(token: str, owner: str) -> list:
    url = f"{GITHUB_API_BASE}/users/{owner}/repos"
    return github_get(url, token, params={"per_page": 100, "sort": "pushed"})


def fetch_issues(token: str, owner: str, repo: str) -> list:
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues"
    return github_get(url, token, params={"per_page": 100, "state": "all"})


def create_issue(token: str, owner: str, repo: str, title: str, body: str) -> dict:
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues"
    return github_post(url, token, {"title": title, "body": body})


def create_pull_request(
    token: str,
    owner: str,
    repo: str,
    title: str,
    head: str,
    base: str,
    body: str,
) -> dict:
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/pulls"
    payload = {"title": title, "head": head, "base": base, "body": body}
    return github_post(url, token, payload)


def fetch_commits(token: str, owner: str, repo: str) -> list:
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/commits"
    return github_get(url, token, params={"per_page": 100})
