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
from typing import Any, Optional, Type, Union

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
            return self.compression.open(self.path, *args, **kwargs)
        else:
            return open(self.path, *args, **kwargs)

    def copy_content_binary(
        self,
        target: File,
        overwrite: bool = False,
    ) -> None:
        if target.path.exists() and not overwrite:
            raise FileExistsError(
                f"The target {target.path} already exists, operation aborted!"
            )
        try:
            with self.open('rb') as source_file:
                with target.open('wb') as target_file:
                    shutil.copyfileobj(source_file, target_file)
        except Exception as e:
            if target.path.exists():
                target.path.unlink()

            raise e

    def compress(
            self,
            compression: Union[str, Compression] = GzipCompression(),
            target_path: Optional[Path] = None,
            overwrite: bool = False,
            delete_source: bool = False,
    ) -> File:
        if isinstance(compression, str):
            compression = create_compression(name=compression)

        target: File = copy.deepcopy(self)
        target.compression = compression

        if target_path is None:
            name: str = f"{self.path.name}{compression.extension}"
            target.path = self.path.parent / name
        else:
            target.path = target_path

        self.copy_content_binary(target=target, overwrite=overwrite)

        if delete_source:
            self.path.unlink()

        return target

    def uncompress(
        self,
        target_path: Optional[Path] = None,
        overwrite: bool = False,
        delete_source: bool = False,
    ) -> File:
        target: File = copy.deepcopy(self)
        target.compression = None

        if target_path is None:
            name: str = self.path.name.lstrip(self.compression.extension)
            target.path = self.path.parent / name
        else:
            target.path = target_path

        self.copy_content_binary(target=target, overwrite=overwrite)

        if delete_source:
            self.path.unlink()

        return target
