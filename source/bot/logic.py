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

    return "\n".join(lines)
