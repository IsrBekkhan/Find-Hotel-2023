from telebot.handler_backends import State, StatesGroup


class HighPriceStates(StatesGroup):
    """
    Класс HighPriceStates. Родитель: StateGroup
    Класс состояний клиента.

    """
    region = State()

