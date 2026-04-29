from pydantic import BaseModel, Field
from typing import Literal
from .models import ModelAPIData

class ProviderConfig(BaseModel):
    name: str = ""
    id: str = ""
    api_key_env: str | list[str] = "API_KEY"
    url: str = ""
    proxy: str | None = None
    models: list[ModelAPIData] | None = None
    timeout: float = 600.0
    
class GroupConfig(BaseModel):
    type: Literal["model_group_config.v1"] = "model_group_config.v1"
    providers: list[ProviderConfig] = Field(default_factory=list)
    library_file: str | None = None