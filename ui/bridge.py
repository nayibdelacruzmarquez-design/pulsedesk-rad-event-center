from core.event_bus import default_bus
from core.events import TelemetryReceivedEvent, AlertRaisedEvent
from ui.app import PulseDeskApp


class UIBridge:
    """Puente desacoplado entre el EventBus y la Interfaz Gráfica."""

    def __init__(self, app: PulseDeskApp) -> None:
        self.app = app
        # Suscribir los métodos de actualización de la UI al bus
        default_bus.subscribe(TelemetryReceivedEvent, self._handle_telemetry)
        default_bus.subscribe(AlertRaisedEvent, self._handle_alert)

    def _handle_telemetry(self, event: TelemetryReceivedEvent) -> None:
        msg = f"{event.vehicle_id} | Vel: {event.speed} km/h | Fuel: {event.fuel_level}% | Temp: {event.temperature}°C"
        # Programar la actualización en el hilo principal de la UI de forma thread-safe
        self.app.after(0, lambda: self.app.update_telemetry(msg))

    def _handle_alert(self, event: AlertRaisedEvent) -> None:
        msg = f"[{event.severity}] {event.alert_id}: {event.message}"
        self.app.after(0, lambda: self.app.update_alerts(msg))