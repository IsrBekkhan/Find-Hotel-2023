from utils.api_request_formation import api_request
from utils.misc.request_params import payload_setter
from utils.misc.request_methods import GET_HOTELS_LIST_ENDWITH
from utils.misc.request_headers import post_request_headers
from utils.regions_from_city_getter import regions_from_city_getter
from handlers.exception_handling_decorator import exception_handling_decorator
from typing import Callable, Union
from datetime import date


@exception_handling_decorator
def get_regions_from_city_handler(city_id: str, city_name: str, check_in: date, check_out: date
                                  ) -> Union[Callable, Exception]:
    """
    Функция, которая формирует API-запрос,
    и возварщает функцию, получающую инфо об отелях этого города из API-ответа.

    """
    payload = payload_setter(city_id=city_id, check_in=check_in, check_out=check_out)
    regions_from_city_response = api_request(
        method_endswith=GET_HOTELS_LIST_ENDWITH,
        params=payload,
        method_type='POST',
        headers=post_request_headers
    )
    return regions_from_city_getter(
        deserialized_response=regions_from_city_response,
        city_name=city_name
    )

