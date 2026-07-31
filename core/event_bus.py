import logging
import weakref
from collections import defaultdict
from typing import Callable, Dict, Type, List
from core.events import Event

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class EventBus:
    """Bus de eventos pub/sub en memoria con manejo de referencias débiles para evitar fugas."""

    def __init__(self) -> None:
        # Mapea tipo de Evento -> Lista de referencias débiles a manejadores (handlers)
        self._listeners: Dict[Type[Event], List[weakref.WeakMethod]] = defaultdict(list)

    def subscribe(self, event_type: Type[Event], handler: Callable[[Event], None]) -> None:
        """Suscribe un manejador a un tipo específico de evento."""
        if hasattr(handler, "__self__"):
            # Es un método ligado a un objeto instanciado -> usamos WeakMethod
            ref = weakref.WeakMethod(handler, lambda r: self._cleanup(event_type, r))
        else:
            # Es una función independiente o estática
            ref = handler

        if ref not in self._listeners[event_type]:
            self._listeners[event_type].append(ref)
            logging.debug(f"[BUS] Suscripción registrada para {event_type.__name__}")

    def unsubscribe(self, event_type: Type[Event], handler: Callable[[Event], None]) -> None:
        """Desuscribe un manejador explícitamente."""
        listeners = self._listeners[event_type]
        self._listeners[event_type] = [
            ref for ref in listeners
            if (isinstance(ref, weakref.WeakMethod) and ref() != handler) or ref != handler
        ]
        logging.debug(f"[BUS] Desuscripción completada para {event_type.__name__}")

    def publish(self, event: Event) -> None:
        """Publica un evento y notifica a todos los suscriptores registrados."""
        event_type = type(event)
        listeners = self._listeners.get(event_type, [])
        active_listeners = []

        for ref in listeners:
            handler = ref() if isinstance(ref, weakref.WeakMethod) else ref
            if handler is not None:
                active_listeners.append(ref)
                try:
                    handler(event)
                except Exception as e:
                    logging.error(f"[BUS] Error al procesar handler en {event_type.__name__}: {e}")

        # Mantener solo escuchas activos (limpieza automática)
        self._listeners[event_type] = active_listeners

    def _cleanup(self, event_type: Type[Event], ref: weakref.WeakMethod) -> None:
        """Limpia referencias muertas de la lista de suscriptores."""
        if ref in self._listeners[event_type]:
            self._listeners[event_type].remove(ref)


# Instancia global (Singleton opcional o inyectable)
default_bus = EventBus()