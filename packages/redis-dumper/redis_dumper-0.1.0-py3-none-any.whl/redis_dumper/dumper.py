import base64 as b64
import io
import json
from typing import Dict, Tuple, Union

import aioredis
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


PASS_HASH_SALT = b''
PASS_HASH_ITERATES = 8


async def dump_to_file(
        redis: Union[str, aioredis.Redis], password: str, file_path: str
) -> None:
    with open(file_path, 'wb') as file:
        file.write(encrypt_data(await redis_data_to_json(redis),
                                password))


async def dump_to_bytesio(
        redis: Union[str, aioredis.Redis], password: str
) -> io.BytesIO:
    return io.BytesIO(encrypt_data(await redis_data_to_json(redis),
                                   password))


def encrypt_data(data: str, password: str) -> bytes:
    data = b64.urlsafe_b64encode(data.encode())
    fernet = Fernet(transform_password(password))
    return fernet.encrypt(data)


async def redis_data_to_json(redis: Union[str, aioredis.Redis]) -> str:
    return json.dumps(await redis_data_to_dict(redis))


async def redis_data_to_dict(
        redis: Union[str, aioredis.Redis]
) -> Dict[str, str]:
    redis, close_redis = await create_redis(redis)
    data = {}
    for key in await redis.keys('*'):
        data.update({
            key.decode(): b64.b64encode(await redis.dump(key)).decode()
        })
    if close_redis:
        redis.close()
    return data


async def restore_from_file(
        redis: Union[str, aioredis.Redis], password: str, file_path: str
) -> None:
    with open(file_path, 'rb') as file:
        await restore_decrypted_data(redis, decrypt_data(file.read(),
                                                         password))


async def restore_from_bytesio(
        redis: Union[str, aioredis.Redis], password: str, data: io.BytesIO
) -> None:
    await restore_decrypted_data(redis, decrypt_data(data.read(), password))


async def restore_decrypted_data(
        redis: Union[str, aioredis.Redis], data: str
) -> None:
    data: Dict[str, str] = json.loads(data)
    redis, close_redis = await create_redis(redis)
    for key, value in data.items():
        await redis.restore(key.encode(), 0, b64.b64decode(value))
    if close_redis:
        redis.close()


def decrypt_data(data: bytes, password: str) -> str:
    fernet = Fernet(transform_password(password))
    data = fernet.decrypt(data)
    return b64.urlsafe_b64decode(data).decode()


def transform_password(
        password: str,
        hash_salt: bytes = PASS_HASH_SALT,
        hash_iterates: int = PASS_HASH_ITERATES
) -> bytes:
    kdf = PBKDF2HMAC(hashes.SHA256(), 32, hash_salt, hash_iterates)
    return b64.urlsafe_b64encode(kdf.derive(password.encode()))


async def create_redis(
        redis: Union[str, aioredis.Redis]
) -> Tuple[aioredis.Redis, bool]:
    if isinstance(redis, aioredis.Redis):
        return redis, False
    return await aioredis.create_redis(redis)
