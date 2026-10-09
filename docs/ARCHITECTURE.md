# Arquitectura

## Alcance

Aplicación Python de una sola fuente por proceso. Se ejecuta en CPU. No hay backend, cuentas, base de datos remota, entrenamiento, reconocimiento de identidad ni infraestructura cloud obligatoria. El HTML publicado es una demo estática de datos públicos; no recibe video del usuario.

| Módulo | Responsabilidad |
|---|---|
| `detector.py` | Cargar ONNX, letterbox BGR 640×640, clase persona, decodificación y NMS |
| `tracker.py` | Estado de movimiento, filtro Kalman, asociación húngara en dos pasadas |
| `analytics.py` | Geometría normalizada, visitas, permanencia, líneas, eventos y heatmap |
| `cli.py` | Captura, timestamps, orquestación, video y cierre de recursos |
| `report.py` | CSV/JSON, mapas y HTML independiente |
| `editor.py` | Primer fotograma incrustado en editor local y descarga de configuración |

## Identidad y seguimiento

El estado de Kalman guarda centro, tamaño y sus velocidades. La asociación combina IoU y distancia al centro; descarta candidatos distantes antes de resolver la asignación. La primera pasada usa detecciones ≥0.4; una segunda pasada acepta detecciones ≥0.12 solo para pistas confirmadas. Son umbrales configurables, no resultados de calibración para todas las tiendas.

Un ID se confirma al acumular tres detecciones. Persiste durante una ausencia de hasta un segundo; luego se crea un ID nuevo. Solo detecciones medidas y confirmadas alimentan métricas: las predicciones del filtro no se cuentan como personas vistas. No hay embeddings de apariencia, reidentificación entre cámaras ni memoria entre ejecuciones.

## Tiempo y contabilidad

Archivos: timestamps del contenedor; si no avanzan o no son finitos, incremento por FPS y marca `fps_fallback`. Webcam: reloj monotónico de captura. Los timestamps son relativos a la ejecución, no horas locales de negocio. La agregación futura necesitará inicio absoluto y zona horaria explícita.

La analítica admite continuidad de hasta 0.5 s. Suma el intervalo cuando el ID sigue dentro de la misma zona; excluye el intervalo incierto de cambio de zona. No atribuye tiempo después de perder la pista ni añade una cola ficticia al final. Se marcan visitas censuradas por fin de sesión u oclusión.

## Cruces

Cada línea tiene dos extremos y sentido de entrada. Se guarda el último lado estable fuera de la banda de histéresis. Un cambio de lado solo cuenta si la trayectoria intersecta el segmento finito. Se restablece el estado tras un hueco largo; reaparecer no genera un cruce. Una persona puede cruzar varias veces, y cada cruce se registra.

## Heatmap

Matriz 90×160. Cada intervalo continuo suma persona-segundos en el ancla observada. Su suma coincide con el tiempo observado de todas las pistas. El mapa mostrado se suaviza y normaliza por sesión; no es un plano métrico del suelo ni una escala comparable por color entre días.

## Decisiones de implementación

- **ONNX en CPU:** instalación pequeña y portable; rendimiento acelerado queda para medir después.
- **Tracking geométrico propio:** dependencias permisivas y sin biometría; oclusiones densas pueden intercambiar IDs.
- **CSV/JSON:** permite inspección y futuras integraciones; no ofrece consultas multiusuario o retención automática.
- **HTML estático:** abre localmente; no autentica accesos ni ofrece datos en vivo.
- **Modelos fuera de Git:** descarga oficial con SHA256; evita versiones binarias grandes en la historia.
- **Demo separada:** solo material público documentado se publica en `docs/`; videos propios y ejecuciones se ignoran en Git.

## Límites operativos actuales

El MP4 se escribe a FPS nominales aunque webcam o video VFR tenga otra cadencia efectiva. La analítica conserva sus timestamps, pero reproducción y tiempo real pueden divergir. No hay recuperación después de reinicios, RTSP supervisado, tolerancia a cambios de encuadre, colas de tareas o modo multitienda. Un corte de lectura no se diagnostica todavía como fallo de cámara frente a fin de fuente. Antes de operación desatendida, implementar salud de captura y sesiones durables.

## Resumen orientado al dueño (0.1.1)

`owner.SessionEvidence` conserva contadores por zona y el primer fotograma de cada máximo, con memoria constante por zona. La CLI escribe `occupancy.csv` incrementalmente para cada fotograma, incluyendo ocupación cero. `owner.build_brief` verifica correspondencia de frames y picos, conserva las métricas observadas y añade preguntas de revisión mediante reglas fijas. No utiliza un LLM ni decide causas, ventas o dotación de personal.

`owner.html` y `owner-summary.json` son adicionales al reporte técnico. Los enlaces de video se calculan por índice de fotograma / FPS de salida, para no confundir tiempo de captura de webcam con tiempo de reproducción. No se calcula cobertura de una jornada sin timestamps absolutos y salud de cámara. [Contrato de datos](DATA_MODEL.md).
