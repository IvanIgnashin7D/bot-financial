import io

from source.structures.structures import Answer


async def text_response(text: str) -> Answer:
    """
    Формирует трату из текста
    """
    answer = Answer()
    return answer


async def voice_response(audio_buffer: io.BytesIO) -> Answer:
    """
    Формирует трату из голосового сообщения.
    """
    answer = Answer()
    return answer


async def photo_response(photo_buffer: io.BytesIO) -> Answer:
    """
    Формирует трату из фотографии.
    """
    answer = Answer()
    return answer
