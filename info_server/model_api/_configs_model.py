from pydantic import BaseModel, Field
from typing import Literal
from .models import ModelAPIData

class ProviderConfig(BaseModel):
    url: str = ""
    max_connections: int | None = None
    max_keepalive_connections: int | None = None
    keepalive_expiry: int | float | None = 5
    proxy: str | None = None

    name: str = ""
    id: str = ""
    api_key_env: str | list[str] = "API_KEY"
    models: list[ModelAPIData] | None = None
    timeout: float = 600.0
    
class GroupConfig(BaseModel):
    type: Literal["model_group_config.v1"] = "model_group_config.v1"
    providers: list[ProviderConfig] = Field(default_factory=list)
    library_file: str | None = None