import asyncio
import redis.asyncio as redis
import logging
import json


class RedisEventProcessor:
    """Handles Redis events such as subscriptions and stream processing."""

    def __init__(self, redis_url="redis://localhost"):
        """
        Initialize the RedisEventProcessor.

        :param redis_url: Redis connection URL.
        """
        self.redis_client = redis.Redis.from_url(redis_url, decode_responses=True)

    async def subscribe_to_channel(self, channel_name):
        """
        Subscribe to a Redis channel and process messages.

        :param channel_name: Name of the Redis channel to subscribe to.
        """
        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe(channel_name)
        logging.info(f"Subscribed to channel: {channel_name}")

        try:
            async for message in pubsub.listen():
                if message["type"] == "message":
                    await self.process_message(channel_name, message["data"])
        except Exception as e:
            logging.error(f"Error in channel subscription: {e}")
        finally:
            await pubsub.unsubscribe(channel_name)
            await pubsub.close()

    async def process_message(self, channel_name, message):
        """
        Process a message received from a Redis channel.

        :param channel_name: Name of the channel.
        :param message: Message data.
        """
        logging.info(f"Message from {channel_name}: {message}")
        # Add custom message processing logic here

    async def process_stream(self, stream_name, last_id="0"):
        """
        Process messages from a Redis stream.

        :param stream_name: Name of the Redis stream.
        :param last_id: ID of the last processed message.
        """
        try:
            while True:
                messages = await self.redis_client.xread({stream_name: last_id}, block=0)
                for stream, entries in messages:
                    for entry_id, data in entries:
                        await self.process_stream_entry(stream, entry_id, data)
                        last_id = entry_id
        except Exception as e:
            logging.error(f"Error in stream processing: {e}")

    async def process_stream_entry(self, stream_name, entry_id, data):
        """
        Process a single entry from a Redis stream.

        :param stream_name: Name of the stream.
        :param entry_id: ID of the stream entry.
        :param data: Data of the stream entry.
        """
        logging.info(f"Stream {stream_name} Entry {entry_id}: {json.dumps(data)}")
        # Add custom stream entry processing logic here

    async def close(self):
        await self.redis_client.close()


if __name__ == "__main__":
    async def main():
        processor = RedisEventProcessor()
        await asyncio.gather(
            processor.subscribe_to_channel("alerts:cows"),
            processor.process_stream("weather:observations"),
        )

    asyncio.run(main())