from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_confirm_kb(callback_data1=str, callback_data2=str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Подтвердить", callback_data=callback_data1
                ),
                InlineKeyboardButton(text="❌ Отмена", callback_data=callback_data2),
            ]
        ]
    )


class PaymentsPaginationCallback(CallbackData, prefix="pay_page"):
    page: int


def get_pagination_kb(page: int, total_pages: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if page > 1:
        builder.button(
            text="⬅️ Назад",
            callback_data=PaymentsPaginationCallback(page=page - 1),
        )

    builder.button(text=f"{page}/{total_pages}", callback_data="noop")

    if page < total_pages:
        builder.button(
            text="Вперёд ➡️",
            callback_data=PaymentsPaginationCallback(page=page + 1),
        )

    builder.adjust(3)
    return builder.as_markup()


def get_stats_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Все траты за день", callback_data="stats_day")
    builder.button(text="Все траты за неделю", callback_data="stats_week")
    builder.button(text="Все траты за месяц", callback_data="stats_month")
    builder.button(text="Общая статистика трат", callback_data="stats_all")
    builder.adjust(1)
    return builder.as_markup()
