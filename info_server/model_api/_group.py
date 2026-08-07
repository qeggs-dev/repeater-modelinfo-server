import os
import re
import httpx
import orjson
import asyncio
import aiofiles
import jsonschema

from loguru import logger
from rapidfuzz import process
from pathlib import Path
from typing import Any, Generator, Callable
from pydantic import ValidationError
from ._configs_model import GroupConfig, ProviderConfig
from ._model import Model
from ._provider import ModelProvider
from ..lifespan import (
    StartHandler,
    ExitHandler
)

class ProviderGroup:
    _model_uid_pattern: re.Pattern[str] = re.compile(r"^(?P<group>.*?)/(?P<model>.*)$", re.IGNORECASE | re.DOTALL)
    _rematch_pattern: re.Pattern[str] = re.compile(r"^(?P<mode>match|search):(?P<regex>.+)$", re.IGNORECASE | re.DOTALL)
    _schema_pattern: re.Pattern[str] = re.compile(r"^(?P<mode>schema):(?P<schema>.+)$", re.IGNORECASE | re.DOTALL)
    _fuzz_pattern: re.Pattern[str] = re.compile(r"^(?P<mode>fuzzy):(?P<model_uid>.+):(?P<match_limit>\d+?)$", re.IGNORECASE | re.DOTALL)
    def __init__(
            self,
            groups: GroupConfig,
            refresh_interval : int | float = 21600,
            allow_schema_match: bool = False,
            default_fuzzy_match_limit: int | None = 32,
        ):
        self._providers: dict[str, ModelProvider] = {provider.id: ModelProvider.from_config(provider) for provider in groups.providers}
        self._groups: GroupConfig = groups
        self._refresh_interval: int | float = refresh_interval
        self._allow_schema_match: bool = allow_schema_match
        self._default_fuzzy_match_limit: int | None = default_fuzzy_match_limit
        StartHandler.add_function(self.init_library_file(groups.library_file))
        StartHandler.add_function(self.automatic_refresh())
        ExitHandler.add_function(self.close_and_save())
    
    @classmethod
    def from_file(
        cls,
        path: str | os.PathLike,
        refresh_interval: int | float = 21600,
        allow_schema_match: bool = False,
        default_fuzzy_match_limit: int | None = 32,
    ) -> "ProviderGroup":
        with open(path, "rb") as f:
            file_content = f.read()
        data = orjson.loads(file_content)
        config = GroupConfig(**data)
        return cls(
            config,
            refresh_interval = refresh_interval,
            allow_schema_match = allow_schema_match,
            default_fuzzy_match_limit = default_fuzzy_match_limit,
        )
    
    @classmethod
    async def from_file_async(
        cls,
        path: str | os.PathLike,
        refresh_interval: int | float = 21600,
        allow_schema_match: bool = False,
        default_fuzzy_match_limit: int | None = 32,
     ) -> "ProviderGroup":
        async with aiofiles.open(path, "rb") as f:
            file_content = await f.read()
        data = orjson.loads(file_content)
        config = GroupConfig(**data)
        return cls(
            config,
            refresh_interval = refresh_interval,
            allow_schema_match = allow_schema_match,
            default_fuzzy_match_limit = default_fuzzy_match_limit,
        )
    
    @property
    def groups(self) -> GroupConfig:
        return self._groups

    @property
    def providers(self) -> list[ModelProvider]:
        return list(self._providers.values())
    
    @property
    def allow_schema_match(self) -> bool:
        return self._allow_schema_match
    
    @property
    def model_uids(self) -> list[str]:
        uids: list[str] = list()
        for provider in self._providers.values():
            uids.extend(provider.uids)
        return uids
    
    @property
    def model_uid_tuples(self) -> list[tuple[str, str]]:
        uids: list[tuple[str, str]] = list()
        for provider in self._providers.values():
            uids.extend(provider.uid_tuples)
        return uids
    
    def find_models(self, model_id: str) -> list[Model]:
        if model_id.lower() == "all":
            matched_models = self.get_all_models()
            if matched_models:
                logger.info(
                    "Matched all models, total: {total}",
                    total = len(matched_models)
                )
                return matched_models
        
        if model_id in self._providers:
            provider = self._providers[model_id]
            matched_models = provider.get_all_models()
            if matched_models:
                logger.info(
                    "From Provider {provider}, matched {models_count} models",
                    provider = model_id,
                    models_count = len(matched_models)
                )
                return matched_models
        
        all_this_models = self.all_this_models(model_id)
        if all_this_models:
            logger.info(
                "Found {models_count} model {model_id} in all providers",
                model_id = model_id,
                models_count = len(all_this_models)
            )
            return all_this_models
        
        match_result = self._model_uid_pattern.match(model_id)
        if match_result:
            group_name = match_result.group("group")
            model_name = match_result.group("model")

            assert isinstance(group_name, str), f"Group name should be a string, but got {type(group_name).__name__}"
            assert isinstance(model_name, str), f"Model name should be a string, but got {type(model_name).__name__}"
            matched_model = self.match_uid(group_name, model_name)
            if matched_model:
                logger.info(
                    "Matched model uid: {model_id}",
                    model_id = model_id
                )
                return matched_model
        
        match_result = self._rematch_pattern.match(model_id)
        if match_result:
            mode = match_result.group("mode")
            regex = match_result.group("regex")

            assert isinstance(mode, str), f"Mode should be a string, but got {type(mode).__name__}"
            assert isinstance(regex, str), f"Regex should be a string, but got {type(regex).__name__}"
            matched_model = self.rematch_models(mode, regex)
            if matched_model:
                logger.info(
                    "Regex [{mode}] matched models: {models_count}",
                    mode = mode,
                    models_count = len(matched_model)
                )
                return matched_model
    
        match_result = self._schema_pattern.match(model_id)
        if match_result:
            schema = match_result.group("schema")
            model: list[Model] = self.schema_match_models(
                orjson.loads(
                    schema
                )
            )
            if model:
                logger.info(
                    "Schema matched models: {models_count}",
                    models_count = len(model)
                )
                return model
        
        match_result = self._fuzz_pattern.match(model_id)
        if match_result:
            model_uid = match_result.group("model_uid")
            match_limit = match_result.group("match_limit")

            assert isinstance(model_uid, str), f"Model UID should be a string, got {type(model_uid)}"
            assert isinstance(match_limit, str), f"Match limit should be a string, got {type(match_limit)}"

            match_limit = int(match_limit)
        else:
            model_uid = model_id
            match_limit = self._default_fuzzy_match_limit
        
        fuzzy_match_result = self.fuzzy_match_models(model_uid, match_limit)
        if fuzzy_match_result:
            logger.info(
                "Fuzzy matched models: {models_count}",
                models_count = len(fuzzy_match_result)
            )
            return fuzzy_match_result

        return []
    
    def get_model(self, provider_id: str, model_id: str) -> Model | None:
        provider = self._providers.get(provider_id)
        if provider is None:
            return None
        return provider.find_model(model_id)
    
    def match_uid(self, group_name: str, model_name: str) -> list[Model]:
        group = self._providers.get(group_name)
        if group is None:
            logger.warning(f"Group {group_name} not found")
            return []
        
        model = group.find_model(model_name)
        if model is None:
            logger.warning(f"Model {model_name} not found in group {group_name}")
            return []
        return [model]

    def all_this_models(self, model_id: str) -> list[Model]:
        list_of_models: list[Model] = []
        for provider in self._providers.values():
            model = provider.find_model(model_id)
            if model is not None:
                list_of_models.append(model)
                return list_of_models
        return list_of_models
    
    def rematch_models(self, mode: str, regex: str) -> list[Model]:
        pattern = re.compile(regex)
        match mode:
            case "match":
                model: list[Model] = self.regex_match_models(
                    lambda model_id: pattern.match(model_id) is not None
                )
            case "search":
                model: list[Model] = self.regex_match_models(
                    lambda model_id: pattern.search(model_id) is not None
                )
            case _:
                raise ValueError(f"Invalid mode: {mode}")
        return model
    
    def regex_match_models(self, matcher: Callable[[str], bool]) -> list[Model]:
        models: list[Model] = []
        for provider in self._providers.values():
            models.extend(
                provider.match_models(
                    matcher,
                    get_key = lambda model_id: f"{provider.id}/{model_id}"
                )
            )
        return models
    
    def fuzzy_match_models(self, model_uid: str, limit: int | None = None) -> list[Model]:

        if limit is not None and limit <= 0:
            return []
        
        model_uid_tuples = self.model_uid_tuples
        
        result = process.extract(
            model_uid,
            [f"{provider_uid}/{model_uid}" for provider_uid, model_uid in model_uid_tuples],
            limit = limit,
        )

        models: list[Model] = []
        for mathched, confidence, index in result:
            matched_provider_id, matched_model_id = model_uid_tuples[index]
            try:
                provider = self._providers[matched_provider_id]
            except KeyError:
                continue

            model = provider.find_model(matched_model_id)

            if model is not None:
                models.append(model)
        
        return models
    
    @staticmethod
    def _matcher(schema: jsonschema.Draft7Validator, models: list[Model]) -> Generator[Model, None, None]:
        for model in models:
            data = model.model_dump()
            try:
                schema.validate(data)
                yield model
            except jsonschema.ValidationError:
                continue

    def schema_match_models(self, schema: Any) -> list[Model]:
        validater = jsonschema.Draft7Validator(schema)
        if self._allow_schema_match:
            models = self.get_all_models()
            matched_models: list[Model] = []
            matched_models.extend(self._matcher(validater, models))
            return matched_models
        else:
            return []
    
    def get_all_models(self) -> list[Model]:
        models: list[Model] = []
        for group in self._providers.values():
            models.extend(group.get_all_models())
        return models
    
    async def _automatic_refresh(self):
        while True:
            await asyncio.sleep(self._refresh_interval)
            await self.get_and_populates()

    async def automatic_refresh(self):
        task = asyncio.create_task(self._automatic_refresh())
    
    async def _get_and_populates(self, provider: ModelProvider):
        try:
            await provider.get_and_populates()
        except httpx.HTTPStatusError as e:
            logger.warning(
                "{provider_name} failed to refresh model info ({code}): {message}",
                provider_name = provider.name,
                code = e.response.status_code,
                message = e.response.text
            )
        except httpx.RequestError as e:
            logger.warning(
                "{provider_name} failed to refresh model info ({message})",
                provider_name = provider.name,
                message = str(e)
            )
        except ValidationError as e:
            logger.warning(
                "{provider_name} failed to refresh model info ({message})",
                provider_name = provider.name,
                message = str(e)
            )
        except Exception as e:
            logger.exception(
                "{provider_name} failed to refresh model info",
                provider_name = provider.name
            )
    
    async def get_and_populates(self):
        tasks: set[asyncio.Task] = set()
        for provider in self._providers.values():
            task = asyncio.create_task(
                self._get_and_populates(provider)
            )
            tasks.add(task)
        await asyncio.gather(*tasks)
    
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
    
    async def to_providers_library(self, file: str | os.PathLike | None = None):
        if file is None:
            if self._groups.library_file is None:
                logger.warning(
                    "No library file specified, skipping saving"
                )
                return
            else:
                file = self._groups.library_file
        
        data = [provider.to_config().model_dump(exclude_none=True) for provider in self.all_providers()]
        file_content = orjson.dumps(data)
        async with aiofiles.open(file, "wb") as f:
            await f.write(file_content)
        logger.info(
            "Saved providers library to {file}",
            file = file
        )
    
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
    
    async def close_and_save(self):
        for provider in self._providers.values():
            await provider.close()
        
        await self.to_providers_library()