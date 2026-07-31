import sys
import os
from pathlib import Path

# Agregar la raíz del proyecto al sys.path para evitar ModuleNotFoundError
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cProfile
import pstats
import io
import time
from core.event_bus import EventBus
from core.events import TelemetryReceivedEvent, AlertRaisedEvent
from core.state import StateStore


def run_benchmark(iterations: int = 50_000):
    """Ejecuta una ráfaga masiva de eventos para medir tiempo y rendimiento de memoria/CPU."""
    bus = EventBus()
    store = StateStore(bus=bus)

    print(f"🚀 Iniciando benchmark con {iterations:,} publicaciones de eventos...")
    start_time = time.perf_counter()

    for i in range(iterations):
        if i % 2 == 0:
            bus.publish(TelemetryReceivedEvent(
                vehicle_id=f"VEH-{(i % 100):03d}",
                speed=80.0 + (i % 20),
                fuel_level=50.0,
                temperature=90.0
            ))
        else:
            bus.publish(AlertRaisedEvent(
                alert_id=f"ALT-{i:05d}",
                severity="WARNING" if i % 4 == 0 else "INFO",
                message="Evento de prueba para profiling",
                source_name="Profiler"
            ))

    elapsed = time.perf_counter() - start_time
    ops_per_sec = iterations / elapsed if elapsed > 0 else 0
    print(f"✅ Procesados {iterations:,} eventos en {elapsed:.4f}s ({ops_per_sec:,.2f} ops/sec)")


def main():
    profiler = cProfile.Profile()
    profiler.enable()

    run_benchmark(iterations=50_000)

    profiler.disable()

    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats(pstats.SortKey.CUMULATIVE)
    ps.print_stats(15)

    print("\n" + "=" * 50)
    print("📊 REPORTE DE PROFILING (Top 15 funciones de mayor impacto)")
    print("=" * 50)
    print(s.getvalue())


if __name__ == "__main__":
    main()