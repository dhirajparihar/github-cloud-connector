from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.dependencies import extract_bearer_token
from app.services.github import create_pull_request

router = APIRouter(tags=["Pull Requests"])


class CreatePRRequest(BaseModel):
    owner: str = Field(..., min_length=1)
    repo: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1, max_length=256)
    head: str = Field(..., min_length=1)
    base: str = Field(..., min_length=1)
    body: str = ""


@router.post("/create-pr", summary="Create a pull request", status_code=201)
def new_pull_request(payload: CreatePRRequest, token: str = Depends(extract_bearer_token)):
    result = create_pull_request(
        token,
        payload.owner,
        payload.repo,
        payload.title,
        payload.head,
        payload.base,
        payload.body,
    )
    return {
        "message": "Pull request created successfully.",
        "pr_number": result.get("number"),
        "html_url": result.get("html_url"),
        "pull_request": result,
    }
