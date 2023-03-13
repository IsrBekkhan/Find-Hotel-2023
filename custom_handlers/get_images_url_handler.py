from custom_handlers.api_request_formation import api_request
from custom_handlers.request_utils.request_params import payload_for_detail_setter
from custom_handlers.request_utils.request_methods import GET_HOTEL_INFO_ENDWITH
from custom_handlers.request_utils.request_headers import post_request_headers
from custom_handlers.info_getters.images_url_getter import images_url_getter
from custom_handlers.exception_handling_decorator import exception_handling_decorator
from typing import Callable, Union, Dict
from loguru import logger


@exception_handling_decorator
def get_images_url_handler(hotel_id: str, images_amount: int) -> Union[Callable, Exception]:
    """
    Функция, которая принимает id отеля, формирует API-запрос,
    и возварщает функцию, получающую список c url-ссылками фотографий из API-ответа.

    """
    logger.info('Обработка запроса: id отеля - {}'.format(hotel_id))
    payload = payload_for_detail_setter(hotel_id=hotel_id)
    hotel_info_response: Union[Dict, Exception] = api_request(
        method_endswith=GET_HOTEL_INFO_ENDWITH,
        params=payload,
        method_type='POST',
        headers=post_request_headers
    )
    return images_url_getter(deserialized_response=hotel_info_response, images_amount=images_amount)
