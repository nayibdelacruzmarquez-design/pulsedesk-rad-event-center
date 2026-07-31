import asyncio
import logging
from core.events import HeartbeatEvent
from core.loop import EngineLoop


async def heartbeat_worker(engine: EngineLoop) -> None:
    """Worker temporal para probar el ciclo de vida emitiendo un latido."""
    seq = 1
    while engine.is_running:
        event = HeartbeatEvent(sequence=seq)
        logging.info(f"[HEARTBEAT] Secuencia #{event.sequence} - Estado: {event.system_status}")
        seq += 1
        await asyncio.sleep(1)


async def main() -> None:
    engine = EngineLoop()
    await engine.start()

    # Crear tarea en el loop
    engine.create_task(heartbeat_worker(engine))

    # Simular ejecución de 3 segundos y apagar
    await asyncio.sleep(3.2)
    await engine.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Programa interrumpido por el usuario.")