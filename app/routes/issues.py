from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from app.dependencies import extract_bearer_token
from app.services.github import create_issue, fetch_issues

router = APIRouter(tags=["Issues"])


class CreateIssueRequest(BaseModel):
    owner: str = Field(..., min_length=1)
    repo: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1, max_length=256)
    body: str = ""


@router.get("/issues", summary="List issues from a repository")
def list_issues(
    owner: str = Query(..., description="Repository owner"),
    repo: str = Query(..., description="Repository name"),
    token: str = Depends(extract_bearer_token),
):
    issues = fetch_issues(token, owner, repo)
    return {"owner": owner, "repo": repo, "count": len(issues), "issues": issues}


@router.post("/create-issue", summary="Create a new issue", status_code=201)
def new_issue(payload: CreateIssueRequest, token: str = Depends(extract_bearer_token)):
    result = create_issue(token, payload.owner, payload.repo, payload.title, payload.body)
    return {
        "message": "Issue created successfully.",
        "issue_number": result.get("number"),
        "html_url": result.get("html_url"),
        "issue": result,
    }
