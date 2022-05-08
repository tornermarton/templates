# coding=utf-8
from __future__ import annotations

import abc
import types
import weakref
from typing import Any, Optional, Type


class SingletonMeta(type):
    """Metaclass for singletons."""

    _instances = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]


class Observer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def update(
        self,
        subject: Optional[Observable] = None,
        parameters: Optional[Any] = None
    ) -> None:
        raise NotImplementedError()


class Observable(metaclass=abc.ABCMeta):
    def __init__(self):
        self._subscribers: weakref.WeakSet[Observer] = weakref.WeakSet()

    def subscribe(self, observer: Observer) -> None:
        self._subscribers.add(observer)

    def notify(self, parameters: Optional[Any] = None) -> None:
        for s in self._subscribers:
            s.update(subject=self, parameters=parameters)


class Runnable(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError()


class Closable(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def close(self) -> None:
        raise NotImplementedError()


class ContextManager(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __enter__(self) -> Any:
        raise NotImplementedError()

    @abc.abstractmethod
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[types.TracebackType]
    ) -> Optional[bool]:
        raise NotImplementedError()


class ClosableContextManager(Closable, ContextManager, metaclass=abc.ABCMeta):
    def __enter__(self) -> ClosableContextManager:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[types.TracebackType]
    ) -> Optional[bool]:
        self.close()

        return
