import asyncio
import threading
import logging
from core.loop import EngineLoop
from core.state import StateStore
from sources.heartbeat import HeartbeatSource
from sources.telemetry_file import TelemetryFileSource
from sources.alerts_api import AlertsApiSource
from ui.app import PulseDeskApp
from ui.bridge import UIBridge

# Configuración básica de logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def run_async_engine(loop: asyncio.AbstractEventLoop, engine: EngineLoop):
    """Ejecuta el loop asíncrono en un hilo secundario para no congelar la GUI."""
    asyncio.set_event_loop(loop)

    hb_source = HeartbeatSource(interval=1.0)
    telemetry_source = TelemetryFileSource(interval=1.5)
    alerts_source = AlertsApiSource(interval=2.5)

    async def start_sources():
        await engine.start()
        engine.create_task(hb_source.start())
        engine.create_task(telemetry_source.start())
        engine.create_task(alerts_source.start())

    loop.run_until_complete(start_sources())
    loop.run_forever()


def main():
    logging.info("🚀 Iniciando PULSEDESK RAD Control Center...")

    # 1. Instanciar el estado y la interfaz gráfica
    state_store = StateStore()
    app = PulseDeskApp()
    bridge = UIBridge(app)

    # 2. Crear y arrancar el Event Loop asíncrono en un hilo secundario (background)
    async_loop = asyncio.new_event_loop()
    engine = EngineLoop()

    engine_thread = threading.Thread(
        target=run_async_engine,
        args=(async_loop, engine),
        daemon=True
    )
    engine_thread.start()

    # 3. Arrancar la ventana visual en el hilo principal
    try:
        app.mainloop()
    finally:
        logging.info("🛑 Cerrando aplicación y deteniendo tareas asíncronas...")
        async_loop.call_soon_threadsafe(async_loop.stop)


if __name__ == "__main__":
    main()