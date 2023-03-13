from typing import Dict, Union
from loguru import logger


def regions_from_city_getter(deserialized_response: Dict[str, Dict], city_name: str) -> Union[Dict, Exception]:
    """
    Функция, возвращающая словарь с информацией о всех найденных отелях города или исключение.

    """
    logger.info('Получение информации о районах города {}'.format(city_name))
    regions_from_city_dict = dict()
    try:
        hotels_search_result = deserialized_response['data']['propertySearch']['properties']

        for hotels_properties in hotels_search_result:
            hotels_name = hotels_properties['name']
            hotels_id = hotels_properties['id']
            hotels_price = hotels_properties['price']['lead']['amount']
            currency_symbol = hotels_properties['price']['lead']['currencyInfo']['symbol']
            distance_from_center_value = hotels_properties['destinationInfo']['distanceFromDestination']['value']
            distance_from_center_unit = hotels_properties['destinationInfo']['distanceFromDestination']['unit']
            try:
                hotels_neighborhood = hotels_properties['neighborhood']['name']
            except TypeError:
                hotels_neighborhood = '{} (район не указан)'.format(city_name)

            curr_hotels_properties = {
                'name': hotels_name,
                'id': hotels_id,
                'price': hotels_price,
                'currency': currency_symbol,
                'distance': distance_from_center_value,
                'distance_unit': distance_from_center_unit
            }

            if hotels_neighborhood in regions_from_city_dict:
                regions_from_city_dict[hotels_neighborhood].append(curr_hotels_properties)
            else:
                regions_from_city_dict[hotels_neighborhood] = [curr_hotels_properties]

    except KeyError:
        raise NameError

    return regions_from_city_dict
