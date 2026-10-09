# Changelog

## Curaduría de videos — 2026-10-09

- Cuatro referencias de operación e inspección: huevos, cafetería, preparación de tacos y limones.
- Fuentes atribuidas, tecnología indicada por caso, reproductores externos y enlaces de respaldo.
- Demo de cafetería identificada como republicación y sin atribución a Decisions.

## Documentación y web — 2026-10-09

- Diseño técnico y viabilidad comercial de Decisions con GPT-6 Luna, sin integración ejecutada.
- Sección de oportunidades en la web, con estado propuesto y dos videos externos atribuidos.
- Se mantiene el motor local y la demo principal de tres negocios.


## 0.1.1 — 2026-10-08

- Demo reproducible de cafetería de barra: Ron Lach / Pexels 8430969, 36 s, 900 fotogramas, zonas de imagen y accesos no disponibles.
- Filtro opcional `min_person_height` calibrado para excluir figuras pequeñas del fondo en la demo; desactivado por defecto y registrado en el resumen.
- Ocupación por zona por fotograma en `occupancy.csv`, incluyendo ceros.
- Resumen determinista `owner-summary.json` / `owner.html`, hechos, límites y enlaces al primer pico observado. Webcam enlaza según fotograma de reproducción.
- Página pública orientada al dueño, con selector de seis giros e hipótesis explícitas; GitHub concentra instalación, arquitectura, evidencia y backlog.
- Tests de evidencia, ausencia de datos, escape HTML y tiempos de reproducción; verificador ampliado para los nuevos archivos.
- Continúan pendientes la validación comercial, espera real, roles, monitoreo desatendido y reportes diarios remotos.

## 0.1.0 — 2026-10-08

Primera publicación pública del MVP local construido y probado inicialmente el 3 de octubre de 2026.

### Disponible

- Detección de personas con YOLOX-S ONNX en CPU.
- Tracking geométrico por sesión, zonas configurables y conteos de cruce.
- Permanencia observada, visitas parciales, trayectorias y heatmap.
- Video MP4, CSV/JSON, reporte HTML y editor visual local.
- Fuente y licencia de demo documentadas, descargas verificadas por SHA256.
- Documentación orientada al dueño, arquitectura, contrato de datos, privacidad y validación.
- Demo pública con video, GIF e imágenes de resultados reales.
- GitHub Actions: 12 pruebas y pipeline completo de 341 frames aprobados en Ubuntu 24.04 y macOS 14 arm64.

### Límites conocidos

Los IDs pueden fragmentarse/intercambiarse con oclusiones. La captura webcam es opcional y no se verificó con hardware físico en la entrega inicial. El MP4 de webcam se escribe a FPS nominales. No hay monitoreo desatendido, alertas remotas, comparaciones diarias, POS ni métricas de espera validadas. Véase el roadmap.

### Presentación de video y próxima capacidad

La portada incorpora el reproductor original de una sesión de Artisti Coffee Roasters (29:09) como referencia de operación real. Se separa explícitamente de la demo procesada del MVP. Tazas preparadas/entregadas/retiradas quedan documentadas como capacidad pendiente; no se muestran conteos ficticios.
