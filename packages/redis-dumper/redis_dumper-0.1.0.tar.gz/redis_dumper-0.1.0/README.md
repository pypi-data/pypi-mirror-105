# Redis Dumper
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/redis_dumper?logo=python&style=flat-square)](https://python.org)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/redis_dumper?style=flat-square)](https://pypi.org/project/redis_dumper)
[![PyPi Package Version](https://img.shields.io/pypi/v/redis_dumper?style=flat-square)](https://pypi.org/project/redis_dumper)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/DavisDmitry/redis_dumper/Tests/master?label=tests&style=flat-square)](https://github.com/DavisDmitry/redis_dumper/actions/workflows/tests.yml)
[![GitHub](https://img.shields.io/github/license/DavisDmitry/redis_dumper?style=flat-square)](https://github.com/DavisDmitry/redis_dumper/raw/master/LICENSE)

CLI utility and library for creating encrypted redis dump.
## Install
```shell
pip install redis_dumper
```
## Use in CLI
```shell
redis_dumper [OPTIONS] COMMAND [ARGS]...
```
## Use in your code
Examples:
```python
import io
import aioredis
import redis_dumper


REDIS_ADDR = 'redis://10.0.0.1:6379'
PASSWORD = 'qwerty'
FILE_PATH = 'mydump.rdump'


async def dump_to_file_example():
    await redis_dumper.dump_to_file(REDIS_ADDR, PASSWORD, FILE_PATH)


async def dump_to_bytesio_example():
    dump = await redis_dumper.dump_to_bytesio(REDIS_ADDR, PASSWORD)


async def restore_from_file_example():
    await redis_dumper.restore_from_file(REDIS_ADDR, PASSWORD, FILE_PATH)


async def restore_from_bytesio_example(dump: io.BytesIO):
    await redis_dumper.restore_from_bytesio(REDIS_ADDR, PASSWORD, dump)


# you can also use the already created aioredis.Redis instance
async def example_with_created_redis():
    redis = await aioredis.create_redis(REDIS_ADDR)
    dump = await redis_dumper.dump_to_bytesio(redis, PASSWORD)

```
