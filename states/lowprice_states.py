from telebot.handler_backends import State, StatesGroup


class LowPriceStates(StatesGroup):
    """
    Класс LowPriceStates. Родитель: StateGroup
    Класс состояний клиента.

    """
    region = State()

