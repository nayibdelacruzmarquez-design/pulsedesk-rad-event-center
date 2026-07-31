import asyncio
from core.events import HeartbeatEvent
from sources.base import BaseSource


class HeartbeatSource(BaseSource):
    """Fuente periódica que emite HeartbeatEvent cada N segundos."""

    def __init__(self, interval: float = 1.0, **kwargs) -> None:
        super().__init__(name="HeartbeatSource", **kwargs)
        self.interval: float = interval
        self._sequence: int = 0

    async def start(self) -> None:
        await super().start()
        while self.is_running:
            self._sequence += 1
            event = HeartbeatEvent(sequence=self._sequence)
            self.bus.publish(event)
            await asyncio.sleep(self.interval)