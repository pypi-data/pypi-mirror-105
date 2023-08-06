from hypothesis import assume, given, settings
from hypothesis.strategies import sampled_from
from pytest import mark, raises

from assertion import Assertion
from tests.conftest import builtin_exceptions, get_exception_raiser

short_wait = Assertion(timeout=2.0)


@given(
    exception_class=sampled_from(builtin_exceptions),
    exception_call=sampled_from(builtin_exceptions + [None]),
)
@settings(max_examples=1000)
def test_exception_parameter_sync(exception_class, exception_call):
    bssertion = Assertion(raised_exc=exception_class)

    with raises(Exception) as exc:
        bssertion.in_(5, {1, 2, 3, 4}, raised_exc=exception_call)

    assert exc.type is (exception_class if exception_call is None else exception_call)


@given(
    exception_class=sampled_from(builtin_exceptions),
    exception_call=sampled_from(builtin_exceptions + [None]),
)
@settings(max_examples=1000)
@mark.asyncio
async def test_exception_parameter_async(exception_class, exception_call):
    assume(StopIteration not in {exception_class, exception_call})

    bssertion = Assertion(raised_exc=exception_class)

    async def return_3():
        return 3

    with raises(Exception) as exc:
        await bssertion.not_in(return_3, {1, 2, 3, 4}, raised_exc=exception_call)

    assert exc.type is (exception_class if exception_call is None else exception_call)


@given(exception=sampled_from(builtin_exceptions))
def test_exceptions_fail_test(exception):
    def raise_exception():
        raise exception("hovercraft")

    with raises(exception) as exc:
        short_wait.true(raise_exception)
    assert "hovercraft" in str(exc.value)


@given(
    raised_exc=sampled_from(builtin_exceptions),
    exc_pass=sampled_from(builtin_exceptions),
)
@settings(max_examples=20, deadline=1000)
def test_exception_passes_sync(raised_exc, exc_pass):
    if raised_exc is exc_pass:
        short_wait.true(get_exception_raiser(2, raised_exc), exc_pass=exc_pass)
    else:
        with raises(raised_exc):
            short_wait.true(get_exception_raiser(2, raised_exc), exc_pass=exc_pass)


@given(
    raised_exc=sampled_from(builtin_exceptions),
    exc_pass=sampled_from(builtin_exceptions),
)
@settings(max_examples=20, deadline=1000)
@mark.asyncio
async def test_exception_passes_async(raised_exc, exc_pass):
    assume(StopIteration not in {raised_exc, exc_pass})

    if raised_exc is exc_pass:
        await short_wait.true(
            get_exception_raiser(2, raised_exc, async_=True), exc_pass=exc_pass
        )
    else:
        with raises(raised_exc):
            await short_wait.true(
                get_exception_raiser(2, raised_exc, async_=True), exc_pass=exc_pass
            )


@given(
    raised_exc=sampled_from(builtin_exceptions),
    exc_ignore=sampled_from(builtin_exceptions),
    timeout=sampled_from([0.1, 2.0]),
)
@settings(max_examples=50, deadline=1000)
def test_exception_ignored_sync(raised_exc, exc_ignore, timeout):
    if raised_exc is exc_ignore and timeout > 1.0:
        short_wait.false(
            get_exception_raiser(2, raised_exc, flavor="raise_first"),
            exc_ignore=exc_ignore,
            timeout=timeout,
        )
    else:
        with raises(Exception) as exc:
            short_wait.false(
                get_exception_raiser(2, raised_exc, flavor="raise_first"),
                exc_ignore=exc_ignore,
                timeout=timeout,
            )

        assert exc.type is (
            short_wait.raised_exc if raised_exc is exc_ignore else raised_exc
        )


@given(
    raised_exc=sampled_from(builtin_exceptions),
    exc_ignore=sampled_from(builtin_exceptions),
    timeout=sampled_from([0.1, 2.0]),
)
@settings(max_examples=50, deadline=1000)
@mark.asyncio
async def test_exception_ignored_async(raised_exc, exc_ignore, timeout):
    assume(StopIteration not in {raised_exc, exc_ignore})

    if raised_exc is exc_ignore and timeout > 1.0:
        await short_wait.false(
            get_exception_raiser(2, raised_exc, flavor="raise_first", async_=True),
            timeout=timeout,
            exc_ignore=exc_ignore,
        )
    else:
        with raises(Exception) as exc:
            await short_wait.false(
                get_exception_raiser(2, raised_exc, flavor="raise_first", async_=True),
                timeout=timeout,
                exc_ignore=exc_ignore,
            )

        assert exc.type is (
            short_wait.raised_exc if raised_exc is exc_ignore else raised_exc
        )


def test_exception_parameters():
    Assertion(exc_pass=(IOError, ValueError))
    Assertion(exc_pass=[IOError, ValueError])
    with raises(ValueError):
        Assertion(exc_pass=42)
