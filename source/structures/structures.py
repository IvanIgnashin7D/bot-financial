from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Category(str, Enum):
    FOOD = "Еда"
    TRANSPORT = "Транспорт"
    ENTERTAINMENT = "Развлечения"
    UTILITIES = "Коммунальные услуги"
    HEALTHCARE = "Здравоохранение"
    EDUCATION = "Образование"
    SHOPPING = "Покупки"
    OTHER = "Другое"


class Trata(BaseModel):
    name: str = Field(description="Название траты")
    amount: float = Field(description="Сумма траты в рублях")
    category: Category = Field(default=Category.OTHER, description="Категория траты")
    date: datetime = Field(
        default_factory=datetime.now,
        description="Дата и время траты в формате YYYY-MM-DD HH:MM",
    )
    shop: str | None = Field(default=None, description="Название магазина")


class Answer(BaseModel):
    content: list[Trata] = Field(default_factory=list, description="Список трат")
