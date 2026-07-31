import asyncio
import random
from core.events import TelemetryReceivedEvent
from sources.base import BaseSource


class TelemetryFileSource(BaseSource):
    """Fuente de telemetría de vehículos (simulación de tail asíncrono)."""

    def __init__(self, interval: float = 1.5, **kwargs) -> None:
        super().__init__(name="TelemetryFileSource", **kwargs)
        self.interval: float = interval
        self._vehicles = ["VEH-01", "VEH-02", "VEH-03", "VEH-04"]

    async def start(self) -> None:
        await super().start()
        while self.is_running:
            vehicle = random.choice(self._vehicles)
            speed = round(random.uniform(60.0, 120.0), 1)
            fuel = round(random.uniform(15.0, 95.0), 1)
            temp = round(random.uniform(85.0, 105.0), 1)

            event = TelemetryReceivedEvent(
                vehicle_id=vehicle,
                speed=speed,
                fuel_level=fuel,
                temperature=temp
            )
            self.bus.publish(event)
            await asyncio.sleep(self.interval)