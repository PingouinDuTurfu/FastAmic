import asyncio
from elasticsearch import AsyncElasticsearch, helpers
from typing import List

from app.core.env_config import settings


class LogService:
    def __init__(self, api_name: str = "unknown"):
        self.buffer: List[dict] = []
        self.bulk_size = settings.ELASTIC_BULK_SIZE
        self.flush_interval = settings.ELASTIC_FLUSH_INTERVAL
        self._task = None
        self._running = True
        self.es = AsyncElasticsearch(hosts=[settings.ELASTIC_LOGS_URL])
        self.api_name = api_name

    async def start(self):
        self._task = asyncio.create_task(self._flush_loop())

    async def index(self, index: str, doc: dict):
        self.buffer.append({
            "_index": index,
            "_source": {
                "proc_name": self.api_name,
                **doc
            }
        })

        if len(self.buffer) >= self.bulk_size:
            await self._flush()

    async def _flush_loop(self):
        while self._running:
            await asyncio.sleep(self.flush_interval)
            await self._flush()

    async def _flush(self):
        if not self.buffer:
            return

        try:
            success, errors = await helpers.async_bulk(self.es, self.buffer, raise_on_error=False)
            if errors:
                print(f"[LogService] Partial errors during bulk: {errors}")
        except Exception as e:
            print(f"[LogService] Bulk error: {e}")

        self.buffer.clear()

    async def flush_and_close(self):
        self._running = False
        await self._flush()
        await self.es.close()
