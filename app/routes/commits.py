from fastapi import APIRouter, Depends, Query

from app.dependencies import extract_bearer_token
from app.services.github import fetch_commits

router = APIRouter(tags=["Commits"])


@router.get("/commits", summary="Fetch commits from a repository")
def list_commits(
    owner: str = Query(..., description="Repository owner"),
    repo: str = Query(..., description="Repository name"),
    token: str = Depends(extract_bearer_token),
):
    commits = fetch_commits(token, owner, repo)
    return {"owner": owner, "repo": repo, "count": len(commits), "commits": commits}
