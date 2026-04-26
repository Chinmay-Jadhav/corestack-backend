import asyncio
# import aioredis
from redis import asyncio as aioredis
from datetime import timedelta

from src.config import Config

JTI_EXPIRY = timedelta(hours=1)

token_blocklist = aioredis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0
)

async def add_jti_to_blocklist(jti : str) -> None :
    
    await token_blocklist.set(
        name=jti,
        value="",
        ex=JTI_EXPIRY
    )
    pass

async def token_in_blocklist(jti : str) -> bool :
    
    jti = await token_blocklist.get(jti)

    return jti is not None

