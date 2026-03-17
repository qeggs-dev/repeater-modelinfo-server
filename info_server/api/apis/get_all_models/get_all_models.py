from ..._resource import Resource
from ....model_api import ModelType
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from ....model_api import ModelAPI

class ModelInfoResponse(BaseModel):
    message: str = ""
    models: list[ModelAPI] = Field(default_factory=list)

@Resource.app.get("/model_info/{model_type}")
def get_all_models(model_type: ModelType):
    """
    Get all model info
    """
    model_info = Resource.core.model_list(model_type)
    return JSONResponse(
        content = ModelInfoResponse(
            message = f"Get {model_type} model info successfully.",
            models = model_info,
        ).model_dump(),
        status_code=200,
    )