import io
from datetime import datetime, timedelta

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart, ExceptionTypeFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ErrorEvent, Message
from bot.keyboards import (
    PaymentsPaginationCallback,
    get_confirm_kb,
    get_pagination_kb,
    get_stats_kb,
)
from bot.logic import answer_to_text, payments_to_text
from bot.states import ClearPaymentsState, PaymentState
from business.business import (
    photo_response,
    text_response,
    voice_response,
)
from db.business import (
    create_new_user,
    delete_all_payments,
    delete_last_payment,
    get_payments_by_period,
    save_payments,
)
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


@router.message(Command("stats"))
async def stats_handler(message: Message):
    await message.answer(
        "ℹ️ Функция статистики пока в разработке. Пожалуйста, подождите.",
        reply_markup=get_stats_kb(),
    )


@router.callback_query(F.data == "stats_day")
async def stats_day_handler(callback: CallbackQuery):
    end_date = datetime.now()
    start_date = end_date - timedelta(hours=24)

    payments, total_pages = await get_payments_by_period(
        tg_id=callback.from_user.id, start_date=start_date, end_date=end_date
    )

    text = payments_to_text(payments)

    await callback.message.edit_text(
        text,
        reply_markup=get_pagination_kb(page=1, total_pages=total_pages),
        parse_mode="HTML",
    )
    # todo
    await callback.answer()


@router.callback_query(F.data == "stats_week")
async def stats_week_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "ℹ️ Статистика за неделю пока в разработке. Пожалуйста, подождите.",
        reply_markup=get_pagination_kb(page=1, total_pages=1),
    )
    # todo

    await callback.answer()


@router.callback_query(F.data == "stats_month")
async def stats_month_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "ℹ️ Статистика за месяц пока в разработке. Пожалуйста, подождите.",
        reply_markup=get_pagination_kb(page=1, total_pages=1),
    )
    # todo
    await callback.answer()


@router.callback_query(F.data == "stats_all")
async def stats_all_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "ℹ️ Общая статистика трат пока в разработке. Пожалуйста, подождите.",
        reply_markup=get_pagination_kb(page=1, total_pages=1),
    )
    # todo:
    await callback.answer()


@router.callback_query(PaymentsPaginationCallback.filter())
def pagination_handler(
    callback: CallbackQuery, callback_data: PaymentsPaginationCallback
):
    pass


# todo


@router.message(Command("delete_last_payment"))
async def delete_last_payment_handler(message: Message):
    deleted = await delete_last_payment(tg_id=message.from_user.id)
    if deleted:
        await message.answer("✅ Последняя трата успешно удалена.")
    else:
        await message.answer("❌ Не удалось удалить последнюю трату.")


@router.message(Command("clear"))
async def clear_payments_handler(message: Message, state: FSMContext):
    await message.answer(
        "Данная функция удалит <b>ВСЕ</b> ваши траты. Вы уверены?",
        reply_markup=get_confirm_kb(
            callback_data1="confirm_clear", callback_data2="cancel_clear"
        ),
        parse_mode="HTML",
    )
    await state.set_state(ClearPaymentsState.confirm_clear)


@router.callback_query(ClearPaymentsState.confirm_clear, F.data == "confirm_clear")
async def confirm_clear_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    deleted = await delete_all_payments(tg_id=callback.from_user.id)
    if deleted:
        await callback.message.edit_text("✅ Все траты успешно удалены.")
    else:
        await callback.message.edit_text("❌ Не удалось удалить траты.")
    await callback.answer()


@router.callback_query(ClearPaymentsState.confirm_clear, F.data == "cancel_clear")
async def cancel_clear_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Очистка трат отменена.")
    await callback.answer()


@router.error(ExceptionTypeFilter(ServerError))
async def handle_gemini_server_error(event: ErrorEvent):
    if event.update.message:
        await event.update.message.answer(
            "⚠️ Нейросеть сейчас перегружена запросами. Повторная попытка..."
        )


@router.message(F.text)
async def text_handler(message: Message, state: FSMContext):
    current_message = await message.answer("⏳ Обрабатываю ваш запрос...")

    answer = await text_response(message.text)
    answer_text = answer_to_text(answer)

    await state.set_data({"payments": answer, "answer_text": answer_text})
    await state.set_state(PaymentState.confirm_payment)

    text_preview = f"📝 <b>Проверьте данные:</b>\n\n{answer_text}"
    await current_message.edit_text(
        text_preview,
        reply_markup=get_confirm_kb(
            callback_data1="confirm_payment", callback_data2="cancel_payment"
        ),
        parse_mode="HTML",
    )


@router.callback_query(PaymentState.confirm_payment, F.data == "confirm_payment")
async def confirm_payment_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    answer = data.get("payments")
    answer_text = data.get("answer_text")

    if not answer:
        await callback.message.edit_text(
            "⚠️ Данные устарели. Отправьте сообщение заново."
        )
        await state.clear()
        return

    result = await save_payments(answer=answer, tg_id=callback.from_user.id)

    if result:
        await callback.message.edit_text(
            f"✅ Расход успешно записан в базу данных!\n\n{answer_text}",
            parse_mode="HTML",
        )
    else:
        await callback.message.edit_text(
            "❌ Произошла ошибка при сохранении данных. Пожалуйста, попробуйте снова."
        )

    await state.clear()
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
    answer_text = answer_to_text(answer)
    await message.answer(text=answer_text, parse_mode="HTML")


@router.message(F.photo)
async def photo_handler(message: Message, bot: Bot):
    file_buffer = io.BytesIO()
    await bot.download(message.photo[-1], file_buffer)

    answer = await photo_response(file_buffer)
    answer_text = answer_to_text(answer)
    await message.answer(text=answer_text, parse_mode="HTML")
