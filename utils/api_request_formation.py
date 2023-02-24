import requests
from requests import get, post
from requests.exceptions import RequestException
from typing import Dict, Callable, Union


def api_request(method_endswith: str, params: Dict, method_type: str, headers: Dict) -> Union[Callable, Exception]:
    """
    Функция, принимающая параметры для API-запроса, и, взависимости от значения
    method_type, возращающая одну из функций для GET или POST запроса.

    """
    url = f"https://hotels4.p.rapidapi.com/{method_endswith}"

    if method_type == 'GET':
        return get_request(
            url=url,
            params=params,
            headers=headers
        )
    else:
        return post_request(
            url=url,
            headers=headers,
            params=params
        )


def get_request(url: str, params: Dict, headers: Dict) -> Union[Dict, Exception]:
    """
    Функция для GET-запроса.

    """
    response = get(
        url,
        headers=headers,
        params=params,
        timeout=15
    )
    if response.status_code == requests.codes.ok:
        return response.json()
    raise RequestException


def post_request(url: str, headers: Dict, params: Dict) -> Union[Dict, Exception]:
    """
    Функция для POST-запроса.

    """
    response = post(
        url=url,
        headers=headers,
        json=params,
        timeout=15
    )
    if response.status_code == requests.codes.ok:
        return response.json()
    raise RequestException


