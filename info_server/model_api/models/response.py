from pydantic import BaseModel, Field
from .model_data import ModelAPIData

class ModelAPIResponse(BaseModel):
    data: list[ModelAPIData] = Field(default_factory=list)