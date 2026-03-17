from pydantic import BaseModel, ConfigDict

class ModelAPIConfig(BaseModel):
    model_config = ConfigDict(case_sensitive=False)
    
    api_file_path: str = "./configs/api_info.json"
    case_sensitive: bool = False
    default_timeout: float = 600.0