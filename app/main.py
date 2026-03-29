from fastapi import FastAPI

from app.routes import auth, commits, issues, pull_requests, repos

app = FastAPI(
    title="GitHub Connector API",
    description=(
        "Simple backend assignment project that connects to GitHub APIs "
        "for repos, issues, pull requests, and commits."
    ),
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(repos.router)
app.include_router(issues.router)
app.include_router(pull_requests.router)
app.include_router(commits.router)


@app.get("/", tags=["Health"], summary="Health check")
def health_check():
    return {
        "status": "healthy",
        "service": "GitHub Connector API",
        "version": "1.0.0",
        "docs": "/docs",
    }
