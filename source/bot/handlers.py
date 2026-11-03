import io

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart, ExceptionTypeFilter
from aiogram.types import ErrorEvent, Message
from bot import logic
from business.business import photo_response, text_response, voice_response
from db.business import create_new_user
from google.genai.errors import ServerError
from texts import abc

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    created_user = await create_new_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
    )

    await message.answer(abc.start_message, parse_mode="HTML")
    if created_user:
        await message.answer(
            "✅ Вы успешно зарегистрированы! Теперь вы можете использовать бота."
        )
    await message.answer(
        "ℹ️ Чтобы получить помощь, используйте команду /help.", parse_mode="HTML"
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(abc.help_message, parse_mode="HTML")


@router.message(F.text)
async def text_handler(message: Message):
    answer = await text_response(message.text)
    answer_text = logic.answer_to_text(answer)
    await message.answer(text=answer_text, parse_mode="HTML")


@router.message(F.voice)
async def voice_handler(message: Message, bot: Bot):
    file_buffer = io.BytesIO()
    await bot.download(message.voice, file_buffer)

    answer = await voice_response(file_buffer)
    answer_text = logic.answer_to_text(answer)
    await message.answer(text=answer_text, parse_mode="HTML")


@router.message(F.photo)
async def photo_handler(message: Message, bot: Bot):
    file_buffer = io.BytesIO()
    await bot.download(message.photo[-1], file_buffer)

    answer = await photo_response(file_buffer)
    answer_text = logic.answer_to_text(answer)
    await message.answer(text=answer_text, parse_mode="HTML")


@router.error(ExceptionTypeFilter(ServerError))
async def handle_gemini_server_error(event: ErrorEvent, retries=3):
    if event.update.message:
        for _ in range(retries):
            await event.update.message.answer(
                "⚠️ Нейросеть сейчас перегружена запросами. Повторная попытка..."
            )
