import asyncio
from abc import ABC, abstractmethod
from core.event_bus import EventBus, default_bus


class BaseSource(ABC):
    """Interfaz base para todas las fuentes de datos asíncronas."""

    def __init__(self, name: str, bus: EventBus = default_bus) -> None:
        self.name: str = name
        self.bus: EventBus = bus
        self.is_running: bool = False

    @abstractmethod
    async def start(self) -> None:
        """Inicia el consumo/generación de eventos."""
        self.is_running = True

    async def stop(self) -> None:
        """Detiene la fuente de datos."""
        self.is_running = False