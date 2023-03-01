# coding=utf-8
__all__ = ["LoggingMixin", "JsonFormatter"]

import datetime
import io
import logging
import traceback
from types import TracebackType
from typing import (
    Optional, 
    Any, 
    Callable, 
    Union, 
    Type, 
    Tuple, 
    TypeAlias, 
    List, 
    Dict,
)

try:
    import ujson as json
except ImportError:
    import json


ExceptionInfo: TypeAlias = Union[
    Tuple[Type[BaseException], BaseException, Optional[TracebackType]],
    Tuple[None, None, None],
]


class LoggingMixin:
    _logger: Union[logging.Logger, None] = None

    def __get_logger(self) -> logging.Logger:
        name: str = self.__class__.__module__ + "." + self.__class__.__name__

        return logging.getLogger(name=name)

    @property
    def log(self) -> logging.Logger:
        """Returns a logger."""

        if self._logger is None:
            self._logger = self.__get_logger()

        return self._logger


class JsonFormatter(logging.Formatter):
    """Format log records as JSON"""

    formatter: Callable[[Dict], str] = json.dumps

    def __init__(
        self,
        fields: List[str],
        rename_fields: Optional[Dict[str, str]] = None,
        static_fields: Optional[Dict[str, Any]] = None,
        timestamp: bool = True,
        dt_fmt: Optional[str] = None,
        dt_tz: datetime.tzinfo = datetime.timezone.utc,
    ) -> None:
        """Initialize the created instance"""

        super().__init__()

        self._fields: List[str] = fields
        self._rename_fields: Optional[Dict[str, str]] = rename_fields or {}
        self._static_fields: Optional[Dict[str, Any]] = static_fields or {}
        self._dt_fmt: Optional[str] = dt_fmt
        self._dt_tz: datetime.tzinfo = dt_tz

        self._uses_time: bool = False

        if "asctime" in self._fields:
            self._uses_time = True
        elif timestamp:
            # Append to the beginning
            self._fields = ["asctime"] + self._fields
            self._rename_fields["asctime"] = "@timestamp"

            self._uses_time = True

    def format_exception(self, exc_info: ExceptionInfo) -> str:
        """Format the provided exception as a single line"""

        string_io: io.StringIO = io.StringIO()
        traceback.print_exception(*exc_info, limit=None, file=string_io)
        stack_trace: str = string_io.getvalue()
        string_io.close()

        if stack_trace[-1:] == "\n":
            stack_trace = stack_trace[:-1]

        return stack_trace

    def format_stack(self, stack_info: str) -> str:
        """Format the provided stack info"""

        return stack_info

    def format_time(self, dt: datetime.datetime) -> str:
        """Convert datetime to string, default ISO standard"""

        if self._dt_fmt is None:
            return dt.isoformat()

        return dt.strftime(self._dt_fmt)

    def format(self, record: logging.LogRecord) -> str:
        """Format the provided LogRecord as string, omit None values"""

        log_dict: Dict[str, Any] = {}

        # This replaces args in message with user supplied args
        # (not recommended but supported)
        record.message = record.getMessage()

        if self._uses_time:
            dt: datetime.datetime = datetime.datetime.fromtimestamp(
                record.created, tz=self._dt_tz
            )
            record.asctime = self.format_time(dt=dt)

        if record.exc_info:
            record.exc_info = self.format_exception(exc_info=record.exc_info)
        elif record.exc_text:
            record.exc_info = record.exc_text

        if record.stack_info:
            record.stack_info = self.format_stack(record.stack_info)

        for field in self._fields:
            value: Any = record.__dict__.get(field)

            if value is not None:
                # key is either field itself (default) or the renamed variant
                log_dict[self._rename_fields.get(field, field)] = value

        return JsonFormatter.formatter({**log_dict, **self._static_fields})
