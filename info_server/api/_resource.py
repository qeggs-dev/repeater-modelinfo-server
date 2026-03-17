import os
import yaml
import orjson

from pathlib import Path
from fastapi import FastAPI
from typing import ClassVar
from ..model_api import ModelAPIManager
from ..global_config_manager import ConfigManager, Global_Config
from .._info import __version__
from ..logger_init import logger_init
from environs import Env

class Resource:
    app: ClassVar[FastAPI] = FastAPI(
        title="Repeater Model API Info Server",
        description="Used to provide model information to the Repeater.",
        version = __version__,
    )
    envs: ClassVar[Env] = Env()
    core: ClassVar[ModelAPIManager | None] = None

    @classmethod
    def read_dotenv(cls, path: str | os.PathLike | None = None):
        cls.envs.read_env(path)

    @classmethod
    def init_config(cls):
        config_file_path = cls.envs.path("CONFIG_FILE_PATH", Path("./configs/main_configs.json"))
        if config_file_path.suffix == ".json":
            if config_file_path.exists():
                with open(config_file_path, "rb") as f:
                    configs = orjson.loads(f.read())
            else:
                config_file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(config_file_path, "wb") as f:
                    f.write(orjson.dumps(ConfigManager.get_configs().model_dump()))
                configs = {}
        elif config_file_path.suffix in (".yml", ".yaml"):
            if config_file_path.exists():
                with open(config_file_path, "r", encoding="utf-8") as f:
                    configs = yaml.safe_load(f)
            else:
                config_file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(config_file_path, "w", encoding="utf-8") as f:
                    f.write(yaml.safe_dump(ConfigManager.get_configs().model_dump()))
                configs = {}
        else:
            raise ValueError("Invalid config file format.")
        config = Global_Config(**configs)
        ConfigManager.update_configs(config)
    
    @classmethod
    def init_core(cls):
        cls.core = ModelAPIManager(
            case_sensitive = ConfigManager.get_configs().model_api.case_sensitive
        )
        cls.core.load(ConfigManager.get_configs().model_api.api_file_path)
    
    @staticmethod
    def init_logger():
        logger_init(ConfigManager.get_configs().logger)
    
    @classmethod
    def init_all(cls):
        cls.read_dotenv()
        cls.init_config()
        cls.init_logger()
        cls.init_core()