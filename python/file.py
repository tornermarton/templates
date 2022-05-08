# coding=utf-8
from __future__ import annotations

import abc
import bz2
import copy
import gzip
import lzma
import shutil
from pathlib import Path
from dataclasses import dataclass
from typing import Any, Optional, Type

_compressions: dict[str, Type[Compression]] = {}


def create_compression(name: str) -> Type[Compression]:
    return _compressions[name]


class Compression(metaclass=abc.ABCMeta):
    def __init__(
        self,
        name: str,
        extension: Optional[str] = None
    ) -> None:
        self._name: str = name
        self._extension: str = extension or f".{name}"

    @property
    def name(self) -> str:
        return self._name

    @property
    def extension(self) -> str:
        return self._extension

    @abc.abstractmethod
    def open(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError()


class GzipCompression(Compression):
    def __init__(self, extension: Optional[str] = ".gz") -> None:
        super().__init__("gzip", extension)

    def open(self, *args: Any, **kwargs: Any) -> Any:
        return gzip.open(*args, **kwargs)


_compressions["gzip"] = GzipCompression


class Bzip2Compression(Compression):
    def __init__(self, extension: Optional[str] = ".bz2") -> None:
        super().__init__("bzip2", extension)

    def open(self, *args: Any, **kwargs: Any) -> Any:
        return bz2.open(*args, **kwargs)


_compressions["bzip2"] = Bzip2Compression


class LzmaCompression(Compression):
    def __init__(self, extension: Optional[str] = ".xz") -> None:
        super().__init__("lzma", extension)

    def open(self, *args: Any, **kwargs: Any) -> Any:
        return lzma.open(*args, **kwargs)


_compressions["lzma"] = LzmaCompression


@dataclass
class File(object):
    path: Path
    encoding: str = "utf-8",
    is_binary: bool = False,
    compression: Optional[Compression] = None

    def open(self, *args: Any, **kwargs: Any) -> Any:
        if self.compression is not None:
            self.compression.open(*args, **kwargs)
        else:
            return open(*args, **kwargs)

    def copy(self, target: File) -> None:
        with self.open('rb') as source_file:
            with target.open('wb') as target_file:
                shutil.copyfileobj(source_file, target_file)


class Compressor(object):
    def __init__(self, compression: Compression) -> None:
        self._compression: Compression = compression

    def compress(
        self,
        source: File,
        target: Optional[File] = None,
        delete_source: bool = False,
    ) -> File:
        if not target:
            file_name: str = f"{source.path.name}{self._compression.extension}"
            target: File = copy.deepcopy(source)
            target.path = source.path.parent / file_name

        if target.path.exists():
            raise FileExistsError(
                f"The target file {target.path} already exists, "
                f"aborting compression to prevent overwriting data!"
            )

        try:
            source.copy(target=target)
        except Exception as e:
            # Provide atomicity
            if target.path.exists():
                target.path.unlink()

            raise e
        else:
            # Delete file if compression was successful
            if delete_source:
                source.path.unlink()

            return target
