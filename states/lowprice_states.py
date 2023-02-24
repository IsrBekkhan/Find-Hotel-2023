from telebot.handler_backends import State, StatesGroup


class LowPriceStates(StatesGroup):
    """
    Класс LowPriceStates. Родитель: StateGroup
    Класс состояний клиента.

    """
    start = State()
    city = State()
    check_in_date = State()
    check_out_date = State()
    region = State()
    hotels_amount = State()
    is_image = State()
    images_amount = State()
    hotel = State()

