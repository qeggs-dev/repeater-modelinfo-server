from ..._server import Server
from ....model_api import ModelType
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from fastapi import Query
from ....model_api import Model
from .._route import router

class ModelInfoResponse(BaseModel):
    message: str = ""
    models: list[Model] = Field(default_factory=list)

@router.get("/models")
def get_all_models():
    """
    Get all model info
    """
    models = Server.core.get_all_models()
    return JSONResponse(
        content = ModelInfoResponse(
            message = f"Get model info successfully.",
            models = models,
        ).model_dump(exclude_none=True),
        status_code=200,
    )