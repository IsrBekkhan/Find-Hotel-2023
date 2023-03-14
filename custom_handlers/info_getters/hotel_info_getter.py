from typing import Dict, Union
from loguru import logger


def hotel_info_getter(deserialized_response: Dict[str, Dict]) -> Union[Dict, Exception]:
    """
    Функция, возвращающая словарь с информацией об отеле или исключение.

    """
    logger.info('Получение подробной информации об отеле')
    try:
        summary = deserialized_response['data']['propertyInfo']['summary']
        return {
            'name': summary['name'],
            'description': summary['tagline'],
            'locality_description': summary['location']['whatsAround']['editorial']['content'],
            'address': summary['location']['address']['addressLine'],
            'map_image': summary['location']['staticImage']['url'],
            'latitude': summary['location']['coordinates']['latitude'],
            'longitude': summary['location']['coordinates']['longitude']
        }
    except KeyError:
        raise NameError
