import io
from datetime import datetime
from os import getenv

from dotenv import load_dotenv
from openai import AsyncOpenAI
from structures.structures import Answer

load_dotenv()
MODEL_API_KEY = getenv("MODEL_API_KEY")
client = AsyncOpenAI(
    api_key=MODEL_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


async def text_response(text: str) -> Answer:
    today = datetime.now().isoformat()

    system_prompt = f"""
    Ты финансовый ассистент. Твоя задача — извлечь из текста пользователя все траты и структурировать их.
    Сегодняшняя дата: {today}.
    Если пользователь пишет "вчера" или "позавчера", вычисляй дату относительно сегодняшней.
    Если валюта не указана, считай, что это рубли.
    Если упоминается магазин или место, укажи его для каждой связанной траты.
    """

    completion = await client.beta.chat.completions.parse(
        model="gemini-3.5-flash-lite",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        response_format=Answer,
        temperature=0.1,
    )

    return completion.choices[0].message.parsed


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
