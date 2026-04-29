from ..._server import Server
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from ....model_api import Model
from .._route import router

class ModelInfoResponse(BaseModel):
    message: str = ""
    models: list[Model] = Field(default_factory=list)

@router.get("/model_info/{model_uid:path}")
def get_model_info(model_uid: str):
    """
    Get model info
    """
    models = Server.core.find_models(model_uid)
    return JSONResponse(
        content = ModelInfoResponse(
            message = f"Get Model {model_uid} successfully",
            models = models,
        ).model_dump(exclude_none=True),
        status_code=200,
    )