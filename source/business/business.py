import io
from datetime import datetime

from openai import AsyncOpenAI

from source.structures.structures import Answer

client = AsyncOpenAI(api_key="ВАШ_OPENAI_API_KEY")


async def text_response(text: str) -> Answer:
    today = datetime.date.today().isoformat()

    system_prompt = f"""
    Ты финансовый ассистент. Твоя задача — извлечь из текста пользователя все траты и структурировать их.
    Сегодняшняя дата: {today}.
    Если пользователь пишет "вчера" или "позавчера", вычисляй дату относительно сегодняшней.
    Если валюта не указана, считай, что это рубли.
    Если упоминается магазин или место, укажи его для каждой связанной траты.
    """

    completion = await client.beta.chat.completions.parse(
        model="gpt-4o-mini",
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
