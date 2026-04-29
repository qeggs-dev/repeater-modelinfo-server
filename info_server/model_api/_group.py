import os
import re
import orjson
import aiofiles

from loguru import logger
from ._configs_model import GroupConfig
from ._model import Model
from ._provider import ModelProvider
from ..lifespan import StartHandler

class ProviderGroup:
    _pattern: re.Pattern[str] = re.compile(r"^(?P<group>.*?)/(?P<model>.*)$", re.IGNORECASE | re.DOTALL)
    def __init__(self, groups: GroupConfig):
        self._providers: dict[str, ModelProvider] = self.parse_group(groups)
        StartHandler.add_function(self.get_and_populates())
    
    def parse_group(self, groups: GroupConfig) -> dict[str, ModelProvider]:
        return {group.name: ModelProvider.from_config(group) for group in groups.provider}
    
    def find_models(self, model_id: str) -> list[Model]:
        match_result = self._pattern.match(model_id)
        if match_result:
            group_name = match_result.group("group")
            model_name = match_result.group("model")

            assert isinstance(group_name, str), "Group name should be a string"
            assert isinstance(model_name, str), "Model name should be a string"

            group = self._providers.get(group_name)
            if group is None:
                logger.warning(f"Group {group_name} not found")
                return []
            
            model = group.find_model(model_name)
            if model is None:
                logger.warning(f"Model {model_name} not found in group {group_name}")
                return []
            return [model]
        else:
            models: list[Model] = []
            for group in self._providers.values():
                model = group.find_model(model_id)
                if model is not None:
                    models.append(model)
            return models
    
    def get_all_models(self) -> list[Model]:
        models: list[Model] = []
        for group in self._providers.values():
            models.extend(group.get_all_models())
        return models
    
    @classmethod
    def from_file(cls, path: str | os.PathLike) -> "ProviderGroup":
        with open(path, "rb") as f:
            file_content = f.read()
            data = orjson.loads(file_content)
            config = GroupConfig(**data)
            return cls(config)
    
    @classmethod
    async def from_file_async(cls, path: str | os.PathLike) -> "ProviderGroup":
        async with aiofiles.open(path, "rb") as f:
            file_content = await f.read()
            data = orjson.loads(file_content)
            config = GroupConfig(**data)
            return cls(config)
    
    async def get_and_populates(self):
        for group in self._providers.values():
            await group.get_and_populates()
    
    def all_providers(self) -> list[ModelProvider]:
        return list(self._providers.values())
    
    def get_provider(self, provider_id: str | None = None) -> ModelProvider:
        if provider_id in self._providers:
            return self._providers[provider_id]
        else:
            raise ValueError(f"Provider {provider_id} not found")
