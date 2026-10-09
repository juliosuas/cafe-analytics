# Verificación de la entrega

Fecha: 3 de octubre de 2026. Entorno real: macOS-15.7.4-arm64-arm-64bit; Python 3.12.14; CPUExecutionProvider, 4 hilos. No se usó GPU.

## Ejecución completa con video público

- Video real: Suika Chan / Pexels 10901926. Fuente y licencia en `SOURCES.md`.
- Modelo oficial YOLOX-S, inferencia ONNX real, sin detecciones simuladas.
- Fotogramas procesados: **341 de 341**.
- Duración del video: **11.3667 s**.
- Tiempo del bucle de procesamiento: **36.24 s**.
- Velocidad media: **9.41 FPS**. Excluye inicialización del modelo, conversión final H.264 y escritura final del reporte; no es una promesa de tiempo real.
- IDs confirmados: **30**; no se afirma que sean personas únicas reales.
- Muestras de trayectorias: **5002**.
- Cruces de la línea virtual: **1 entrada, 0 salidas**; no es una puerta real.
- Video generado: **H.264, 960 × 540, 30 FPS, 341 fotogramas**, sin audio.
- Ejecución final completa con `python -W error`; terminó sin advertencias ni excepciones.

## Pruebas e integridad

**12 pruebas aprobadas** con `pytest -q -W error`:

1. Tiempos basados en observación y exclusión de huecos largos.
2. Cruces en ambos sentidos e histéresis frente a oscilación.
3. Cruces de la prolongación fuera del segmento no se cuentan.
4. Reaparición tras pérdida no genera un cruce ficticio.
5. Métricas vacías sin personas.
6. Cierre de visitas al salir de una zona.
7. Rechazo de coordenadas inválidas y polígonos cruzados.
8. Persistencia de ID ante oclusión corta y detección de baja confianza; nuevo ID tras expiración.
9. Detección débil no crea IDs nuevos.
10. El orden de las detecciones no cambia la asignación de IDs.
11. Detector real encuentra personas en el video y ninguna en imagen negra.
12. Rama webcam con seis frames de video real como cámara simulada, FPS desconocidos, timestamps monotónicos y exportación MP4V sin FFmpeg. No abre una cámara física.

`python scripts/verify_run.py runs/demo` aprobó: decodificación completa de los 341 frames de salida, correspondencia entre IDs, CSV/JSON y eventos, permanencias no negativas, e igualdad entre persona-segundos observados y heatmap (176.033333). Evidencia estructurada en `runs/demo/verification.json`.

Instalación editable `pip install -e '.[test]'` y comando `cafe-analytics --help` comprobados. Descargador ejecutado con assets presentes: ambos SHA256 correctos. Los archivos originales se descargaron de las URLs públicas documentadas durante esta sesión.

## Navegador

- Reporte abierto y revisado visualmente en navegador integrado.
- Reproductor: readyState 4, duración 11.366667 s, ancho 960, sin error de medio.
- Editor: imagen cargada; dibujo y guardado de un polígono; línea de acceso e inversión de dirección.
- Descarga `zonas.json` efectuada desde el editor y validada posteriormente por `validate_config`: una zona, un acceso y dirección invertida correcta.

## Límites de lo verificado

No se ejecutó en Ubuntu ni con una webcam física. No se midieron precisión, recall, ID switches, error de aforo o dwell contra anotaciones humanas. La demo tiene oclusiones y recortes de cuerpos. La prueba de funcionamiento no certifica exactitud comercial. Para un piloto, fijar la cámara, definir accesos reales y comparar manualmente cruces y permanencias durante una muestra representativa.
