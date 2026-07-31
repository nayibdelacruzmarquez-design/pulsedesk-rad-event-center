import threading
from typing import Dict, Any
from core.events import StateChangedEvent, TelemetryReceivedEvent, AlertRaisedEvent
from core.event_bus import EventBus, default_bus


class StateStore:
    """Almacén de estado global thread-safe para la aplicación."""

    def __init__(self, bus: EventBus = default_bus) -> None:
        self.bus: EventBus = bus
        self._lock = threading.Lock()
        self._state: Dict[str, Any] = {
            "vehicles": {},
            "alerts_summary": {"total": 0, "critical": 0, "warning": 0, "info": 0}
        }

        # Suscribirse automáticamente a los eventos de interés
        self.bus.subscribe(TelemetryReceivedEvent, self._on_telemetry)
        self.bus.subscribe(AlertRaisedEvent, self._on_alert)

    def set(self, key: str, value: Any) -> None:
        """Actualiza una clave de manera thread-safe y emite evento de cambio."""
        with self._lock:
            old_value = self._state.get(key)
            self._state[key] = value

        # Emitir cambio de estado fuera del lock para evitar deadlocks
        self.bus.publish(StateChangedEvent(key=key, old_value=old_value, new_value=value))

    def get(self, key: str, default: Any = None) -> Any:
        """Obtiene un valor del estado de manera thread-safe."""
        with self._lock:
            return self._state.get(key, default)

    def _on_telemetry(self, event: TelemetryReceivedEvent) -> None:
        with self._lock:
            vehicles = dict(self._state.get("vehicles", {}))
            vehicles[event.vehicle_id] = {
                "speed": event.speed,
                "fuel_level": event.fuel_level,
                "temperature": event.temperature,
                "last_update": event.timestamp
            }
            self._state["vehicles"] = vehicles

    def _on_alert(self, event: AlertRaisedEvent) -> None:
        with self._lock:
            summary = dict(self._state.get("alerts_summary", {}))
            summary["total"] += 1
            severity_key = event.severity.lower()
            if severity_key in summary:
                summary[severity_key] += 1
            self._state["alerts_summary"] = summary