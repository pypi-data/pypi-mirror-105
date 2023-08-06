from itertools import count
from time import monotonic
from typing import Awaitable, Callable, Union

from hypothesis.strategies import (  # type: ignore
    composite,
    dictionaries,
    floats,
    integers,
    lists,
    none,
    sampled_from,
    sets,
    text,
    tuples,
)
from typing_extensions import Type

elements = integers() | floats() | text() | none()
anything = (
    elements
    | lists(elements)
    | tuples(elements)
    | dictionaries(elements, elements)
    | sets(elements)
)
builtin_exceptions = list(
    exc for exc in Exception.__subclasses__() if exc.__module__ == "builtins"
)


def get_func_with_fuse(fuse: float) -> Callable[[], bool]:
    now = monotonic()

    def tester():
        return monotonic() - now >= fuse

    return tester


def get_awaitable_with_fuse(fuse: float) -> Callable[[], Awaitable[bool]]:
    now = monotonic()

    async def tester():
        return monotonic() - now >= fuse

    return tester


def get_exception_raiser(
    countdown: int, exception: Type[Exception], flavor: str = "raise_last", async_=False
) -> Union[Callable[[], bool], Awaitable[bool]]:
    assert flavor in {"raise_first", "raise_last"}

    counter = count(countdown, -1)

    def exception_raiser_sync():
        if (next(counter) > 0) ^ (flavor == "raise_first"):
            return False
        else:
            raise exception

    async def exception_raiser_async():
        return exception_raiser_sync()

    return exception_raiser_async if async_ else exception_raiser_sync


@composite
def func_and_parameters(
    draw,
    func=sampled_from(
        [
            lambda: False,
            lambda a: a < 0,
            lambda a, b: a + b < 0,
            lambda a, b, c: a + b + c < 0,
        ]
    ),
):
    f = draw(func)
    args = []
    for _ in range(4):
        try:
            f(*args)
        except TypeError:
            args.append(draw(integers(min_value=-10, max_value=10)))
        else:
            return f, args
    raise ValueError("custom strategy is broken")


class MutableBoolean:
    def __init__(self, countdown: int) -> None:
        self.counter = count(countdown, -1)

    def __bool__(self) -> bool:
        return next(self.counter) == 0
