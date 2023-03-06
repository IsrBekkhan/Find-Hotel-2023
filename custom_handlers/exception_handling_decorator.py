from functools import wraps
from requests.exceptions import RequestException
from typing import Callable


def exception_handling_decorator(func: Callable) -> Callable:
    """
    Декоратор, обрабатывающий исключения декорируемой функции.

    """
    @wraps(func)
    def wrapped_func(**kwargs):

        try:
            return func(**kwargs)
        except RequestException:
            return 'Упс! Ошибка сервиса: что-то пошло не так.\nПопробуйте ещё раз или повторите попытку позже.'
        except KeyError:
            return 'По такому городу ничего не найдено.\nУточните правильное название города и повторите попытку'
        except NameError:
            return 'Упс! Ошибка сервиса:\nсервис не может работать с данным городом.\nПриносим свои извинения!(('
        except Exception:
            return 'Неопознанная ошибка\nПовторите попытку позже'

    return wrapped_func
