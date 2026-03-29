# GitHub Connector (Back-end Assignment)

This is a simple FastAPI project for the back-end assignment.
It connects to GitHub and exposes REST endpoints for common actions.

## Assignment Coverage

- Authentication: PAT is supported by sending `Authorization: Bearer <token>`.
- OAuth 2.0 (Bonus)
                - OAuth 2.0 flow is implemented as an additional feature.
- API Integration: real GitHub API calls implemented for:
  - Fetch repositories
  - List issues
  - Create issue
  - Fetch commits
  - Create pull request (bonus)
- Interface: REST API using FastAPI
- Code quality: modular files (`routes`, `services`, `utils`) and error handling

## Tech Stack

- Python 3.10+
- FastAPI
- httpx
- Uvicorn

## Project Structure

```text
app/
  main.py
  config.py
  dependencies.py
  routes/
    auth.py
    repos.py
    issues.py
    pull_requests.py
    commits.py
  services/
    github.py
  utils/
    http_client.py
```

## Setup

1. Create and activate virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create `.env` from sample:

```bash
copy .env.example .env
```

4. Fill `.env`:

```env
GITHUB_CLIENT_ID=your_client_id
GITHUB_CLIENT_SECRET=your_client_secret
REDIRECT_URI=http://localhost:8000/auth/callback
```

5. Run server:

```bash
uvicorn app.main:app --reload
```

- Base URL: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`

## Authentication Notes

- For protected endpoints, send your GitHub Personal Access Token:

```text
Authorization: Bearer <your_pat>
```

- OAuth flow is also available as bonus:
  - `GET /auth/login` (JSON for API clients, redirect for direct browser open)
  - `GET /auth/callback?code=...`

## Endpoints

- `GET /` - health check
- `GET /auth/login` - OAuth login (JSON or redirect)
- `GET /auth/callback` - OAuth callback/token exchange
- `GET /repos` - authenticated user repos
- `GET /repos/{owner}` - repos by owner
- `GET /issues?owner=<owner>&repo=<repo>` - list issues
- `POST /create-issue` - create issue
- `POST /create-pr` - create pull request
- `GET /commits?owner=<owner>&repo=<repo>` - list commits

## Example Requests

List repos:

```bash
curl -H "Authorization: Bearer <your_pat>" http://localhost:8000/repos
```

Create issue:

```bash
curl -X POST http://localhost:8000/create-issue \
  -H "Authorization: Bearer <your_pat>" \
  -H "Content-Type: application/json" \
  -d '{
    "owner": "your-username",
    "repo": "your-repo",
    "title": "Test issue",
    "body": "Created from assignment API"
  }'
```
