from ..._resource import Resource
from ....model_api import ModelType
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from fastapi import Query
from ....model_api import ModelAPI, StaticModelAPI

class ModelInfoResponse(BaseModel):
    message: str = ""
    models: list[ModelAPI | StaticModelAPI] = Field(default_factory=list)

@Resource.app.get("/model_info/{model_type}/{model_uid}")
def get_model_info(model_type: ModelType, model_uid: str, with_api_key: bool = Query(False)):
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
    model_info: list[ModelAPI | StaticModelAPI] = Resource.core.find_model(model_type, model_uid)
    if with_api_key:
        model_info = [model.to_static() for model in model_info]
    return JSONResponse(
        content = ModelInfoResponse(
            message = f"Get Model {model_type}/{model_uid} successfully",
            models = model_info,
        ).model_dump(),
        status_code=200,
    )