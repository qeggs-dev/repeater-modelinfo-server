import os
import yaml
import orjson
import asyncio
import aiofiles
import threading
from pathlib import Path

from ._configs_model import ModelAPIConfig, ModelGroup
from ..global_config_manager import ConfigManager
from ._model_type import ModelType
from ._model_api import ModelAPI
from ._exceptions import *

class ModelAPIManager:
    def __init__(self, case_sensitive: bool = False):
        if not isinstance(case_sensitive, bool):
            raise TypeError("case_sensitive must be a boolean")
        self._models: dict[ModelType, dict[str, list[ModelAPI]]] = {}
        self._case_sensitive: bool = case_sensitive
        self._async_lock = asyncio.Lock()
        self._sync_lock = threading.Lock()

        # Initialize the indexs
        for model_type in ModelType:
            self._models[model_type] = {}

    def _create_model_group(self, api_data: list[dict]) -> ModelGroup:
        """Create a model groups instance from raw data."""
        return ModelGroup(api = api_data)

    def _parse_model_groups(self, raw_api_groups: list[dict]) -> None:
        """Parse raw model groups data and populate indexes."""
        default_timeout = ConfigManager.get_configs().model_api.default_timeout
        
        api_groups: ModelGroup = self._create_model_group(raw_api_groups)
        self._api_groups: ModelGroup = api_groups

        for group in api_groups.api:
            for model in group.models:

                if model.timeout is not None:
                    model_timeout: float = group.timeout
                elif group.timeout is not None:
                    model_timeout: float = group.timeout
                else:
                    model_timeout: float = default_timeout
                
                api_obj = ModelAPI(
                    name = model.name,
                    uid = model.uid,
                    id = model.id,
                    api_key_env = group.api_key_env,
                    parent = group.name,
                    url = model.url or group.url,
                    proxy = model.proxy or group.proxy,
                    type = model.type,
                    timeout = model_timeout,
                )
                if api_obj.uid not in self._models:
                    self._models[model.type][api_obj.uid] = [api_obj]
                else:
                    self._models[model.type][api_obj.uid].append(api_obj)

    def load(self, path: str | os.PathLike) -> None:
        """Load and parse model groups from a JSON/YAML file."""
        path: Path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"File \"{path}\" does not exist")
        with self._sync_lock:
            if path.suffix.lower() == ".json":
                try:
                    with open(path, "rb") as f:
                        fdata = f.read()
                        raw_api_groups: list[dict] = orjson.loads(fdata)
                        self._parse_model_groups(raw_api_groups)
                except orjson.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON format: {e}")
                except OSError as e:
                    raise IOError(f"Failed to read file: {e}")
            elif path.suffix.lower() == ".yaml" or path.suffix.lower() == ".yml":
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        fdata = f.read()
                        raw_api_groups: list[dict] = yaml.safe_load(fdata)
                        self._parse_model_groups(raw_api_groups)
                except yaml.YAMLError as e:
                    raise ValueError(f"Invalid YAML format: {e}")
                except OSError as e:
                    raise IOError(f"Failed to read file: {e}")
            else:
                raise ValueError(f"Invalid file format: {path.suffix}")

    async def load_async(self, path: str | os.PathLike) -> None:
        """Load and parse model groups from a JSON/YAML file."""
        path: Path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"File \"{path}\" does not exist")
        async with self._async_lock:
            if path.suffix.lower() == ".json":
                try:
                    async with aiofiles.open(path, "rb") as f:
                        fdata = await f.read()
                        raw_api_groups: list[dict] = orjson.loads(fdata)
                        await self._parse_model_groups(raw_api_groups)
                except orjson.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON format: {e}")
                except OSError as e:
                    raise IOError(f"Failed to read file: {e}")
            elif path.suffix.lower() == ".yaml" or path.suffix.lower() == ".yml":
                try:
                    async with aiofiles.open(path, "r", encoding="utf-8") as f:
                        fdata = await f.read()
                        raw_api_groups: list[dict] = yaml.safe_load(fdata)
                        await self._parse_model_groups(raw_api_groups)
                except yaml.YAMLError as e:
                    raise ValueError(f"Invalid YAML format: {e}")
                except OSError as e:
                    raise IOError(f"Failed to read file: {e}")
            else:
                raise ValueError(f"Invalid file format: {path.suffix}")
    
    def contains(self, model_type: ModelType, model_uid: str):
        if self._case_sensitive:
            key = model_uid
        else:
            key = model_uid.lower()
        if model_type in self._models:
            return key in self._models[model_type]
        return False

    def find_model(self, model_type: ModelType, model_uid: str, default: list[ModelAPI] | None = None) -> list[ModelAPI]:
        """Find model by model uid."""
        if self._case_sensitive:
            key = model_uid
        else:
            key = model_uid.lower()

        index_list = self._models[model_type].get(key, default)
        if index_list is None:
            return []
        
        return index_list.copy()

    def model_uid_list(self, model_type: ModelType) -> list[str]:
        """Get a list of all model uids."""
        if not isinstance(model_type, ModelType):
            raise TypeError("model_type must be an instance of ModelType")
        
        return list(self._models[model_type].keys())

    def model_list(self, model_type: ModelType) -> list[ModelAPI]:
        """Get a list of all model objects."""
        if not isinstance(model_type, ModelType):
            raise TypeError("model_type must be an instance of ModelType")
        
        model_list: list[ModelAPI] = []
        for model_uid_group in self._models[model_type].values():
            model_list.extend(model_uid_group)

        return model_list
    @property
    def empty_model(self) -> ModelAPI:
        return ModelAPI()