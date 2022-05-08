# coding=utf-8
from functools import wraps
import time
from typing import Any, Callable, TypeVar

R = TypeVar('R')


def timeit(func: Callable[..., R]) -> Callable[..., R]:
    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> R:
        start: int = time.perf_counter_ns()
        result: Any = func(*args, **kwargs)
        perf: int = time.perf_counter_ns() - start

        print(f"Performance({func.__name__}): {perf}s")

        return result

    return inner


def debug(func: Callable[..., R]) -> Callable[..., R]:
    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> R:
        arguments: str = ", ".join(
            [str(a) for a in args] + [f"{k}={v}" for k, v in kwargs.items()]
        )

        print(f"{func} invoked as: {func.__name__}({arguments})")

        start: int = time.perf_counter_ns()
        result: Any = func(*args, **kwargs)
        perf: int = time.perf_counter_ns() - start

        print(f"{func} returned: {result} (runtime: {perf/1000000000}s)")

        return result

    return inner
