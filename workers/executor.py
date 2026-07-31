import asyncio
import time
import logging
from concurrent.futures import ThreadPoolExecutor

executor_pool = ThreadPoolExecutor(max_workers=2)


def heavy_cpu_calculation(data_points: int) -> float:
    """Función bloqueante que simula procesamiento pesado de CPU (ej. cálculo estadístico)."""
    logging.info(f" [WORKER] Iniciando procesamiento pesado con {data_points} datos...")
    start_time = time.perf_counter()

    # Simulación de cálculo pesado
    total = sum(i * i for i in range(data_points))

    elapsed = time.perf_counter() - start_time
    logging.info(f" [WORKER] Cálculo completado en {elapsed:.4f}s - Resultado: {total}")
    return elapsed


async def run_cpu_bound_task(data_points: int = 10_000_000) -> float:
    """Delega la ejecución de la función bloqueante al ThreadPoolExecutor."""
    loop = asyncio.get_running_loop()
    # run_in_executor evita bloquear el Event Loop principal
    result = await loop.run_in_executor(executor_pool, heavy_cpu_calculation, data_points)
    return result