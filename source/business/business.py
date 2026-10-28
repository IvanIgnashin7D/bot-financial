import base64
import io
from datetime import datetime
from os import getenv

from dotenv import load_dotenv
from faster_whisper import WhisperModel
from openai import AsyncOpenAI
from structures.structures import Answer

load_dotenv()
MODEL_API_KEY = getenv("MODEL_API_KEY")
client = AsyncOpenAI(
    api_key=MODEL_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

whisper_model = WhisperModel("base", device="cpu", compute_type="int8")


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
    recognized_text = transcribe_voice(audio_buffer)
    if not recognized_text:
        return Answer()
    return await text_response(recognized_text)


async def photo_response(photo_buffer: io.BytesIO) -> Answer:
    today = datetime.now().isoformat()
    photo_buffer.seek(0)
    base64_image = base64.b64encode(photo_buffer.getvalue()).decode("utf-8")

    system_prompt = f"""
    Ты финансовый ассистент. Твоя задача — изучить чек или фото покупки, найти все позиции трат и структурировать их.
    Сегодняшняя дата: {today}.
    Если на чеке видна конкретная дата покупки, используй её вместо сегодняшней.
    Если на чеке указано название магазина или юрлица, заполни поле shop.
    Если валюта не указана, считай, что это рубли.
    """

    completion = await client.beta.chat.completions.parse(
        model="gemini-3.5-flash-lite",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Распознай все купленные товары, суммы и магазин на этом чеке.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            },
        ],
        response_format=Answer,
        temperature=0.1,
    )

    return completion.choices[0].message.parsed


def transcribe_voice(audio_buffer: io.BytesIO) -> str:
    audio_buffer.seek(0)
    segments, _ = whisper_model.transcribe(audio_buffer, language="ru")
    return " ".join(segment.text for segment in segments).strip()
