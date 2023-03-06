from typing import Dict, Union


def city_info_getter(deserialized_response: Dict[str, Dict], city: str) -> Union[Dict, Exception]:
    """
    Функция, возвращающая словарь с информацией о городе или исключение.

    """
    search_results = deserialized_response.get('sr', None)

    if len(search_results) == 0:
        raise KeyError

    if search_results:
        for item in search_results:

            if item['type'] == 'CITY':
                short_name = item['regionNames']['shortName']

                if short_name.lower() == city.lower():
                    return {
                        'id': item['gaiaId'],
                        'state': item['regionNames']['secondaryDisplayName'],
                        'city': item['regionNames']['primaryDisplayName']
                    }
    raise KeyError
