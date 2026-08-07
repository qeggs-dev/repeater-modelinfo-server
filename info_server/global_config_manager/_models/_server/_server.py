from pydantic import BaseModel, ConfigDict

class ServerConfig(BaseModel):
    host: str | None = None
    port: int | None = None
    api_key_env: str = "API_KEY"
    workers: int | None = None
    reload: bool | None = None
    run_server: bool = True