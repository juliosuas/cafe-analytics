# Validación técnica y de negocio

## Reproducir una ejecución

```bash
python -m pip install -e '.[test]'
python scripts/download_assets.py
python -m pytest -q -W error
cafe-analytics run --source assets/retail.mp4 --config configs/demo.json --output runs/validation
python scripts/verify_run.py runs/validation
```

Los assets deben existir para que las pruebas de inferencia real se ejecuten. No confundas “10 pasaron, 2 omitidas” con una prueba del modelo. La webcam física no se abre en tests: se sustituye por seis frames de archivo y se mantiene el detector real.

## Qué demuestra cada nivel

| Nivel | Evidencia | No demuestra |
|---|---|---|
| Unitario | Tiempos, geometría, direcciones e IDs en casos controlados | Exactitud en una tienda real |
| Integración | ONNX detecta personas, exportación y contratos consistentes | Robustez de cámara/IP en producción |
| Demo completa | Archivo real procesado y video íntegro | Calidad de decisiones comerciales |
| Piloto de campo (pendiente) | Comparación contra etiquetas humanas | Causalidad de mejoras del negocio |

## Protocolo de piloto

1. Definir una pregunta y las métricas relacionadas antes de ajustar umbrales.
2. Confirmar permisos del video, cámara fija, campo de visión y accesos incluidos.
3. Separar muestras de calibración y validación con períodos de distinta actividad.
4. Anotar manualmente cruces por dirección; emparejar eventos con tolerancia temporal acordada.
5. Medir precisión, recall y error absoluto de conteo por período; no solo el total del día.
6. Revisar fragmentación/intercambio de IDs y errores de permanencia por zona.
7. Registrar oclusiones, iluminación, cambios de encuadre y cobertura temporal.
8. Acordar tolerancias y decidir si el sistema puede apoyar la pregunta seleccionada.

Para evaluar **espera**, anotar inicio de fila e inicio de atención de forma independiente. Para evaluar **conversión**, acordar acceso, denominador y conciliación con POS. No obtener ambas etiquetas solamente de la permanencia.

## Rendimiento

Registrar hardware, SO, Python, proveedor, hilos, tamaño de fuente, duración y `processing_seconds`. `processing_fps` no incluye carga del modelo ni posproducción; informar latencia total por separado si se usa para operación en vivo. Comparar el mismo clip/modelo/configuración.

La referencia local histórica es 9.41 FPS sobre el clip de 341 frames. Consultar [VERIFICATION.md](../VERIFICATION.md) para las ejecuciones y pruebas efectivamente realizadas; los objetivos del roadmap son futuros.
