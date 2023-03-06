from datetime import date


def date_reverser(date_object: date) -> str:
    """
    Функция, которая принимает объект даты, меняет местами день и год и возвращает строку с датой

    """
    reversed_date_list = reversed(str(date_object).split('-'))
    return '-'.join(reversed_date_list)
