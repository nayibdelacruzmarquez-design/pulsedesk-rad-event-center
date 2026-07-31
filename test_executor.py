import asyncio
import logging
from workers.executor import run_cpu_bound_task

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


async def async_counter():
    """Demuestra que el Event Loop sigue respondiendo mientras el worker procesa en background."""
    for i in range(1, 4):
        logging.info(f"⏳ [EVENT LOOP] El bucle principal sigue activo... ({i}s)")
        await asyncio.sleep(0.5)


async def main():
    logging.info("🚀 Iniciando prueba de concurrencia con Executor...")
    # Ejecutamos la tarea pesada en thread executor y el contador en el loop simultáneamente
    await asyncio.gather(
        run_cpu_bound_task(data_points=5_000_000),
        async_counter()
    )

if __name__ == "__main__":
    asyncio.run(main())