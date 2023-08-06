import asyncio
import getpass
from datetime import datetime
from typing import Callable

import click

from . import dumper


cli = click.Group()


def add_options(func: Callable) -> Callable:
    func = click.option(
        '-r', '--redis-address',
        metavar='URL', type=str, default='redis://localhost:6379',
        help='Redis URL, redis://localhost:6379 by default.'
    )(func)
    func = click.option(
        '-f', '--file-path',
        metavar='PATH', type=str,
        default=f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.rdump',
        help='Path to file with dumped data, datetime_now.rdump by_default.'
    )(func)
    return func


@cli.command()
@add_options
def dump(redis_address: str, file_path: str):
    password = getpass.getpass()
    asyncio.run(dumper.dump_to_file(redis_address, password, file_path))


@cli.command()
@add_options
def restore(redis_address: str, file_path: str):
    password = getpass.getpass()
    asyncio.run(dumper.restore_from_file(redis_address, password, file_path))


if __name__ == '__main__':
    cli()
