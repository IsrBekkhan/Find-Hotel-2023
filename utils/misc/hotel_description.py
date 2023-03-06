from typing import Dict


def hotel_description_maker(hotel_info: Dict) -> str:
    """
    Функция, возвращающая строку с информацией об отеле.

    """
    if len(hotel_info['locality_description']) != 0:
        locality_description = ' '.join(['<b>Что рядом:</b>', '<i>', *hotel_info['locality_description'], '</i>'])
    else:
        locality_description = ''

    return '<b>{hotels_name}</b> - <i>{description}</i>' \
           '<b>Адрес:</b> {address}\n\n' \
           '{locality_description}'.format(hotels_name=hotel_info['name'],
                                           description=hotel_info['description'],
                                           address=hotel_info['address'],
                                           locality_description=locality_description)
