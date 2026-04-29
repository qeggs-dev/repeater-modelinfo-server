from ..._server import Server
from fastapi.responses import JSONResponse

@Server.app.post("/refresh")
async def refresh_all():
    """
    Refresh all model info from providers
    """
    await Server.core.get_and_populates()
    await Server.core.to_providers_library()
    return JSONResponse(
        content={
            "message": "Model info refreshed successfully",
            "status": "ok"
        },
        status_code=200
    )