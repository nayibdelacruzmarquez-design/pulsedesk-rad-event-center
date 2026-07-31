import asyncio
import logging
import signal
import sys
from typing import Set

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)


class EngineLoop:
    """Gestor del ciclo de vida del Event Loop principal y tareas asíncronas."""

    def __init__(self) -> None:
        self.is_running: bool = False
        self._tasks: Set[asyncio.Task] = set()

    def create_task(self, coro) -> asyncio.Task:
        """Crea y registra una tarea asíncrona rastreada por el loop."""
        task = asyncio.create_task(coro)
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        return task

    async def start(self) -> None:
        """Inicia el Event Loop de la aplicación."""
        logging.info("⚡ Iniciando Event Loop de PulseDesk...")
        self.is_running = True

    async def stop(self) -> None:
        """Realiza un apagado limpio (Graceful Shutdown) cancelando tareas pendientes."""
        if not self.is_running:
            return

        logging.info("🛑 Iniciando apagado limpio (Graceful Shutdown)...")
        self.is_running = False

        # Cancelar tareas pendientes activas
        pending_tasks = [t for t in self._tasks if not t.done()]
        if pending_tasks:
            logging.info(f"Cancelando {len(pending_tasks)} tarea(s) asíncrona(s) activa(s)...")
            for task in pending_tasks:
                task.cancel()
            await asyncio.gather(*pending_tasks, return_exceptions=True)

        logging.info("✅ Apagado completado exitosamente. Recurso liberados.")