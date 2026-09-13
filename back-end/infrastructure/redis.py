from typing import Optional

from fastapi import Request

import redis.asyncio as aioredis

from core.config import settings

async def init_redis():
    redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    try:
        await redis_client.ping()
    except Exception:
        raise
    return redis_client


async def close_redis() -> None:
    global redis_client
    if redis_client is not None:
        try:
            await redis_client.close()
        finally:
            redis_client = None


def get_redis_from_request(request: Request):
    return request.app.state.redis
