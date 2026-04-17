from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI(title="Omni Mind Web")

BASE_DIR = Path(__file__).resolve().parent


@app.get("/", include_in_schema=False)
async def root_redirect():
    return RedirectResponse(url="/landing.html")


@app.api_route(
    "/api/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    include_in_schema=False,
)
async def api_passthrough(path: str):
    # Forward frontend API calls to the backend service prefix.
    return RedirectResponse(url=f"/_/backend/api/{path}", status_code=307)


# Serve all static frontend assets and HTML pages from ux design directory.
app.mount("/", StaticFiles(directory=str(BASE_DIR), html=True), name="frontend")
