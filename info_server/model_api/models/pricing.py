from pydantic import BaseModel

class Pricing(BaseModel):
    prompt: str | None = None
    image: str | None = None
    audio: str | None = None
    completion: str | None = None
    internal_reasoning: str | None = None
    web_search: str | None = None
    input_cache_read: str | None = None
    input_cache_write: str | None = None