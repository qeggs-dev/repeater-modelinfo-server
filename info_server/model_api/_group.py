import os
import re
import aiofiles

from loguru import logger
from ._configs_model import GroupConfig
from ._model import Model
from ._provider import ModelProvider

class ProviderGroup:
    _pattern: re.Pattern[str] = re.compile(r"^(?P<group>.*?)/(?P<model>.*)$", re.IGNORECASE | re.DOTALL)
    def __init__(self, groups: GroupConfig):
        self._groups: dict[str, ModelProvider] = self.parse_group(groups)
    
    def parse_group(self, groups: GroupConfig) -> dict[str, ModelProvider]:
        return {group.name: ModelProvider.from_config(group) for group in groups.provider}
    
    def find_models(self, model_id: str) -> list[Model]:
        match_result = self._pattern.match(model_id)
        if match_result:
            group_name = match_result.group("group")
            model_name = match_result.group("model")

            assert isinstance(group_name, str), "Group name should be a string"
            assert isinstance(model_name, str), "Model name should be a string"

            group = self._groups.get(group_name)
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
            for group in self._groups.values():
                model = group.find_model(model_id)
                if model is not None:
                    models.append(model)
            return models
    
    def get_all_models(cls) -> list[Model]:
        models: list[Model] = []
        for group in cls._groups.values():
            models.extend(group.get_all_models())
    
    @classmethod
    def from_file(cls, path: str | os.PathLike, encoding = "utf-8") -> "ProviderGroup":
        with open(path, "r", encoding=encoding) as f:
            config = GroupConfig(**f.read())
            return cls(config)
    
    @classmethod
    async def from_file_async(cls, path: str | os.PathLike, encoding = "utf-8") -> "ProviderGroup":
        async with aiofiles.open(path, "r", encoding=encoding) as f:
            config = GroupConfig(**await f.read())
            return cls(config)