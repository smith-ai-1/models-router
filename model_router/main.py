"""Main FastAPI application for the model router."""

import uvicorn
from fastapi import FastAPI

from model_router.api.routes import router
from model_router.config import config

# Validate configuration
config.validate_required_keys()

# Create FastAPI app
app = FastAPI(
    title="Model Router",
    version="1.0.0",
    description="OpenAI-compatible API for routing requests to multiple AI providers"
)

# Include routes
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
