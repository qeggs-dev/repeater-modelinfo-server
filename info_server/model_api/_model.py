from pydantic import BaseModel, Field
from .models import ModelAPIData

class Model(BaseModel):
    name: str = ""
    url: str = ""
    proxy: str | None = None
    id: str = ""
    api_key: str | None = None
    parent: str = ""
    uid: str = ""
    model: ModelAPIData = Field(default_factory=ModelAPIData)
    timeout: float = 600.0