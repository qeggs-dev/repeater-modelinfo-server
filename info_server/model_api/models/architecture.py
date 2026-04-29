from pydantic import BaseModel, Field
from .modalities import Modalities

class Architecture(BaseModel):
    modality: str | None = None
    input_modalities: list[Modalities] | None = None
    output_modalities: list[Modalities] | None = None
    tokenizer: str | None = None
    instruct_type: str | None = None