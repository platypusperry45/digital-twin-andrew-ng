"""
Main FastAPI Application Entrypoint for Digital Twin of Andrew Ng.

Configures application lifecycle, CORS middleware, and central API routers.
"""

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from backend.core.lifecycle import lifespan
from backend.api.routes.chat import router as chat_router
from backend.api.routes.memory_dashboard import router as memory_dashboard_router

# Instantiate main FastAPI application with lifecycle context
app = FastAPI(
    title="Digital Twin of Andrew Ng API",
    description="Backend API supporting RAG, Memory, Persona Engine, and Visualization for Andrew Ng Digital Twin.",
    version="1.0.0",
    lifespan=lifespan,
)

# Enable CORS for frontend and client integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Central API Router under /api
api_router = APIRouter(prefix="/api")

# Register individual sub-routers
api_router.include_router(chat_router)
api_router.include_router(memory_dashboard_router)

# Mount central API router into FastAPI application
app.include_router(api_router)


@app.get("/", tags=["Health"])
def health_check():
    """Basic health check endpoint returning service status."""
    return {
        "status": "healthy",
        "service": "Andrew Ng Digital Twin API",
        "version": "1.0.0"
    }