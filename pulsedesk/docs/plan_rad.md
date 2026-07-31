# PLAN RAD — PULSEDESK
**Centro de Control de Eventos en Tiempo Real**  
*Diplomado: Certificación Especialista en Desarrollo de Software con Python SSR*

---

## 1. Alcance y Priorización (Matriz MoSCoW)

### 🔴 Must Have (Obligatorio para aprobación)
- **Bus de eventos propio** en memoria, asíncrono y desacoplado (pub/sub).
- **Event Loop** robusto con soporte para Graceful Shutdown sin trazas de error.
- **Fuentes de datos asíncronas**: archivo de telemetría (tailing), API de alertas simulada y Heartbeat.
- **Interfaz Gráfica (GUI)** responsiva que nunca se bloquee ni supere los 16 ms por frame.
- **Store de Estado** unificado y thread-safe.
- **Suite de pruebas automatizadas** (mínimo 15 pruebas con `pytest` y `pytest-asyncio`).
- **Script de Profiling** antes y después de la optimización del cuello de botella.

### 🟡 Should Have (Deseable de alto valor)
- Indicadores visuales de estado por color para fuentes desconectadas o con fallos.
- Ejecutor en hilo secundario (`run_in_executor`) para tareas con carga intensiva de CPU.
- Registro estructurado de logs (logging) con marcas de tiempo relativas.

### 🟢 Could Have (Si el timebox lo permite)
- Exportación de logs a formato JSON.
- Personalización de temas visuales en la interfaz gráfica.

### ⚪ Won't Have (Fuera de alcance — Espiral Futura)
- Persistencia en base de datos SQL o NoSQL.
- Integración con brokers externos de mensajería (RabbitMQ / Kafka).
- Autenticación de usuarios o roles.

---

## 2. Cronograma de Timeboxes (9 Lecciones)

| Timebox | Fase | Objetivo Principal | Entregable Clave | Criterio de "Hecho" (Definition of Done) |
| :---: | :--- | :--- | :--- | :--- |
| **TB1** | Requisitos y Plan | Congelar alcance y definir matriz MoSCoW. | `docs/plan_rad.md` | Plan documentado y aprobado en el repositorio. |
| **TB2** | Modelo de Eventos | Diseñar catálogo de eventos tipados. | `core/events.py` | Dataclasses inmutables definidas con payload claro. |
| **TB3** | Event Loop Base | Gestionar ciclo de vida y apagado limpio. | `core/loop.py` | App inicia, emite latido y apaga con Ctrl+C sin warnings. |
| **TB4** | Prototipo Visual | Crear interfaz gráfica base en framework RAD. | `ui/app.py` | Ventana renderizada conectada a un evento simulado. |
| **TB5** | Bus de Eventos | Implementar patrón Pub/Sub con refs débiles. | `core/event_bus.py` | Pruebas pasando; sin fugas de memoria por handlers. |
| **TB6** | Fuentes Pub/Sub | Crear adaptadores de telemetría y alertas. | `sources/` | Nueva fuente agregada sin modificar código de `ui/`. |
| **TB7** | Estado y Concurrencia | Aislar tareas pesadas en threads/executors. | `core/state.py` | UI fluida sin congelamientos ante carga pesada. |
| **TB8** | Testing & Profiling | Validar cobertura y medir rendimiento. | `tests/`, `tools/` | $\ge 15$ pruebas en verde y reporte de optimización. |
| **TB9** | Empaquetado & Demo | Consolidar entrega, ejecutable y documentación. | `pyproject.toml`, `README.md` | Aplicación ejecutable mediante un solo comando. |
| **TB9** | Empaquetado & Demo | Consolidar entrega, ejecutable y documentación. | `pyproject.toml`, `README.md` | Aplicación ejecutable mediante un solo comando. |