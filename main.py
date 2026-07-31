import asyncio
import logging
from core.events import TelemetryReceivedEvent, AlertRaisedEvent, HeartbeatEvent
from core.event_bus import default_bus
from core.loop import EngineLoop
from sources.heartbeat import HeartbeatSource
from sources.telemetry_file import TelemetryFileSource
from sources.alerts_api import AlertsApiSource

# Configuración de logs con formato limpio
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)


# Handlers (Manejadores de eventos suscritos al bus)
def on_telemetry(event: TelemetryReceivedEvent) -> None:
    logging.info(
        f"[UI-TELEMETRIA] {event.vehicle_id} ➔ Vel: {event.speed} km/h | "
        f"Fuel: {event.fuel_level}% | Temp: {event.temperature}°C"
    )


def on_alert(event: AlertRaisedEvent) -> None:
    logging.info(f"[UI-ALERTAS] [{event.severity}] {event.alert_id}: {event.message} ({event.source_name})")


def on_heartbeat(event: HeartbeatEvent) -> None:
    logging.info(f"[UI-STATUS] Heartbeat #{event.sequence} recibido - Estado: {event.system_status}")


async def main() -> None:
    engine = EngineLoop()

    # 1. Suscribir los handlers al EventBus (Totalmente desacoplado)
    default_bus.subscribe(TelemetryReceivedEvent, on_telemetry)
    default_bus.subscribe(AlertRaisedEvent, on_alert)
    default_bus.subscribe(HeartbeatEvent, on_heartbeat)

    # 2. Instanciar las fuentes Pub/Sub
    hb_source = HeartbeatSource(interval=1.0)
    telemetry_source = TelemetryFileSource(interval=1.2)
    alerts_source = AlertsApiSource(interval=2.0)

    # 3. Arrancar el Event Loop
    await engine.start()

    # 4. Registrar la ejecución de las fuentes como tareas en el loop
    engine.create_task(hb_source.start())
    engine.create_task(telemetry_source.start())
    engine.create_task(alerts_source.start())

    # Simular ejecución activa durante 4.5 segundos
    await asyncio.sleep(4.5)

    # 5. Apagado limpio de fuentes y del motor
    logging.info("Deteniendo fuentes de datos asíncronas...")
    await hb_source.stop()
    await telemetry_source.stop()
    await alerts_source.stop()
    await engine.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Programa interrumpido manualmente por el usuario.")