from fastapi import APIRouter, Depends

from app.dependencies import extract_bearer_token
from app.services.github import fetch_repos_by_owner, fetch_user_repos

router = APIRouter(tags=["Repositories"])


@router.get("/repos", summary="Fetch authenticated user's repositories")
def get_my_repos(token: str = Depends(extract_bearer_token)):
    repos = fetch_user_repos(token)
    return {"count": len(repos), "repositories": repos}


@router.get("/repos/{owner}", summary="Fetch repositories for a user/org")
def get_repos_by_owner(owner: str, token: str = Depends(extract_bearer_token)):
    repos = fetch_repos_by_owner(token, owner)
    return {"owner": owner, "count": len(repos), "repositories": repos}
