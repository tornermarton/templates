# coding=utf-8
__all__ = ["cli"]

import click


@click.command()
@click.version_option()
def cli() -> None:
    print("OK")
