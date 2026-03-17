import sys
import uvicorn

from .api import Resource
from .global_config_manager import ConfigManager
from ._info import __version__
from loguru import logger

class Core:
    def __init__(self):
        self.resource = Resource()
    
    def init_resource(self):
        self.resource.init_all()
    
    @staticmethod
    def record_version():
        logger.info("Version: {version}", version = __version__)
        logger.info(
            "Running from python {version_major}.{version_minor}.{version_micro}",
            version_major = sys.version_info.major,
            version_minor = sys.version_info.minor,
            version_micro = sys.version_info.micro
        )
    
    def run(self):
        config = ConfigManager.get_configs()
        if config.server.run_server:
            uvicorn.run(
                app = self.resource.app,
                host = config.server.host,
                port = config.server.port,
                workers = config.server.workers,
                reload = config.server.reload,
                log_config = None
            )
    
    def one_key_run(self):
        self.init_resource()
        self.record_version()
        self.run()