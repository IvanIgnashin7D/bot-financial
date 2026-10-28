from structures.structures import Answer


def answer_to_text(answer: Answer) -> str:
    """
    Преобразует объект Answer в текстовое сообщение.
    """
    if not answer.content:
        return "Нет данных для отображения."

    lines = []
    for trata in answer.content:
        line = f"<b>{trata.name}</b>: {trata.amount} руб, <i>{trata.category.value}</i>, {trata.date.strftime('%d.%m.%Y')}"
        if trata.shop:
            line += f" ({trata.shop})"
        lines.append(line)

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
