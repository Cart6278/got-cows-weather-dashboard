import redis
from typing import Optional


class RedisConfig:
    """Redis connection configuration"""
    HOST = "localhost"  # or "redis" if running in Docker network
    PORT = 6379
    DB = 0
    DECODE_RESPONSES = True  # Automatically decode bytes to strings


def get_redis_client() -> redis.Redis:
    """Get a Redis client connection"""
    return redis.Redis(
        host=RedisConfig.HOST,
        port=RedisConfig.PORT,
        db=RedisConfig.DB,
        decode_responses=RedisConfig.DECODE_RESPONSES
    )


def test_connection() -> bool:
    """Test Redis connection"""
    try:
        client = get_redis_client()
        client.ping()
        print("✅ Redis connection successful!")
        return True
    except redis.ConnectionError as e:
        print(f"❌ Redis connection failed: {e}")
        return False
