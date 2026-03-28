import random

from pydantic import BaseModel, Field, ConfigDict
from environs import Env
from ._model_type import ModelType

_env = Env()

class StaticModelAPI(BaseModel):
    name: str = ""
    url: str = ""
    id: str = ""
    api_key: str | None = None
    parent: str = ""
    uid: str = ""
    type: ModelType = ModelType.CHAT
    timeout: float = 600.0

class ModelAPI(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True
    )

    name: str = ""
    url: str = ""
    id: str = ""
    api_key_env: str | str = Field("API_KEY", exclude = True)
    parent: str = ""
    uid: str = ""
    type: ModelType = ModelType.CHAT
    timeout: float = 600.0

    def get_api_key(self) -> str | None:
        if isinstance(self.api_key_env, str):
            api_key_env = self.api_key_env
        elif isinstance(self.api_key_env, list):
            api_key_env = random.choice(self.api_key_env)
        else:
            raise ValueError("api_key_env must be a string or a list of strings")
        return _env.str(api_key_env, None)
    
    def to_static(self) -> StaticModelAPI:
        return StaticModelAPI(
            name = self.name,
            url = self.url,
            id = self.id,
            api_key = self.get_api_key(),
            parent = self.parent,
            uid = self.uid,
            type = self.type,
            timeout = self.timeout
        )