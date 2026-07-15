from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.router import router
from backend.core.lifecycle import lifespan

app = FastAPI(
    title="Digital Twin of Andrew Ng",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)