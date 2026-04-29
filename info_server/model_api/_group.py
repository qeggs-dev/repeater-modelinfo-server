import os
import re
import httpx
import orjson
import aiofiles
import jsonschema

from loguru import logger
from pathlib import Path
from typing import Any, Generator
from ._configs_model import GroupConfig, ProviderConfig
from ._model import Model
from ._provider import ModelProvider
from ..lifespan import (
    StartHandler,
    ExitHandler
)

class ProviderGroup:
    _pattern: re.Pattern[str] = re.compile(r"^(?P<group>.*?)/(?P<model>.*)$", re.IGNORECASE | re.DOTALL)
    def __init__(self, groups: GroupConfig):
        self._providers: dict[str, ModelProvider] = {provider.id: ModelProvider.from_config(provider) for provider in groups.providers}
        self._groups: GroupConfig = groups
        StartHandler.add_function(self.init_library_file(groups.library_file))
        ExitHandler.add_function(self.close_all())
    
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
    
    def regex_match_models(self, regex: re.Pattern[str]) -> list[Model]:
        models: list[Model] = []
        for provider in self._providers.values():
            models.extend(provider.match_models(regex, lambda x: f"{provider.id}/{x}"))

    def schema_match_models(self, schema: Any) -> list[Model]:
        models = self.get_all_models()
        def matcher(models: list[Model]) -> Generator[Model, None, None]:
            for model in models:
                data = model.model_dump()
                try:
                    jsonschema.validate(data, schema)
                    yield model
                except jsonschema.ValidationError:
                    continue
        matched_models: list[Model] = []
        matched_models.extend(matcher(models))
        return matched_models
    
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
        for provider in self._providers.values():
            try:
                await provider.get_and_populates()
            except httpx.HTTPStatusError as e:
                logger.warning(
                    "{provider_name} failed to refresh model info ({code}): {message}",
                    provider_name = provider.name,
                    code = e.response.status_code,
                    message = e.response.text
                )
    
    async def init_library_file(self, file: str | os.PathLike | None = None):
        if file is not None and Path(file).exists():
            await self.from_providers_library(file)
        else:
            await self.get_and_populates()
            if file is not None:
                await self.to_providers_library(file)
    
    async def from_providers_library(self, file: str | os.PathLike):
        async with aiofiles.open(file, "rb") as f:
            file_content = await f.read()
        data = orjson.loads(file_content)
        if not isinstance(data, list):
            raise ValueError("Providers library must be a list of providers")
        
        providers: dict[str, ModelProvider] = {}
        for provider_data in data:
            config = ProviderConfig(**provider_data)
            if config.id in self._providers:
                client = self._providers[config.id].client
            else:
                client = None
            provider = ModelProvider.from_config(config, client = client)
            if provider.id in providers:
                logger.warning(
                    "There are two providers {provider_name_1} and {provider_name_2} with the same ID, and the program will override the previous one, which you probably don't want.",
                    provider_name_1 = provider.name,
                    provider_name_2 = providers[provider.id].name
                )
            providers[provider.id] = provider
        self._providers = providers
    
    async def to_providers_library(self, file: str | os.PathLike):
        data = [provider.to_config().model_dump(exclude_none=True) for provider in self.all_providers()]
        file_content = orjson.dumps(data)
        async with aiofiles.open(file, "wb") as f:
            await f.write(file_content)
    
    def all_providers(self) -> list[ModelProvider]:
        return list(self._providers.values())
    
    def get_provider(self, provider_id: str) -> ModelProvider:
        if provider_id in self._providers:
            return self._providers[provider_id]
        else:
            raise ValueError(f"Provider {provider_id} not found")

    async def close(self, provider_id: str) -> ModelProvider:
        if provider_id in self._providers:
            provider = self._providers.pop(provider_id)
            await provider.close()
            return provider
        else:
            raise ValueError(f"Provider {provider_id} not found")
    
    async def close_all(self):
        for provider in self._providers.values():
            await provider.close()