# processing/storm_detector.py
import json

from api.main import redis_client


class StormDetecting:
    """
    Detect severe weather patterns
    Reference: Twister's Dorothy would be proud
    """

    def __init__(self):
        self.pressure_history = {}

    async def analyze_stream(self):
        """Process weather stream for patterns"""
        while True:
            # Read from Redis Stream
            messages = await redis_client.xread({'weather:observations': '0'})

            for message in messages:
                data = json.loads(message['data'])
                station = data['station']

                # Detect rapid pressure drops (tornado indicator)
                pressure_drop = self.calculate_pressure_change(station, data['pressure'])

                if pressure_drop > 4:  # mb/hour
                    # Dorothy would definitely deploy here!
                    await self.send_tornado_alert(station, pressure_drop)

                # Check for "cow conditions"
                if self.check_cow_conditions(data):
                    await redis_client.publish(
                        'alerts:cows',
                        f"COW ALERT at {station}! Wind: {data['wind_speed']}mph"
                    )