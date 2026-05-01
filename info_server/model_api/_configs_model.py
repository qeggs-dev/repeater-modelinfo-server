from pydantic import BaseModel, Field
from typing import Literal
from .models import ModelAPIData

class HTTPLimit(BaseModel):
    max_connections: int | None = 100
    max_keepalive_connections: int | None = 20
    keepalive_expiry: int | float | None = 5

class HTTPTimeouts(BaseModel):
    connect: int | float | None = 5
    read: int | float | None = 5
    write: int | float | None = 5
    pool: int | float | None = None

class ProviderConfig(BaseModel):
    url: str = ""
    limit: HTTPLimit | None = None
    timeout: int | float | HTTPTimeouts | None = None
    proxy: str | None = None

    name: str = ""
    id: str = ""
    api_key_env: str | list[str] = "API_KEY"
    models: list[ModelAPIData] | None = None
    
class GroupConfig(BaseModel):
    type: Literal["model_group_config.v1"] = "model_group_config.v1"
    providers: list[ProviderConfig] = Field(default_factory=list)
    library_file: str | None = None