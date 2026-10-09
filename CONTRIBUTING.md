# Contribuir

El objetivo es ayudar a dueños de cafeterías y tiendas a decidir con evidencia. Antes de añadir una métrica, explica qué pregunta operacional responde y qué podría interpretarse incorrectamente.

## Desarrollo local

```bash
git clone https://github.com/juliosuas/pulso-local.git
cd pulso-local
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
python scripts/download_assets.py
python -m pytest -q -W error
```

Usa una rama y un PR con problema, cambio observable y verificación. Añade pruebas cuando cambies conteos, continuidad temporal, geometría, lectura/exportación o contrato de datos. Mantén CPU como ruta de referencia y las dependencias principales permisivas. No agregues reconocimiento facial, perfiles demográficos o telemetría de video.

## Documentación y ejemplos

Mantén actualizadas las opciones del CLI, `schema_version`, las limitaciones y el roadmap. Publica únicamente material cuya fuente y licencia estén documentadas. Las demos deben indicar si sus datos son reales o ilustrativos; no convertir IDs en clientes únicos ni dwell en espera sin medición independiente.

No subas credenciales, videos privados, registros del negocio o carpetas `runs/`. Incluye pasos mínimos para reproducir un bug usando la demo pública o datos sintéticos. Si el problema es de seguridad, usa [SECURITY.md](SECURITY.md).

## Versiones

Proyecto en etapa 0.x; describe cambios incompatibles y migraciones explícitamente. Las etiquetas de versión deben apuntar a un commit verificado. No publicar benchmarks sin entorno y procedimiento de medición.

Las contribuciones de código se reciben bajo Apache-2.0. Conserva avisos de terceros y documenta nuevas dependencias y assets.
