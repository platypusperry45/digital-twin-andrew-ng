"""
Digital Twin of Andrew Ng API
"""


from fastapi import FastAPI

from backend.api.router import router

from backend.core.lifecycle import lifespan

from backend.core.config import settings



app = FastAPI(

    title=settings.APP_NAME,

    version=settings.APP_VERSION,

    lifespan=lifespan,

)



app.include_router(
    router
)



@app.get("/")
def root():

    return {

        "name":
            settings.APP_NAME,

        "version":
            settings.APP_VERSION,

        "status":
            "running"

    }