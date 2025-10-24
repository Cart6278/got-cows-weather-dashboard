# api/main.py
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import redis.asyncio as redis
import json

app = FastAPI(title="Got Cows Weather Platform")
redis_client = redis.Redis(decode_responses=True)


@app.websocket("/ws/weather")
async def weather_feed(websocket: WebSocket):
    """Stream real-time weather updates to browser"""
    await websocket.accept()

    # Subscribe to Redis stream
    pubsub = redis_client.pubsub()
    await pubsub.subscribe('weather:observations')

    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                await websocket.send_json({
                    'type': 'weather_update',
                    'data': json.loads(message['data'])
                })
    except:
        await websocket.close()


@app.websocket("/ws/alerts")
async def cow_alerts(websocket: WebSocket):
    """Special alerts for cow-worthy conditions"""
    await websocket.accept()
    pubsub = redis_client.pubsub()
    await pubsub.subscribe('alerts:cows')

    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                await websocket.send_json({
                    'type': 'COW_ALERT',
                    'message': message['data']
                })
    except:
        await websocket.close()