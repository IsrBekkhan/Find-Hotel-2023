from random import sample
from typing import Union, List, Dict


def images_url_getter(deserialized_response: Dict[str, Dict], images_amount: int) -> Union[List[str], Exception]:
    """
    Функция, возвращающая список с url-адресами фотографий отеля или исключение.

    """
    try:
        images_category = deserialized_response['data']['propertyInfo']['propertyGallery']['images']

        if len(images_category) < images_amount:
            images_amount = len(images_category)

        random_selected_images = sample(images_category, images_amount)
        return [image_dict["image"]["url"] for image_dict in random_selected_images]

    except KeyError:
        raise NameError
