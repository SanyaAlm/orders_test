import json

from redis.asyncio import Redis

REDIS_URL = "redis://localhost:6379"
redis_client: Redis = Redis.from_url(REDIS_URL, decode_responses=True)

CACHE_TTL = 300


def _get_order_key(order_id: int):
    return f"order:{order_id}"


async def set_order_cache(order_id: int, data: dict, ttl: int = CACHE_TTL):
    key = _get_order_key(order_id)
    result = await redis_client.set(key, json.dumps(data), ex=ttl)
    return result


async def get_order_cache(order_id: int):
    key = _get_order_key(order_id)
    value = await redis_client.get(key)
    if value:
        return value
    return None


async def delete_order_cache(order_id: int):
    key = _get_order_key(order_id)
    await redis_client.delete(key)
