from pydantic import BaseModel

class TopProvider(BaseModel):
    context_length: int | None = None
    max_completion_tokens: int | None = None
    is_moderated: bool = False