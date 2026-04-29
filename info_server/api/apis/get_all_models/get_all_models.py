import asyncio
from ..._server import Server
from pydantic import BaseModel, Field
from fastapi import Query
from fastapi.responses import JSONResponse
from ....model_api import Model

class ModelInfoResponse(BaseModel):
    message: str = ""
    models: list[Model] = Field(default_factory=list)

@Server.app.get("/models")
async def get_all_models(json_schema: str | None = Query(None), regex: str | None = Query(None)):
    """
    Get all model info
    """
    models: list[Model] = []
    if json_schema is None and regex is None:
        models.extend(Server.core.get_all_models())
    else:
        if json_schema is not None:
            models.extend(
                await asyncio.to_thread(
                    Server.core.schema_match_models,
                    json_schema
                )
            )
        if regex is not None:
            models.extend(
                await asyncio.to_thread(
                    Server.core.regex_match_models, 
                    regex
                )
            )
    return JSONResponse(
        content = ModelInfoResponse(
            message = f"Get model info successfully.",
            models = models,
        ).model_dump(exclude_none=True),
        status_code=200,
    )