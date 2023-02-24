from utils.api_request_formation import api_request
from utils.misc.request_params import querystring_setter
from utils.misc.request_methods import GET_CITYID_ENDWITH
from utils.misc.request_headers import get_request_headers
from utils.city_info_getter import city_info_getter
from handlers.exception_handling_decorator import exception_handling_decorator
from typing import Callable, Union


@exception_handling_decorator
def get_city_info_handler(city_name: str) -> Union[Callable, Exception]:
    """
    Функция, которая принимает название города, формирует API-запрос,
    и возварщает функцию, получающую инфо о городе из API-ответа.

    """
    querystring = querystring_setter(city=city_name)
    response_with_city_id = api_request(
        method_endswith=GET_CITYID_ENDWITH,
        params=querystring, method_type='GET',
        headers=get_request_headers
    )
    return city_info_getter(response_with_city_id, city_name)

