import asyncio
import logging
import time
from asyncio import iscoroutinefunction
from functools import partial, wraps
from inspect import isawaitable, isclass
from time import monotonic
from typing import (
    Any,
    Awaitable,
    Callable,
    Generator,
    Iterable,
    Optional,
    Tuple,
    Type,
    Union,
)

LOGGER = logging.getLogger("assertion")
TExc = Type[Exception]
TExcTuple = Tuple[TExc, ...]
TExcIter = Iterable[TExc]


def as_tuple(v: Union[TExcIter, TExc]) -> TExcTuple:
    if isinstance(v, tuple):
        return v
    elif isinstance(v, Iterable):
        return tuple(v)
    elif isclass(v) and issubclass(v, Exception):
        return (v,)
    else:
        raise ValueError("expected an Exception subclass or a list/tuple of those")


# coro partials: https://stackoverflow.com/a/52422903/20954
def is_coro_or_partial(obj: Callable) -> bool:
    # fix partial() for Python 3.7
    while isinstance(obj, partial):
        obj = obj.func  # pragma: no cover
    return iscoroutinefunction(obj)


class DummyAwaitable:
    def __await__(self) -> Generator:
        yield


dummy_awaitable = DummyAwaitable()


def test_wrapper(func: Callable) -> Union[Callable, Awaitable]:
    async def async_tester(
        self: "Assertion",  # type: ignore # noqa: F821
        test: Callable,
        tests: Tuple,
        msg: Optional[str],
        raised_exc: TExc,
        timeout: float,
        exc_pass: TExcTuple,
        exc_ignore: TExcTuple,
    ) -> None:
        # we are going to modify test_list, so make it a list
        test_list = list(tests)
        time_start = monotonic()
        delay = self.delay_init
        exc_ignore += (raised_exc,)
        while True:
            try:
                # replace all awaitables (can only be awaited once) with their result
                awaitable_results = await asyncio.gather(
                    *filter(isawaitable, test_list)
                )
                for i, a in enumerate(test_list):
                    if isawaitable(a):
                        test_list[i] = awaitable_results.pop()

                awaitable_results = await asyncio.gather(
                    *[a() for a in test_list if is_coro_or_partial(a)]
                )
                evaluated = []
                for a in test_list:
                    if iscoroutinefunction(a):
                        evaluated.append(awaitable_results.pop())
                    elif callable(a):
                        evaluated.append(a())
                    else:
                        evaluated.append(a)

                test(
                    self,
                    *evaluated,
                    msg=msg,
                    raised_exc=raised_exc,
                )
                break
            except exc_pass:
                break
            except exc_ignore as e:
                exc = e

            time_diff = monotonic() - time_start
            if time_diff >= timeout:
                if isinstance(exc, raised_exc):
                    raise exc
                else:
                    raise raised_exc
            else:
                await asyncio.sleep(min(delay, timeout - time_diff + 0.01))
                delay = self._get_next_delay(delay)

        if timeout > 0 and self.timeout_fraction_warning is not None:
            time_diff = monotonic() - time_start
            timeout_fraction = time_diff / timeout
            if timeout > 0 and timeout_fraction > self.timeout_fraction_warning:
                LOGGER.warning(
                    "more than %.0f%% (%.1fs) of timeout (%.1fs) "
                    "passed before success",
                    100 * timeout_fraction,
                    time_diff,
                    timeout,
                )

    def sync_tester(
        self: "Assertion",  # type: ignore # noqa: F821
        test: Callable,
        tests: Tuple,
        msg: Optional[str],
        raised_exc: TExc,
        timeout: float,
        exc_pass: TExcTuple,
        exc_ignore: TExcTuple,
    ) -> DummyAwaitable:
        time_start = monotonic()
        delay = self.delay_init
        exc_ignore += (raised_exc,)
        while True:
            try:
                evaluated = []
                for t in tests:
                    if callable(t):
                        evaluated.append(t())
                    else:
                        evaluated.append(t)

                test(
                    self,
                    *evaluated,
                    msg=msg,
                    raised_exc=raised_exc,
                )
                break
            except exc_pass:
                break
            except exc_ignore as e:
                exc = e

            time_diff = monotonic() - time_start
            if time_diff >= timeout:
                if isinstance(exc, raised_exc):
                    raise exc
                else:
                    raise raised_exc
            else:
                time.sleep(min(delay, timeout - time_diff + 0.01))
                delay = self._get_next_delay(delay)

        if timeout > 0 and self.timeout_fraction_warning is not None:
            time_diff = monotonic() - time_start
            timeout_fraction = time_diff / timeout
            if timeout_fraction > self.timeout_fraction_warning:
                LOGGER.warning(
                    "more than %.0f%% (%.1fs) of timeout (%.1fs) "
                    "passed before success",
                    100 * timeout_fraction,
                    time_diff,
                    timeout,
                )
        # return dummy awaitable to keep redundant awaits happy
        return dummy_awaitable

    @wraps(func)
    def wrapper(
        self: "Assertion",  # type: ignore # noqa: F821
        *tests: Any,
        msg: Optional[str] = None,
        raised_exc: Optional[TExc] = None,
        timeout: Optional[float] = None,
        exc_pass: Union[TExcIter, TExc, None] = None,
        exc_ignore: Union[TExcIter, TExc, None] = None,
    ) -> Awaitable:
        raised_exc = self.raised_exc if raised_exc is None else raised_exc
        timeout = self.timeout if timeout is None else timeout
        exc_pass = self.exc_pass if exc_pass is None else as_tuple(exc_pass)
        exc_ignore = self.exc_ignore if exc_ignore is None else as_tuple(exc_ignore)

        for t in tests:
            if isawaitable(t) or iscoroutinefunction(t):
                return async_tester(
                    self,
                    func,
                    tests,
                    msg,
                    raised_exc,
                    timeout,
                    exc_pass,
                    exc_ignore,
                )
        else:
            return sync_tester(
                self,
                func,
                tests,
                msg,
                raised_exc,
                timeout,
                exc_pass,
                exc_ignore,
            )

    return wrapper
