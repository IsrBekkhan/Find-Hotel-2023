from custom_handlers.api_request_formation import api_request
from custom_handlers.request_utils.request_params import payload_setter
from custom_handlers.request_utils.request_methods import GET_HOTELS_LIST_ENDWITH
from custom_handlers.request_utils.request_headers import post_request_headers
from custom_handlers.info_getters.regions_from_city_getter import regions_from_city_getter
from custom_handlers.exception_handling_decorator import exception_handling_decorator
from typing import Callable, Union, Dict
from datetime import date
from loguru import logger


@exception_handling_decorator
def get_regions_from_city_handler(
        city_id: str,
        city_name: str,
        check_in: date,
        check_out: date,
        min_price: int = 1,
        max_price: int = 300,
        sort_by: str = 'PRICE_LOW_TO_HIGH'
) -> Union[Callable, Exception]:
    """
    Функция, которая формирует API-запрос,
    и возварщает функцию, получающую инфо об отелях этого города из API-ответа.

    """
    logger.info('Обработка запроса: {}'.format(city_id))
    payload = payload_setter(city_id=city_id,
                             check_in=check_in,
                             check_out=check_out,
                             min_price=min_price,
                             max_price=max_price,
                             sort_by=sort_by)
    regions_from_city_response: Union[Dict, Exception] = api_request(
        method_endswith=GET_HOTELS_LIST_ENDWITH,
        params=payload,
        method_type='POST',
        headers=post_request_headers
    )
    return regions_from_city_getter(
        deserialized_response=regions_from_city_response,
        city_name=city_name
    )

