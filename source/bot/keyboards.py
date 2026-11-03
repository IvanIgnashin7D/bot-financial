from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_confirm_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Подтвердить", callback_data="confirm_payment"
                ),
                InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_payment"),
            ]
        ]
    )
