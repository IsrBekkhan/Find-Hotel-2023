from random import sample
from typing import Union, List, Dict, Tuple
from loguru import logger


def images_url_getter(deserialized_response: Dict[str, Dict], images_amount: int) -> Union[List[Tuple], Exception]:
    """
    Функция, возвращающая список кортежей с url-адресами и описанием фотографий соответственно, или, исключение.

    """
    logger.info('Получение списка url-адресов фотографий отеля')
    try:
        images_category = deserialized_response['data']['propertyInfo']['propertyGallery']['images']

        if len(images_category) < images_amount:
            images_amount = len(images_category)

        random_selected_images = sample(images_category, images_amount)
        return [(image_dict["image"]["url"], image_dict["image"]['description'])
                for image_dict in random_selected_images]

    except KeyError:
        raise NameError
