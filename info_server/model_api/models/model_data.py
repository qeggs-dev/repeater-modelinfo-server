from pydantic import BaseModel, Field
from .architecture import Architecture
from .pricing import Pricing
from .top_provider import TopProvider
from .supported_parameters import SupportedParameters
from .links import Links

class ModelAPIData(BaseModel):
    id: str = ""
    canonical_slug: str = ""
    hugging_face_id: str = ""
    name: str = ""
    created: int = 0
    description: str = ""
    context_length: int = 0
    architecture: Architecture = Field(default_factory=Architecture)
    pricing: Pricing = Field(default_factory=Pricing)
    top_provider: TopProvider = Field(default_factory=TopProvider)
    per_request_limits: None = None
    supported_parameters: list[SupportedParameters] = Field(default_factory=list)
    knowledge_cutoff: str | None = None
    expiration_date: str | None = None
    links: Links = Field(default_factory=Links)

class ModelAPIResponse(BaseModel):
    data: list[ModelAPIData] = Field(default_factory=list)