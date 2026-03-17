from pydantic import BaseModel, ConfigDict, Field
from ._models import *

class Global_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    logger: LoggerConfig = Field(default_factory=LoggerConfig)
    model_api: ModelAPIConfig = Field(default_factory=ModelAPIConfig)
    server: ServerConfig = Field(default_factory=ServerConfig)