from ..._resource import Resource
from ....model_api import ModelType
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from ....model_api import ModelAPI

class ModelInfoResponse(BaseModel):
    message: str = ""
    model_info: list[ModelAPI] = Field(default_factory=list)

@Resource.app.get("/model_info/{model_type}")
def get_all_info(model_type: ModelType):
    """
    Get all model info
    """
    model_info = Resource.core.model_list(model_type)
    return JSONResponse(
        content = ModelInfoResponse(
            message = f"Get {model_type} model info successfully.",
            model_info = model_info,
        ).model_dump(),
        status_code=200,
    )