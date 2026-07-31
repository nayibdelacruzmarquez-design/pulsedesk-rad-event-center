import gc
import pytest
from core.event_bus import EventBus
from core.events import HeartbeatEvent


class MockSubscriber:
    def __init__(self):
        self.received = False

    def on_heartbeat(self, event: HeartbeatEvent):
        self.received = True


def test_event_bus_publish_subscribe():
    bus = EventBus()
    sub = MockSubscriber()

    bus.subscribe(HeartbeatEvent, sub.on_heartbeat)
    bus.publish(HeartbeatEvent(sequence=1))

    assert sub.received is True


def test_zero_leaks_weakref_cleanup():
    """Prueba que los listeners destruidos no retengan memoria (Insignia Zero Leaks)."""
    bus = EventBus()
    sub = MockSubscriber()

    bus.subscribe(HeartbeatEvent, sub.on_heartbeat)

    # Destruir la instancia del suscriptor
    del sub
    gc.collect()

    # Publicar evento post-destrucción
    bus.publish(HeartbeatEvent(sequence=2))

    # Verificar que el bus limpió el handler muerto
    assert len(bus._listeners[HeartbeatEvent]) == 0