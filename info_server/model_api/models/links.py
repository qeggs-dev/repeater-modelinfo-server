from pydantic import BaseModel

class Links(BaseModel):
    details: str | None = None