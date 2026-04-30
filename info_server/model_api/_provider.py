import re
import httpx
import random

from environs import Env
from typing import Callable
from .models import ModelAPIData, ModelAPIResponse
from ._configs_model import ProviderConfig
from ._model import Model
from loguru import logger

class ModelProvider:
    _env = Env()

    def __init__(
        self,
        id: str,
        name: str,
        base_url: str,
        api_key_env: str | list[str],
        proxy: str | None = None,
        models: list[ModelAPIData] | None = None,
        timeout: float = 600.0,
        client: httpx.AsyncClient | None = None
    ):
        self._id = id
        self._name = name
        self._base_url = base_url
        self._proxy = proxy
        self._timeout = timeout
        self._api_key_env = api_key_env
        self._models: dict[str, ModelAPIData] = {}
        if models is not None:
            self._models = {model.id: model for model in models}
        self._client = client or httpx.AsyncClient(
            base_url = base_url,
            proxy = proxy,
            timeout = timeout
        )
    
    @property
    def id(self):
        return self._id
    
    @property
    def uid(self):
        return f"{self._id}/{self._name}"
    
    @property
    def name(self):
        return self._name

    @property
    def base_url(self):
        return self._base_url

    @property
    def proxy(self):
        return self._proxy
    
    @property
    def models(self) -> list[ModelAPIData]:
        return list(self._models.values())
    
    @property
    def timeout(self):
        return self._timeout
    
    @property
    def api_key_env(self) -> str | list[str]:
        return self._api_key_env
    
    @property
    def client(self) -> httpx.AsyncClient:
        return self._client
    
    @property
    def api_keys(self) -> str | list[str | None] | None:
        if isinstance(self.api_key_env, str):
            return self._env.str(self.api_key_env, None)
        elif isinstance(self.api_key_env, list):
            return [self._env.str(api_key_env, None) for api_key_env in self.api_key_env]
        else:
            return None
    
    @property
    def random_api_key(self) -> str | None:
        if isinstance(self.api_key_env, str):
            return self.api_keys
        elif isinstance(self.api_key_env, list):
            return random.choice(self.api_keys)
        else:
            return None
    
    @property
    def headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.random_api_key}"
        }
    
    async def get_models(self) -> ModelAPIResponse:
        response = await self._client.get(
            "/models",
            headers = self.headers
        )
        response.raise_for_status()
        return ModelAPIResponse(**response.json())
    
    async def get_and_populates(self):
        response = await self.get_models()
        models = response.data
        self._models = {model.id: model for model in models}
    
    def _api_data_to_model(self, api_data: ModelAPIData) -> Model:
        return Model(
            name = api_data.name or api_data.id,
            url = self.base_url,
            proxy = self.proxy,
            id = api_data.id,
            uid = self.uid,
            api_key = self.random_api_key,
            parent_id = self.id,
            detailed = api_data,
            parent = self.name,
            timeout = self.timeout
        )
    
    def find_model(self, model_id: str) -> Model | None:
        if model_id in self._models:
            model_info = self._models[model_id]
            return self._api_data_to_model(model_info)
        else:
            return None
    
    def match_models(self, regex: re.Pattern[str], get_key: Callable[[str], str] = lambda x: x) -> list[Model]:
        return [
            self._api_data_to_model(model_info)
            for model_info in self._models.values()
            if regex.match(get_key(model_info.id))
        ]
    
    def get_all_models(self) -> list[Model]:
        return [self._api_data_to_model(model_info) for model_info in self._models.values()]
    
    @classmethod
    def from_config(cls, config: ProviderConfig, client: httpx.AsyncClient | None = None) -> "ModelProvider":
        return cls(
            name = config.name,
            id = config.id,
            base_url = config.url,
            api_key_env = config.api_key_env,
            proxy = config.proxy,
            models = config.models,
            timeout = config.timeout,
            client = client
        )
    
    def to_config(self) -> ProviderConfig:
        return ProviderConfig(
            name = self.name,
            id = self.id,
            url = self.base_url,
            api_key_env = self.api_key_env,
            proxy = self.proxy,
            models = self.models,
            timeout = self.timeout,
        )
    
    async def close(self):
        logger.info(
            "Closing Provider: {provider_name}({provider_id})",
            provider_name = self.name,
            provider_id = self.id
        )
        await self._client.aclose()