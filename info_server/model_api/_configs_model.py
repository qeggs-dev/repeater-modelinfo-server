from pydantic import BaseModel, Field
from typing import Literal

class ProviderConfig(BaseModel):
    name: str = ""
    api_key_env: str | list[str] = "API_KEY"
    url: str = ""
    proxy: str | None = None
    timeout: float = 600.0
    
class GroupConfig(BaseModel):
    type: Literal["model_group_config.v1"] = "model_group_config.v1"
    provider: list[ProviderConfig] = Field(default_factory=list)