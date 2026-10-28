from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Category(str, Enum):
    """
    Категории трат.
    """

    FOOD = "Еда"
    TRANSPORT = "Транспорт"
    ENTERTAINMENT = "Развлечения"
    UTILITIES = "Коммунальные услуги"
    HEALTHCARE = "Здравоохранение"
    EDUCATION = "Образование"
    SHOPPING = "Покупки"
    OTHER = "Другое"


class Trata(BaseModel):
    amount: float
    category: Category = Category.OTHER
    date: datetime = Field(default_factory=datetime.now)
    shop: str | None = None


class Answer(BaseModel):
    """
    Класс для хранения ответа на запрос.
    """

    content: list[Trata] = Field(default_factory=list)
