from db.models import Payment
from structures.structures import Answer


def answer_to_text(answer: Answer) -> str:
    """
    Преобразует объект Answer в текстовое сообщение.
    """
    if not answer.content:
        return "Нет данных для отображения."

    lines = []
    shop = None
    for trata in answer.content:
        line = ""

        if trata.shop != shop:
            shop = trata.shop
            line += f"\n🧾 <b>Чек из магазина «{shop if shop else 'Не указан'}»</b>\n"

        line += (
            f"🛒 <b>{trata.name}</b>\n"
            f"├ Цена: {trata.amount} ₽\n"
            f"├ Категория: {trata.category.value}\n"
            f"└ Дата: {trata.date.strftime('%d.%m.%Y')}\n"
        )
        lines.append(line)

    return "\n".join(lines)


def payments_to_text(payments: list[Payment]) -> str:
    """
    Преобразует список объектов Payment в текстовое сообщение.
    """
    if not payments:
        return "Нет данных для отображения."

    lines = []
    shop = None
    for payment in payments:
        line = ""

        if payment.shop != shop:
            shop = payment.shop
            line += f"\n🧾 <b>Чек из магазина «{shop if shop else 'Не указан'}»</b>\n"

        line += (
            f"🛒 <b>{payment.name}</b>\n"
            f"├ Цена: {payment.amount} ₽\n"
            f"├ Категория: {payment.category.value}\n"
            f"└ Дата: {payment.date.strftime('%d.%m.%Y')}\n"
        )
        lines.append(line)

    return "\n".join(lines)
