from time import sleep
from typing import Callable

from django.conf import settings


def retry(tries=-1, delay=0, delay_step=0, max_delay=None):  # noqa
    def func_wrapper(f: Callable):  # noqa
        async def wrapper(*args: list, **kwargs: dict):  # noqa
            if settings.DEBUG:
                return await f(*args, **kwargs)

            _tries, _delay = tries, delay
            while _tries:
                try:
                    return await f(*args, **kwargs)
                except Exception:
                    sleep(_delay)

                _tries -= 1
                _delay += delay_step

                if max_delay is not None:
                    _delay = min(_delay, max_delay)

        return wrapper

    return func_wrapper
