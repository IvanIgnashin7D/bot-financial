import io

from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from business import business
from texts import abc

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(abc.start_message, parse_mode="HTML")


@router.message(F.text)
async def text_handler(message: Message):
    await business.text_response(message.text)
    await message.send_copy(chat_id=message.chat.id)


@router.message(F.voice)
async def voice_handler(message: Message, bot: Bot):
    file_buffer = io.BytesIO()
    await bot.download(message.voice, file_buffer)
    file_buffer.seek(0)

    answer = await business.voice_response(file_buffer)
    answer_text = await business.answer_to_text(answer)
    await message.answer(chat_id=message.chat.id, text=answer_text)


@router.message(F.photo)
async def photo_handler(message: Message, bot: Bot):
    file_buffer = io.BytesIO()
    await bot.download(message.photo[-1], file_buffer)
    file_buffer.seek(0)

    answer = await business.photo_response(file_buffer)
    answer_text = await business.answer_to_text(answer)
    await message.answer(chat_id=message.chat.id, text=answer_text)
