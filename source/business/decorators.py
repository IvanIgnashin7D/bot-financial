import asyncio
import logging
from functools import wraps

from google.genai.errors import ServerError


def retry_on_server_error(retries: int = 3, delay: float = 2.0):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return await func(*args, **kwargs)
                except ServerError:
                    if attempt == retries:
                        raise
                    logging.warning(  # noqa: LOG015
                        f"Ошибка 503 в {func.__name__}. Попытка {attempt}/{retries}. Ждём {delay} сек..."
                    )
                    await asyncio.sleep(delay * attempt)

        return wrapper

    return decorator
