"""Server startup entry point separated from app definition."""

import os

import uvicorn


def run() -> None:
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))
    uvicorn.run("skeleton_api.main:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    run()
