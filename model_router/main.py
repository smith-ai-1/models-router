"""Main FastAPI application for the model router."""

import uvicorn
import inject
from fastapi import FastAPI
from contextlib import asynccontextmanager

from model_router.api.routes import router
from model_router.config import config
from model_router.main_configuration import main_configuration, initialize_sample_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    # Startup - configure dependency injection
    inject.configure_once(main_configuration)
    
    # Initialize sample data
    await initialize_sample_data()
    yield
    # Shutdown
    pass


# Validate configuration
config.validate_required_keys()

# Create FastAPI app
app = FastAPI(
    title="Model Router",
    version="1.0.0",
    description="OpenAI-compatible API for routing requests to multiple AI providers",
    lifespan=lifespan
)

# Include routes
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
