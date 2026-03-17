import traceback

from fastapi import Request, Response
from typing import Callable, Awaitable
from datetime import datetime
from pydantic import BaseModel
from loguru import logger

class ExceptionResponse(BaseModel):
    message: str = ""
    exception: str = ""
    timestamp: float = 0.0

async def exception_catcher(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    try:
        return await call_next(request)
    except Exception as e:
        time = datetime.now()
        logger.exception(
            "Global Exception Caught: {exception_name}\n{traceback}",
            exception_name = type(e).__name__,
            traceback = traceback.format_exc(),
        )
        return Response(
            content = ExceptionResponse(
                message = str(e),
                exception = type(e).__name__,
                timestamp = time.timestamp(),
            ),
            status_code=500,
        )