from fastapi import FastAPI

from app.routers.procedure import api as procedure_router


def create_app():
    app = FastAPI()
    app.include_router(procedure_router, prefix="/procedure")

    return app
