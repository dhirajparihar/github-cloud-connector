from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import RedirectResponse

from app.config import (
    GITHUB_AUTH_URL,
    GITHUB_CLIENT_ID,
    GITHUB_CLIENT_SECRET,
    GITHUB_SCOPES,
    GITHUB_TOKEN_URL,
    REDIRECT_URI,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _build_auth_url() -> str:
    if not GITHUB_CLIENT_ID:
        raise HTTPException(
            status_code=500,
            detail="GITHUB_CLIENT_ID is not configured. Check your .env file.",
        )

    query = urlencode(
        {
            "client_id": GITHUB_CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "scope": GITHUB_SCOPES,
        }
    )
    return f"{GITHUB_AUTH_URL}?{query}"


@router.get("/login", summary="Redirect to GitHub OAuth login")
def login(request: Request):
    auth_url = _build_auth_url()
    accept = request.headers.get("accept", "")

    # Swagger UI and API clients usually request JSON.
    # Returning JSON avoids browser CORS/fetch issues on cross-site redirect.
    if "application/json" in accept:
        return {
            "message": "Open this URL in your browser to authenticate with GitHub.",
            "authorization_url": auth_url,
        }

    # Direct browser visit still gets redirected.
    return RedirectResponse(url=auth_url, status_code=307)


@router.get("/callback", summary="OAuth callback - exchange code for token")
def callback(code: str = Query(..., description="Temporary code returned by GitHub")):
    if not GITHUB_CLIENT_ID or not GITHUB_CLIENT_SECRET:
        raise HTTPException(
            status_code=500,
            detail="GITHUB_CLIENT_ID or GITHUB_CLIENT_SECRET is not configured.",
        )

    payload = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    try:
        response = httpx.post(
            GITHUB_TOKEN_URL,
            data=payload,
            headers={"Accept": "application/json"},
            timeout=10,
        )
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Could not reach GitHub OAuth endpoint: {exc}")

    data = response.json()
    if "error" in data:
        raise HTTPException(
            status_code=400,
            detail=f"GitHub OAuth error: {data.get('error_description', data['error'])}",
        )

    token = data.get("access_token")
    if not token:
        raise HTTPException(status_code=500, detail="Access token not found in GitHub response.")

    return {
        "message": "Authentication successful.",
        "access_token": token,
        "token_type": data.get("token_type", "bearer"),
        "scope": data.get("scope", ""),
    }
