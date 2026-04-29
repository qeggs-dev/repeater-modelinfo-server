from pydantic import BaseModel

class TopProvider(BaseModel):
    context_length: int = 0
    max_completion_tokens: int = 0
    is_moderated: bool = False