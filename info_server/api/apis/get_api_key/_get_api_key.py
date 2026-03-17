from ..._resource import Resource
from ....model_api import ModelType
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from ....model_api import ModelAPI

class ModelInfoResponse(BaseModel):
    message: str = ""
    api_keys: dict[str, str] = Field(default_factory=dict)

@Resource.app.get("/model_api_key/{model_type}/{model_uid}")
def get_api_key(model_type: ModelType, model_uid: str):
    """
    Get model api key
    """
    if not Resource.core.contains(model_type, model_uid):
        return JSONResponse(
            content = ModelInfoResponse(
                message = f"Model {model_type}/{model_uid} not found"
            ).model_dump(),
            status_code=404,
        )
    model_info = Resource.core.find_model(model_type, model_uid)
    response = ModelInfoResponse(
        message = f"Get Model {model_type}/{model_uid} api key successfully.",
    )
    for model in model_info:
        response.api_keys[model.uid] = model.get_api_key()
    return JSONResponse(
        content = response.model_dump(),
        status_code=200,
    )