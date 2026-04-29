from pydantic import BaseModel

class Pricing(BaseModel):
    prompt: str = "0"
    image: str = "0"
    audio: str = "0"
    completion: str = "0"
    internal_reasoning: str = "0"
    web_search: str = "0"
    input_cache_read: str = "0"
    input_cache_write: str = "0"