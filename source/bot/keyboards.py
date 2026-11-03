from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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
