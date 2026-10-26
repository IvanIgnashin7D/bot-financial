from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Это эхо-бот. Напиши мне что-нибудь, и я отвечу тем же.")


@router.message()
async def echo_handler(message: Message):
    await message.send_copy(chat_id=message.chat.id)
