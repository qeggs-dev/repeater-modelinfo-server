from ..._resource import Resource
from ....model_api import ModelType
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from fastapi import Query
from ....model_api import ModelAPI, StaticModelAPI

class ModelInfoResponse(BaseModel):
    message: str = ""
    models: list[ModelAPI | StaticModelAPI] = Field(default_factory=list)

@Resource.app.get("/model_info/{model_type}")
def get_all_models(model_type: ModelType, with_api_key: bool = Query(False)):
    """
    Get all model info
    """
    model_info = Resource.core.model_list(model_type)
    if with_api_key:
        model_info = [model.to_static() for model in model_info]
    return JSONResponse(
        content = ModelInfoResponse(
            message = f"Get {model_type} model info successfully.",
            models = model_info,
        ).model_dump(),
        status_code=200,
    )