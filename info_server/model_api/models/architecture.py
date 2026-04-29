from pydantic import BaseModel, Field
from .modalities import Modalities

class Architecture(BaseModel):
    modality: str = ""
    input_modalities: list[Modalities] = Field(default_factory=list)
    output_modalities: list[Modalities] = Field(default_factory=list)
    tokenizer: str = ""
    instruct_type: str | None = None