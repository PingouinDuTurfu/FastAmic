import asyncio

import aiomysql
from pymysql import OperationalError, InterfaceError

from app.core.env_config import settings


class MySQLService:
    def __init__(self):
        self.pool = None
        self.lock = asyncio.Lock()

    async def connect(self):
        if self.pool:
            await self.disconnect()

        self.pool = await aiomysql.create_pool(
            host=settings.MYSQL_HOST,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            db=settings.MYSQL_DATABASE_MAIN,
            minsize=settings.MYSQL_POOL_SIZE_MIN,
            maxsize=settings.MYSQL_POOL_SIZE_MAX,
            port=settings.MYSQL_PORT
        )

    async def disconnect(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            self.pool = None

    async def execute(self, sql: str, params=None):
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(sql, params or ())
                    return await cur.fetchall()

        except (OperationalError, InterfaceError):
            async with self.lock:
                for attempt in range(settings.MYSQL_RETRY_LIMIT):
                    try:
                        await self.connect()
                        async with self.pool.acquire() as conn:
                            async with conn.cursor(aiomysql.DictCursor) as cur:
                                await cur.execute(sql, params or ())
                                return await cur.fetchall()

                    except (OperationalError, InterfaceError):
                        await asyncio.sleep(settings.MYSQL_RETRY_DELAY_SECONDS)

        raise RuntimeError("MySQL execute failed after retrying.")