import asyncio
import random
from core.events import AlertRaisedEvent
from sources.base import BaseSource


class AlertsApiSource(BaseSource):
    """Fuente que simula la recepción de alertas remotas con latencia."""

    def __init__(self, interval: float = 2.5, **kwargs) -> None:
        super().__init__(name="AlertsApiSource", **kwargs)
        self.interval: float = interval
        self._alert_count = 0
        self._severities = ["INFO", "WARNING", "CRITICAL"]
        self._messages = [
            "Presión de neumáticos baja",
            "Nivel de combustible en reserva",
            "Freno con desgaste elevado",
            "Temperatura de motor por encima del umbral"
        ]

    async def start(self) -> None:
        await super().start()
        while self.is_running:
            self._alert_count += 1
            severity = random.choice(self._severities)
            msg = random.choice(self._messages)

            event = AlertRaisedEvent(
                alert_id=f"ALT-{self._alert_count:04d}",
                severity=severity,
                message=msg,
                source_name=self.name
            )
            self.bus.publish(event)
            await asyncio.sleep(self.interval)