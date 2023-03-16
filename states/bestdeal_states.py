from telebot.handler_backends import State, StatesGroup


class BestDealStates(StatesGroup):
    """
    Класс BestDealStates. Родитель: StateGroup
    Класс состояний клиента.

    """
    min_price = State()
    max_price = State()
    region = State()
    hotels_amount = State()

