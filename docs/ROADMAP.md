# Roadmap: del MVP al asistente de operación

La prioridad es que el dueño tome decisiones con evidencia sin estar presente. Ningún elemento pendiente de esta lista se comercializa como implementado.

## v0.1 — Base observable (disponible)

- [x] Personas, tracking por sesión y geometría configurable.
- [x] Permanencia, ocupación, líneas, trayectorias y heatmap.
- [x] MP4, CSV, JSON, reporte local y demo pública con atribución.
- [x] Pruebas de lógica, inferencia real y verificador de integridad.

## v0.1.1 — Barra y evidencia para el dueño (disponible)

- [x] Demo de cafetería de barra con fuente, licencia y configuración reproducible.
- [x] Ocupación por fotograma, incluyendo ceros, y primeros máximos trazables.
- [x] Resumen de sesión para el dueño; falta de acceso como dato no disponible.
- [x] Web pública con seis hipótesis por giro; documentación técnica en GitHub.
- [ ] Validación comercial de los casos: requiere pilotos específicos.

## v0.2 — Calidad y piloto en un local

- [ ] Dataset autorizado con cámara fija: acceso y barra, horas tranquilas y congestionadas.
- [ ] Ground truth de cruces y presencia; informe de precisión/recall, error de conteo y fragmentación de IDs.
- [x] Ubuntu 24.04 y macOS 14 arm64: inferencia y pipeline completo en GitHub Actions.
- [ ] Prueba con webcam física y Ubuntu sobre hardware del piloto.
- [ ] Indicadores de datos insuficientes: pérdidas de cámara, encuadre movido, zonas sin cobertura.
- [ ] Validación rigurosa de configuración y final de archivo vs error de lectura.

**Terminado cuando:** el dueño y el equipo acuerdan por escrito una tolerancia de error; una muestra separada de validación la satisface o el reporte declara claramente que no la cumple. La permanencia en barra no se etiqueta como espera sin validación independiente.

## v0.3 — Operación desatendida

- [ ] Captura RTSP/IP supervisada, reconexión y detección de stream congelado.
- [ ] Sesiones durables con cámara, local, inicio UTC y zona horaria de negocio.
- [ ] Almacenamiento local consultable, rotación y recuperación después de reinicio.
- [ ] Métricas de salud y exportación incremental; no confundir falta de datos con cero actividad.
- [ ] Validar cadencia real de webcam y video de salida.

**Terminado cuando:** ensayo continuo de al menos 72 horas con desconexiones y reinicios controlados, sin doble conteo tras recuperación, con huecos de cobertura visibles. Objetivo de prueba, no resultado actual.

## v0.4 — Resumen para el dueño

- [ ] Reporte por día/turno: cobertura, ocupación, afluencia validada y cambios relevantes.
- [ ] Comparación con línea base del mismo local y horarios comparables.
- [ ] Umbrales definidos por negocio; alertas con evidencia y sin repetición innecesaria.
- [ ] Acceso remoto autenticado y canal de entrega elegido por el dueño.
- [ ] Bitácora de decisiones y seguimiento de acciones.

**Terminado cuando:** el dueño puede responder qué cambió, qué revisar y por qué en una prueba de uso de cinco minutos; cada alerta permite verificar período, evidencia y calidad. Ninguna alerta comercial sale cuando la cobertura es insuficiente.

## v0.5 — Relación con resultados del negocio

- [ ] Integración opcional con POS: ventas y tickets agregados por franja.
- [ ] Definiciones de conversión y espera verificadas en el local.
- [ ] Experimentos antes/después con registro de cambios y factores externos.
- [ ] Reportes multitienda sin rastrear identidades entre ubicaciones.

**Terminado cuando:** cada métrica tiene denominador, ventana temporal, trazabilidad y limitaciones; los resultados distinguen correlación de causalidad.

## Fuera de alcance

Reconocimiento facial, clasificación de edad/género/emoción, identidad entre visitas, vigilancia individual del desempeño, inferencia de intención delictiva o decisiones automáticas de sanción. El foco es la operación del negocio.

## Extensión solicitada: flujo de bebidas

- [x] Referencia de servicio real visible como video en la portada, con fuente y alcance separados de la demo de IA.
- [ ] Video autorizado y fijo con preparación y entrega visibles.
- [ ] Detección/tracking de taza o vaso; eventos únicos de puesta en entrega y retirada, con tratamiento de oclusiones y devoluciones.
- [ ] Validación manual de preparación/entrega antes de presentar conteos o tiempos como métricas del negocio.

Esta extensión sigue pendiente; un video del proceso no significa que el software reconozca esas acciones.


## Extensión propuesta: Decisions + GPT-6 Luna

- [x] [Factibilidad y arquitectura](../DECISIONS.md) con escenario de costos y criterios de evaluación.
- [x] [Alcance comercial](../COMMERCIALIZATION.md) y videos de referencia atribuidos.
- [ ] Dataset autorizado, anotación y turnos de evaluación separados.
- [ ] Adaptador opcional, recortes, control de consumo y manejo de errores.
- [ ] Estados de mesas y entregas por estación, deduplicados y trazables.
- [ ] Inferencia real y comparación contra referencia manual; publicar aciertos y fallos.

Estado: propuesta. No cambia las capacidades disponibles de v0.1.1.
