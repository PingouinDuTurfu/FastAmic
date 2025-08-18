import asyncio
import json
from typing import Union

import aio_pika
from aiormq import AMQPConnectionError, ChannelClosed

from app.core.env_config import settings


class RMQService:
    def __init__(self, name: str = "unknown"):
        self.connection = None
        self.channel = None
        self.exchange = None
        self.name = name
        self.lock = asyncio.Lock()

    async def connect(self):
        if self.connection and not self.connection.is_closed:
            return

        try:
            self.connection = await aio_pika.connect_robust(
                host=settings.RMQ_HOST,
                login=settings.RMQ_USER,
                password=settings.RMQ_PASSWORD,
                virtualhost=settings.RMQ_VHOST,
                client_properties = {
                    'name': self.name
                }
            )
            self.channel = await self.connection.channel()

        except AMQPConnectionError as e:
            raise RuntimeError(f"Failed to connect to RabbitMQ: {e}")

    async def disconnect(self):
        if self.channel and not self.channel.is_closed:
            await self.channel.close()

        if self.connection and not self.connection.is_closed:
            await self.connection.close()

    async def publish(self, queue: str, message: Union[str, dict]):
        if isinstance(message, dict):
            body = json.dumps(message).encode()
            content_type = "application/json"
        elif isinstance(message, str):
            body = message.encode()
            content_type = "text/plain"
        else:
            raise TypeError("Message must be str or dict")

        try:
            if not self.channel or self.channel.is_closed:
                await self.connect()

            await self.channel.default_exchange.publish(
                aio_pika.Message(
                    body=body,
                    content_type=content_type
                ),
                routing_key=queue
            )

        except (AMQPConnectionError, ChannelClosed):
            async with self.lock:
                try:
                    await self.connect()

                    await self.channel.default_exchange.publish(
                        aio_pika.Message(
                            body=body,
                            content_type=content_type
                        ),
                        routing_key=queue
                    )

                except Exception as e:
                    raise RuntimeError(f"Failed to publish to RMQ after reconnect: {e}")