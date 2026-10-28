from aiogram import F, Router
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


@router.message(F.audio)
async def audio_handler(message: Message):
    await business.audio_response(message.audio.file_id)
    await message.send_copy(chat_id=message.chat.id)


@router.message(F.photo)
async def photo_handler(message: Message):
    await business.photo_response(message.photo[-1].file_id)
    await message.send_copy(chat_id=message.chat.id)
