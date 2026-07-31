from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True, kw_only=True)
class Event:
    """Clase base inmutable para todos los eventos del sistema."""
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True, kw_only=True)
class TelemetryReceivedEvent(Event):
    """Evento emitido cuando la fuente de telemetría lee datos de vehículos."""
    vehicle_id: str
    speed: float
    fuel_level: float
    temperature: float


@dataclass(frozen=True, kw_only=True)
class AlertRaisedEvent(Event):
    """Evento emitido cuando se detecta una condición crítica o de advertencia."""
    alert_id: str
    severity: str  # 'INFO', 'WARNING', 'CRITICAL'
    message: str
    source_name: str


@dataclass(frozen=True, kw_only=True)
class SourceFailedEvent(Event):
    """Evento emitido cuando una fuente de datos sufre una desconexión o fallo."""
    source_name: str
    error_message: str


@dataclass(frozen=True, kw_only=True)
class StateChangedEvent(Event):
    """Evento emitido cuando cambia una clave en el store de estado global."""
    key: str
    old_value: Any
    new_value: Any


@dataclass(frozen=True, kw_only=True)
class HeartbeatEvent(Event):
    """Evento periódico para monitorear el estado del Event Loop."""
    sequence: int
    system_status: str = "OPERATIONAL"


@dataclass(frozen=True, kw_only=True)
class ShutdownRequestedEvent(Event):
    """Evento emitido para solicitar el apagado limpio del sistema."""
    reason: str = "User initiated shutdown"