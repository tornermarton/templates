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
        perf_s: float = (time.perf_counter_ns() - start) / 1_000_000_000

        print(f"Performance({f.__module__}.{f.__qualname__}): {perf_s:.9f}s")

        return result

    return inner


def debug(f: Callable[..., R]) -> Callable[..., R]:
    @functools.wraps(f)
    def inner(*args: Any, **kwargs: Any) -> R:
        pos_args: list[str] = [str(a) for a in args]
        key_args: list[str] = [f"{k}={v}" for k, v in kwargs.items()]

        arguments: str = ", ".join(pos_args + key_args)
        print(f"{f} invoked as: {f.__module__}.{f.__name__}({arguments})")

        start: int = time.perf_counter_ns()
        result: Any = f(*args, **kwargs)
        perf_s: float = (time.perf_counter_ns() - start) / 1_000_000_000

        print(f"{f} returned: {result} (runtime: {perf_s:.9f}s)")

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
