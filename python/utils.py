# coding=utf-8
import copy
import datetime
import functools
import time
from typing import Any, Callable, Iterator, Optional, TypeVar

R = TypeVar('R')


def timeit(f: Callable[..., R]) -> Callable[..., R]:
    @functools.wraps(f)
    def inner(*args: Any, **kwargs: Any) -> R:
        start: int = time.perf_counter_ns()
        result: Any = f(*args, **kwargs)
        perf: int = time.perf_counter_ns() - start

        print(f"Performance({f.__name__}): {perf}s")

        return result

    return inner


def debug(f: Callable[..., R]) -> Callable[..., R]:
    @functools.wraps(f)
    def inner(*args: Any, **kwargs: Any) -> R:
        arguments: str = ", ".join(
            [str(a) for a in args] + [f"{k}={v}" for k, v in kwargs.items()]
        )

        print(f"{f} invoked as: {f.__name__}({arguments})")

        start: int = time.perf_counter_ns()
        result: Any = f(*args, **kwargs)
        perf: int = time.perf_counter_ns() - start

        print(f"{f} returned: {result} (runtime: {perf / 1000000000}s)")

        return result

    return inner


def dt_range(
    start: datetime.date,
    end: datetime.date,
    step: datetime.timedelta,
) -> Iterator[datetime.datetime]:
    """Range for dates and datetimes like for numbers range(1, 10)"""

    if (
        issubclass(type(start), datetime.datetime) or
        issubclass(type(end), datetime.datetime) or
        (step.seconds > 0 or step.microseconds > 0)
    ):
        c: datetime.datetime = datetime.datetime.fromordinal(start.toordinal())
        e: datetime.datetime = datetime.datetime.fromordinal(end.toordinal())
    else:
        c: datetime.date = copy.deepcopy(start)
        e: datetime.date = copy.deepcopy(end)

    while c < e:
        yield c
        c += step


def is_empty(s: Optional[str]) -> bool:
    return s is None or s.strip() == ""
