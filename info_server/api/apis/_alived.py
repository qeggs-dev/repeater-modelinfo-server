from .._server import Server
from fastapi.responses import PlainTextResponse

@Server.app.get("/alived")
def alived():
    return PlainTextResponse("OK")