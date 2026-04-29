from fastapi import FastAPI
from ..lifespan import StartHandler, ExitHandler

class Lifespan:
    def __init__(self, app: FastAPI) -> None:
        self._app = app
    
    async def enter_lifespan(self):
        await StartHandler.execute()

    async def exit_lifespan(self):
        await ExitHandler.execute()
    
    async def __aenter__(self):
        return await self.enter_lifespan()
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        return await self.exit_lifespan()