from source.structures.structures import Answer


def answer_to_text(answer: Answer) -> str:
    """
    Преобразует объект Answer в текстовое сообщение.
    """
    if not answer.content:
        return "Нет данных для отображения."

    lines = []
    for trata in answer.content:
        line = f"Сумма: {trata.amount}, Категория: {trata.category}, Дата: {trata.date.strftime('%Y-%m-%d %H:%M:%S')}"
        if trata.shop:
            line += f", Магазин: {trata.shop}"
        lines.append(line)

    return "\n".join(lines)
