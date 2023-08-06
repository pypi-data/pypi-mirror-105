<div align="center">

[![pypi version](https://img.shields.io/pypi/v/assertion.svg)](https://pypi.org/project/assertion/) 
[![pipeline status](https://gitlab.com/coherentminds/assertion/badges/main/pipeline.svg)](https://gitlab.com/coherentminds/assertion/-/commits/main) 
[![coverage report](https://gitlab.com/coherentminds/assertion/badges/main/coverage.svg)](https://gitlab.com/coherentminds/assertion/-/commits/main) 
[![tested with hypothesis](https://img.shields.io/badge/hypothesis-tested-brightgreen.svg)](https://hypothesis.readthedocs.io) 
[![black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) 
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet.svg)](https://pdm.fming.dev) 
[![coherent minds](https://img.shields.io/badge/minds-coherent-88cdd8.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAACXBIWXMAAAK4AAACuAGk+2ZLAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAatJREFUKJFtkk1IVFEYhp/v3KvjiBMtNX8mCIwWboIQzGCgUEjwhwiCFsN0SdoZrdo5KzUXCndXizuLFuay0Aha6GJw4yiunJkWEUUguAnERpw8X4tGu3dm3tXLd97nnPccDkSVAJ4DG8BPYBJgbrt0+1W+lAgHTcjfBYrAMpACrtS8cRy6NM6X+e1iqh4cAdaB7roGV4HrVrQAdIqRT4s75Tvn4GUgB8RorlajclrzMYuuLG39iBsgXavVTIfAvj3T/tCsu9r6O+MCE6FhAdgDHOAmsAhUjSOPVf+HFB0R4DtwAEzXoIgWCuVhRDcAN4Tuu8Am8CybzZ70JJOPFO6JxZ79cWePB1K/TuV4LQoBiBhgOpfL2d6+5EeUFVE8hKdOS3X8xVBvBTTfeHUpGuDEwqzCaN3qjO/7McdteQLsRDC1H1wAq4xJ46432jsSrzvLux48HPx6rXRfRW4Zq5XKUduqALwJgiGDfAbam9TKY3jppdNbInLxthcHBUEwaJF3/PstDVLYdYUHmUzmWwQE8H0/Fu+4lBbVKYR+wEEoA+/F2ree5x2dZ/8CIW2FUo31n20AAAAASUVORK5CYII=)](https://coherentminds.de)

</div>

---------------------------------------------------------------------

# assertion

This small package solves a few issues of the regular `assert`
statements in Python:

* Regular asserts are ignored if the code is run with `python -O`.

* If an assertion fails, no additional information is given about the
  parameters which caused the fail.

* Test parameters are fixed (e.g., a variable which is `True`).

* A timing-critical test might fail *now*, but would have passed a few seconds later
  (e.g., after some action has been completed).

* In a set of tests, only tests until the first failed test are executed.

The `assertion` tests behave differently:

* The tests are always evaluated.

* If a test fails, a string representation of the provided arguments is included in the
  exception description.

* Test parameters can be
  * constants,
  * functions (sync and async),
  * other mutable variables.

* Optionally, a test can be re-evaluated until a configurable timeout is reached. By
  default, the timeout is zero and test fail instantly.

* Optionally, raising exceptions of failed tests can be deferred to allow for the
  completion of a set of tests (works also with `pytest`).


## Quickstart

Here is a simple example:

```python
>>> from assertion import Assertion
>>> assertion = Assertion()
>>> val = 999
>>> assertion.false(val)
Traceback (most recent call last):
    ...
AssertionError: 999 != False
```

Here is a more complex example using coroutines:

```python
import asyncio
from assertion import Assertion

assertion = Assertion(msg="D'oh!", timeout=10.0)

class Countdown:
    def __init__(self, start: int):
        self.counter = start

    async def countdown(self) -> bool:
        self.counter -= 1
        return self.counter == 0

async def main():
    print("Test A...")
    await assertion.true(Countdown(10).countdown)  # should be successful
    print("ok")

    print("Test B...")
    await assertion.true(Countdown(50).countdown)  # should fail
    print("ok")

asyncio.run(main())
```

> ### Note
>    The test functions act as both regular functions and as awaitables depending
>    on the test arguments.
>
>    If the test arguments contain coroutines or awaitables, you **must** `await`
>    the test.


There are several pre-defined tests:


| Function | Description |
| --- | --- |
| `true`<br>`false` | Expects single parameter and determines its boolean value. |
| `equal`<br>`not_equal`<br>`less`<br>`less_or_equal`<br>`greater`<br>`greater_or_equal` |  Expects two parameters and performs the corresponding comparison operators. |
| `in_`<br>`not_in` | Expects two parameters and uses the built-in `in` operator. |
| `is_`<br>`is_not` | Expects two parameters and uses the built-in `is` operator. |

In addition to the test parameters, each call accepts optional parameters:

* `msg` (`str`, default: ""):
  
  This message is prefixed to the exception text.

* `timeout` (`float`, unit: seconds, default: 0.0):
  
  The number of seconds until the test is finally considered as failed.

* `raised_exc` (`Type(Exception)`, default: `TestError`):
  
  Any `Exception` subclass which is raised if the test fails.

* `exc_pass`: `Type(Exception)` or `Tuple(Type(Exception))`, default: `[]`

   If one of the provided tests raises an exception in `exc_pass`, the test is
   considered to be passed, independent of the actual test criteria.

* `exc_ignore`: `Type(Exception)` or `Tuple(Type(Exception))`, default: `[]`

   If one of the provided tests raises an exception in `exc_ignore`, the exception
   is ignored, and the test evaluation proceeds.
  
> ### Note
>
> If you use a non-zero timeout, the test arguments might be evaluated/called
> multiple time. Make sure that any given function call can handle this or set
> the timeout to zero.


## Detailed Description

### Configuration

You can choose different defaults for `msg`, `raised_exc`, `timeout`, `exc_pass`,
and `exc_ignore` while creating an instance of `Assertion`.

In addition, you can specify three more parameters:

* `msg_length_max`: `int`, default: 100
  
   This limits the string representation of the provided test parameters to the given
   number of characters. The optional message is not considered and will always be
   included in full length).

* `delay_init`: `float`, default 0.125 seconds
  
  Non-zero timeout only: If the initial test fails, the arguments are re-evaluated
  after this initial delay.

* `delay_max`: `float`, default: 5.0 seconds
  
   Non-zero timeout only: This limits the delay between two test parameter
   evaluations.

* `timeout_fraction_warning`: `float`, default: 0.75 (equals 75%)
  
   Non-zero timeout only: If more than this fraction of the timeout passed before
   the test was successful, a warning is logged. If you see this warning, you might
   want to increase the timeout. Set to `None` to disable warning.
  
In the default implementation, the delay between each evaluation is doubled
(until it reaches the given maximum). This behavior can be changed by
overloading `Assert._get_new_delay`.


### Deferring

If you want to execute all tests in a set of tests even if early tests fail, you can
defer the raising of exceptions. You have three options:

* Decorator:

  ```python
  assertion = Assertion(raised_exc=ZeroDivisionError)

  @assertion.deferring_decorator
  def multiple_fails():
      assertion.true(False)
      assertion.true("this will not fail")
      assertion.equal(5, 99, raised_exc=ValueError)
      assertion.false(True, msg="D'oh!")
  ```
  When calling `multiple_fails()`, all four tests will be executed (with three
  failing), but only one exception will be raised when leaving the functions scope. Here
  is the abbreviated output of the exception:

      ZeroDivisionError: 3 deferred exception(s):
          ZeroDivisionError[File "<input>", line 5, in multiple_fails, "<code unavailable>"]: False != True
          ValueError[File "<input>", line 7, in multiple_fails, "<code unavailable>"]: 5 != 99
          ZeroDivisionError[File "<input>", line 8, in multiple_fails, "<code unavailable>"]: D'oh!: True != False

  The decorator works for both synchronous and asynchronous functions.

* Context manager:

  If you want to define a defer scope on a sub-function level, you can use contexts:

  ```python
  assertion = Assertion(raised_exc=ZeroDivisionError)

  with assertion.deferring_context():
      for i in range(3):
          assertion.equal(i, 1)
  ```

* Explicit start/stop calls (only use as a last resort):

  ```python
  assertion = Assertion(raised_exc=ZeroDivisionError)

  assertion.start_deferring()
  for i in range(3):
      assertion.equal(i, 1)
  assertion.stop_deferring()
  ```
  When an assertion instance is garbage-collected, it checks if there are open defer
  scopes (which not always works because of the limitations during the teardown phase).
  If so, a warning and any remaining fail messages are logged, but no exception
  is raised to avoid disturbing any ongoing shutdown procedures.

Defer scopes can be nested. The raising of exceptions is deferred until *all* scopes
have been exited.


### Exception Handling

If an exception is raised from any of the tests, this exception is not caught by default
and therefore terminates the test evaluation. This behavior can be changed with the
two parameters `exc_pass` and `exc_ignore`:

* If one of the provided tests raises an exception in `exc_pass`, the test is
  considered to be passed, independent of the actual test criteria.

* If one of the provided tests raises an exception in `exc_ignore`, the exception
  is ignored, and the test evaluation proceeds. This only makes a difference if the
  `timeout` parameter is non-zero, and the tests are re-evaluated.


## Similar Packages

This package was heavily inspired by the assert magic in
`pytest <https://pytest.org>`_.

`assert-info <https://pypi.org/project/assert-info/>`_ has a slightly different
focus, but might suit you better.
