from aiogram.fsm.state import State, StatesGroup


class PaymentState(StatesGroup):
    confirm_payment = State()  # Ожидание нажатия кнопки подтверждения


class ClearPaymentsState(StatesGroup):
    confirm_clear = State()  # Ожидание нажатия кнопки подтверждения
