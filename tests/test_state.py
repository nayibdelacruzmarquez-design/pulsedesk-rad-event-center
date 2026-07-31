import pytest
from core.state import StateStore
from core.events import TelemetryReceivedEvent, AlertRaisedEvent
from core.event_bus import EventBus


def test_state_store_updates_telemetry():
    bus = EventBus()
    store = StateStore(bus=bus)

    event = TelemetryReceivedEvent(vehicle_id="VEH-99", speed=100.0, fuel_level=50.0, temperature=90.0)
    bus.publish(event)

    vehicles = store.get("vehicles")
    assert "VEH-99" in vehicles
    assert vehicles["VEH-99"]["speed"] == 100.0


def test_state_store_alerts_summary():
    bus = EventBus()
    store = StateStore(bus=bus)

    event = AlertRaisedEvent(alert_id="ALT-1", severity="CRITICAL", message="Error grave", source_name="test")
    bus.publish(event)

    summary = store.get("alerts_summary")
    assert summary["total"] == 1
    assert summary["critical"] == 1