from pydantic import BaseModel, ConfigDict

class ModelAPIConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)
    
    api_file_path: str = "./configs/api_info.json"
    default_timeout: float = 600.0
    allow_schema_match: bool = False
    default_fuzzy_match_limit: int | None = 32
    refresh_interval: int | float = 21600.0