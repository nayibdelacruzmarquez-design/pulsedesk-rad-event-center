import asyncio
import pytest
from core.loop import EngineLoop


@pytest.mark.asyncio
async def test_engine_loop_lifecycle():
    engine = EngineLoop()
    assert engine.is_running is False

    await engine.start()
    assert engine.is_running is True

    await engine.stop()
    assert engine.is_running is False


@pytest.mark.asyncio
async def test_engine_loop_task_cancellation():
    engine = EngineLoop()
    await engine.start()

    async def dummy_task():
        await asyncio.sleep(10)

    task = engine.create_task(dummy_task())
    assert not task.done()

    # Graceful shutdown debe cancelar la tarea pendiente
    await engine.stop()
    assert task.cancelled() or task.done()