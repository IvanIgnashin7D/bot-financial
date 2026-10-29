import io

from aiogram import Bot, ExceptionTypeFilter, F, Router
from aiogram.filters import CommandStart
from aiogram.types import ErrorEvent, Message
from bot import logic
from business import business
from google.genai.errors import ServerError
from texts import abc

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(abc.start_message, parse_mode="HTML")


@router.message(F.text)
async def text_handler(message: Message):
    answer = await business.text_response(message.text)
    answer_text = logic.answer_to_text(answer)
    await message.answer(text=answer_text, parse_mode="HTML")


@router.message(F.voice)
async def voice_handler(message: Message, bot: Bot):
    file_buffer = io.BytesIO()
    await bot.download(message.voice, file_buffer)

    answer = await business.voice_response(file_buffer)
    answer_text = logic.answer_to_text(answer)
    await message.answer(text=answer_text, parse_mode="HTML")


@router.message(F.photo)
async def photo_handler(message: Message, bot: Bot):
    file_buffer = io.BytesIO()
    await bot.download(message.photo[-1], file_buffer)

    answer = await business.photo_response(file_buffer)
    answer_text = logic.answer_to_text(answer)
    await message.answer(text=answer_text, parse_mode="HTML")


@router.error(ExceptionTypeFilter(ServerError))
async def handle_gemini_server_error(event: ErrorEvent, retries=3):
    if event.update.message:
        for _ in range(retries):
            await event.update.message.answer(
                "⚠️ Нейросеть сейчас перегружена запросами. Повторная попытка..."
            )


# ⚠️ Нейросеть сейчас перегружена запросами. Повторите отправку через минуту.
