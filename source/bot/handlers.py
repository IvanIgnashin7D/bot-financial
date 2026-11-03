import io

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart, ExceptionTypeFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ErrorEvent, Message
from bot import logic
from bot.keyboards import get_confirm_kb
from bot.states import PaymentState
from business.business import photo_response, text_response, voice_response
from db.business import create_new_user, delete_last_payment, save_payments
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
async def text_handler(message: Message, state: FSMContext):
    current_message = await message.answer("⏳ Обрабатываю ваш запрос...")

    answer = await text_response(message.text)
    answer_text = logic.answer_to_text(answer)

    await state.set_data({"payments": answer.model_dump(), "answer_text": answer_text})
    await state.set_state(PaymentState.confirm_payment)

    text_preview = f"📝 <b>Проверьте данные:</b>\n\n{answer_text}"
    await current_message.edit_text(
        text_preview, reply_markup=get_confirm_kb(), parse_mode="HTML"
    )


@router.callback_query(PaymentState.confirm_payment, F.data == "confirm_payment")
async def confirm_payment_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    payments = data.get("payments")
    answer_text = data.get("answer_text")

    if not payments:
        await callback.message.edit_text(
            "⚠️ Данные устарели. Отправьте сообщение заново."
        )
        await state.clear()
        return

    await save_payments([payments])

    await state.clear()

    await callback.message.edit_text(
        f"✅ Расход успешно записан в базу данных!\n\n{answer_text}", parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(PaymentState.confirm_payment, F.data == "cancel_payment")
async def cancel_payment_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Запись отменена.")
    await callback.answer()


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


@router.message(Command("delete_last_payment"))
async def delete_last_payment_handler(message: Message):
    deleted = await delete_last_payment(telegram_id=message.from_user.id)
    if deleted:
        await message.answer("✅ Последняя трата успешно удалена.")
    else:
        await message.answer("❌ Не удалось удалить последнюю трату.")


@router.error(ExceptionTypeFilter(ServerError))
async def handle_gemini_server_error(event: ErrorEvent, retries=3):
    if event.update.message:
        for _ in range(retries):
            await event.update.message.answer(
                "⚠️ Нейросеть сейчас перегружена запросами. Повторная попытка..."
            )
