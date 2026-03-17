from ..._resource import Resource
from ....model_api import ModelType
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from ....model_api import ModelAPI

class ModelInfoResponse(BaseModel):
    message: str = ""
    models: list[ModelAPI] = Field(default_factory=list)

@Resource.app.get("/model_info/{model_type}/{model_uid}")
def get_model_info(model_type: ModelType, model_uid: str):
    """
    Get model info
    """
    if not Resource.core.contains(model_type, model_uid):
        return JSONResponse(
            content = ModelInfoResponse(
                message = f"Model {model_type}/{model_uid} not found"
            ).model_dump(),
            status_code=404,
        )
    model_info: list[ModelAPI] = Resource.core.find_model(model_type, model_uid)
    return JSONResponse(
        content = ModelInfoResponse(
            message = f"Get Model {model_type}/{model_uid} successfully",
            models = model_info,
        ).model_dump(),
        status_code=200,
    )