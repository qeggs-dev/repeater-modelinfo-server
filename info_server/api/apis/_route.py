from fastapi import APIRouter
from .._server import Server

router = APIRouter(
    prefix="/v1",
    tags=["v1 api routes"]
)

Server.include_router(router)