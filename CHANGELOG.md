# Changelog

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
