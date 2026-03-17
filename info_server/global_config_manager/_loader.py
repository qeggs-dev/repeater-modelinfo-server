from __future__ import annotations

import os
import yaml
import shutil
import orjson

from pathlib import Path
from typing import ClassVar, Generator, Iterable

from ._base_model import Global_Config

class ConfigManager:
    _configs: ClassVar[Global_Config] = Global_Config()
    _instance: ClassVar[ConfigManager] | None = None

    @classmethod
    def get_configs(cls) -> Global_Config:
        return cls._configs

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def update_configs(cls, configs: Global_Config):
        if not isinstance(configs, Global_Config):
            raise TypeError("configs must be an instance of Global_Config")
        cls._configs = configs