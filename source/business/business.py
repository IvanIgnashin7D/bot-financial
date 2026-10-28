async def text_response(text: str) -> str:
    """
    Формирует текстовый ответ для пользователя.
    """
    return text


async def audio_response(audio_path: str) -> str:
    """
    Формирует аудио ответ для пользователя.
    """
    return audio_path


async def photo_response(photo_path: str) -> str:
    """
    Формирует фото ответ для пользователя.
    """
    return photo_path
