import httpx
from fastapi import HTTPException

DEFAULT_TIMEOUT = 10.0


def github_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }


def github_get(url: str, token: str, params: dict | None = None) -> dict | list:
    try:
        response = httpx.get(url, headers=github_headers(token), params=params, timeout=DEFAULT_TIMEOUT)
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Failed to reach GitHub API: {exc}")

    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="Invalid or expired GitHub token.")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="GitHub resource not found.")
    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=f"GitHub API error: {response.text}")

    return response.json()


def github_post(url: str, token: str, payload: dict) -> dict:
    try:
        response = httpx.post(url, headers=github_headers(token), json=payload, timeout=DEFAULT_TIMEOUT)
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Failed to reach GitHub API: {exc}")

    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="Invalid or expired GitHub token.")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="GitHub resource not found.")
    if response.status_code == 422:
        msg = response.json().get("message", response.text)
        raise HTTPException(status_code=422, detail=f"Validation failed: {msg}")
    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=f"GitHub API error: {response.text}")

    return response.json()
