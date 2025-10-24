import asyncio
import aiohttp
from datetime import datetime
import redis.asyncio as redis
import json
import logging


class NOAACollector:
    """Gathers real-time weather and alerts from the NOAA and NWS APIs."""

    def __init__(self, stations=None, redis_url="redis://localhost", wind_speed_threshold=50, sleep_interval=300):
        """
        Initialize the NOAACollector.

        :param stations: List of station codes to collect data from.
        :param redis_url: Redis connection URL.
        :param wind_speed_threshold: Wind speed threshold for cow alerts (in mph).
        :param sleep_interval: Interval between data collection cycles (in seconds).
        """
        self.stations = stations or ['KPDX', 'KSEA', 'KBOI']
        self.redis_client = redis.Redis.from_url(redis_url, decode_responses=True)
        self.wind_speed_threshold = wind_speed_threshold
        self.sleep_interval = sleep_interval
        self.session = None

    async def collect_station_data(self, station: str):
        """
        Fetch current conditions from NOAA for a specific station.

        :param station: Station code.
        :return: Transformed weather data or None if the request fails.
        """
        url = f"https://api.weather.gov/stations/{station}/observations/latest"
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return self.transform_noaa_data(data)
                else:
                    logging.warning(f"Failed to fetch data for {station}: {response.status}")
        except Exception as e:
            logging.error(f"Error fetching data for {station}: {e}")
        return None

    @staticmethod
    def transform_noaa_data(data):
        """
        Transform NOAA data into a desired format.

        :param data: Raw NOAA data.
        :return: Transformed data.
        """
        return {
            "station": data.get("properties", {}).get("station"),
            "timestamp": data.get("properties", {}).get("timestamp"),
            "temperature": data.get("properties", {}).get("temperature", {}).get("value"),
            "wind_speed": data.get("properties", {}).get("windSpeed", {}).get("value"),
            "precipitation": data.get("properties", {}).get("precipitationLastHour", {}).get("value"),
            "pressure": data.get("properties", {}).get("barometricPressure", {}).get("value"),
            "humidity": data.get("properties", {}).get("relativeHumidity", {}).get("value"),
            "cloud_cover": data.get("properties", {}).get("cloudLayers", [{}])[0].get("amount"),
        }

    async def run_collector(self):
        """Continuously collect weather data and publish to Redis."""
        self.session = aiohttp.ClientSession()
        try:
            while True:
                for station in self.stations:
                    try:
                        data = await self.collect_station_data(station)
                        if data:
                            # Publish to Redis Stream
                            await self.redis_client.xadd(
                                'weather:observations',
                                {'data': json.dumps(data)}
                            )

                            # Check for cow conditions!
                            if data['wind_speed'] and data['wind_speed'] > self.wind_speed_threshold:
                                await self.redis_client.publish(
                                    'alerts:cows',
                                    f"We got cows at {station}!"
                                )
                    except Exception as e:
                        logging.error(f"Error collecting from {station}: {e}")

                await asyncio.sleep(self.sleep_interval)
        finally:
            await self.session.close()
            await self.redis_client.close()