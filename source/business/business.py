import io
from datetime import datetime
from os import getenv

from business.decorators import retry_on_server_error
from dotenv import load_dotenv
from google import genai
from google.genai import types
from structures.structures import Answer

load_dotenv()

MODEL_API_KEY = getenv("MODEL_API_KEY")
MODEL = "gemini-3.5-flash"
APPLICATION_JSON = "application/json"

client = genai.Client(api_key=MODEL_API_KEY)


def get_system_prompt() -> str:
    today = datetime.now().isoformat()
    return f"""
    Ты финансовый ассистент. Твоя задача — извлечь все траты, суммы и магазины,
    а затем разложить их строго по заданной схеме.
    Сегодняшняя дата: {today}.
    Если пользователь пишет или говорит "вчера", "позавчера", вычисляй дату относительно сегодняшней.
    Если валюта не указана, считай, что это рубли.
    """


@retry_on_server_error()
async def text_response(text: str) -> Answer:
    response = await client.aio.models.generate_content(
        model=MODEL,
        contents=text,
        config=types.GenerateContentConfig(
            system_instruction=get_system_prompt(),
            response_mime_type=APPLICATION_JSON,
            response_schema=Answer,
            temperature=0.1,
        ),
    )
    return response.parsed


@retry_on_server_error()
async def voice_response(audio_buffer: io.BytesIO) -> Answer:
    audio_buffer.seek(0)
    audio_bytes = audio_buffer.getvalue()
    audio_part = types.Part.from_bytes(
        data=audio_bytes,
        mime_type="audio/ogg",
    )

    response = await client.aio.models.generate_content(
        model=MODEL,
        contents=audio_part,
        config=types.GenerateContentConfig(
            system_instruction=get_system_prompt(),
            response_mime_type=APPLICATION_JSON,
            response_schema=Answer,
            temperature=0.1,
        ),
    )
    return response.parsed


@retry_on_server_error()
async def photo_response(photo_buffer: io.BytesIO) -> Answer:
    photo_buffer.seek(0)
    photo_bytes = photo_buffer.getvalue()

    image_part = types.Part.from_bytes(
        data=photo_bytes,
        mime_type="image/jpeg",
    )

    response = await client.aio.models.generate_content(
        model=MODEL,
        contents=image_part,
        config=types.GenerateContentConfig(
            system_instruction=get_system_prompt(),
            response_mime_type=APPLICATION_JSON,
            response_schema=Answer,
            temperature=0.1,
        ),
    )
    return response.parsed
