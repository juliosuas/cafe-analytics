# Una web para el dueño, un repositorio para desarrollar

## Primer caso: cafetería de barra

**Pregunta:** ¿qué ocurre frente a la barra y qué momentos conviene revisar sin estar presente?

La primera demo específica usa [Ron Lach / Pexels 8430969](https://www.pexels.com/video/man-ordering-at-a-cafe-8430969/): 36 segundos, 900 fotogramas, interacción en mostrador. Es material de stock, no una grabación de un cliente ni una evaluación de su negocio. Sus dos zonas describen regiones de imagen: no clasifican a una persona como empleado o cliente. No hay puerta visible y no configuramos una línea artificial para simular entradas.

La demo produce evidencia de presencia; no prueba ahorro, reducción de espera o retorno de inversión. [Procedencia y licencia](../SOURCES.md).

## Dos superficies del mismo producto

| Superficie | A quién sirve | Qué debe responder | Qué contiene |
|---|---|---|---|
| Web pública | Dueño o encargado | ¿Me ayuda? ¿Cómo se vería en mi negocio? ¿Qué necesito probar? | Video de barra, resumen legible, casos por giro y pasos del piloto |
| GitHub | Desarrolladores e integradores | ¿Cómo se reproduce? ¿Dónde falla? ¿Cómo lo mejoramos? | Código, configuración, contratos, tests, evidencia de ejecución y backlog |
| Reporte local generado | Dueño y encargado con acceso autorizado | ¿Qué observó esta sesión y dónde lo puedo revisar? | Métricas, limitaciones y enlaces a instantes de evidencia |

La web pública no es un panel conectado a cámaras. El reporte local no es todavía un servicio diario ni remoto. Los datos de un piloto privado nunca deben publicarse automáticamente en GitHub Pages.

## Extender por pregunta, no por promesa

| Giro | Hipótesis útil | Señal observable | Validación adicional | Acción pequeña a evaluar |
|---|---|---|---|---|
| Cafetería | Se mezclan pedido y recogida | Ocupación y permanencia en zonas separadas | Inicio de atención y entrega, pedidos | Señalización o ubicación de recogida |
| Panadería | Hay acumulación en vitrina o caja | Presencia por región y circulación | Observación de fila y ventas | Cambiar exhibición o señal de pago |
| Comida para llevar | Recogidas interfieren con nuevos pedidos | Presencia en mostradores definidos | Timestamps de órdenes, preparación y entrega | Separar punto de recogida |
| Tienda de barrio | Un exhibidor dificulta el paso | Trayectorias y ocupación del pasillo | Cobertura, accesos y revisión manual | Mover exhibidor y comparar períodos |
| Barbería / salón | Sala de espera se llena en ciertas franjas | Presencia en área común | Agenda e inicio de servicio | Revisar distribución de citas |
| Lavandería | Entrega y recogida coinciden en mostrador | Presencia y permanencia de zona | Registro de órdenes y tipo de trámite | Ordenar el flujo de atención |

Estas son hipótesis, no resultados obtenidos con el video de cafetería. No entrenamos seis modelos ni declaramos seis verticales validadas. Las necesidades comunes son geometría configurable, tiempos fiables, evidencia y contexto. Cada giro requiere sus propias definiciones y muestra.

## Mejora técnica entregada en 0.1.1

- `occupancy.csv` registra cada zona en **todos** los fotogramas procesados, incluyendo ceros. Permite reconstruir cuándo aparece presencia, no solo leer el pico final.
- `owner-summary.json` y `owner.html` convierten el resumen técnico en hechos, preguntas y próximos pasos de revisión. Generación determinista, sin LLM ni API.
- Los máximos se enlazan a su primer fotograma. En webcam, el enlace usa tiempo de reproducción del MP4, mientras el texto conserva tiempo de captura.
- Una línea no configurada se representa como `null` / no disponible; no se presenta como cero clientes.
- Se conservan visitas parciales y sus límites. No se fabrica una medición de espera ni una recomendación de personal.

## Backlog técnico, en orden

1. **Vista adecuada y verdad de referencia.** Una toma fija más abierta que la demo; acceso, fila y entrega visibles. Etiquetar personas y zonas en varios momentos. Medir falsos positivos, omisiones, cambios de ID y error de permanencia antes de ajustar umbrales.
2. **Tracking frente a oclusiones.** Medir y reducir fragmentación con una evaluación repetible. Las portadas/fondos con personas y los cuerpos tapados son casos a probar. No sustituir estabilidad de ID por reconocimiento facial.
3. **Estados de servicio validados.** Definir entrada a fila, inicio de atención y entrega con anotación manual. Solo entonces estimar espera; no renombrar permanencia como espera.
4. **Captura fiable.** Salud de cámara, tiempo absoluto y zona horaria, reconexión, almacenamiento acotado y recuperación de sesiones. Distinguir falta de datos de ausencia de personas.
5. **Resumen por jornada.** Cobertura y comparación de períodos equivalentes, entrega privada y autenticada, evidencia accesible al dueño.
6. **Evaluación del beneficio.** Elegir una acción con el dueño, registrar cuándo cambió y comparar con datos del punto de venta si la pregunta implica ventas.

## Criterio para expandir

Primero demostrar que un dueño de cafetería puede contestar una pregunta operacional con datos revisables, dentro de un error acordado. Después repetir el protocolo en un segundo giro. No prometer autonomía, precisión comercial ni mejoras económicas hasta medirlas.

## Hallazgo al ejecutar la demo de barra

La ejecución inicial sin filtro generó 6 IDs y un pico de 3 en la zona frente a barra. La inspección del fotograma 90 mostró una figura impresa del fondo detectada como persona. Esto no describe un problema de atención del comercio: es un error del modelo sobre material visual.

Se añadió `min_person_height`, desactivado por defecto y fijado a `0.20` solo en esta demo. Se conserva una imagen del resultado anterior junto al resultado corregido en la evidencia técnica. La comparación es una calibración sobre el mismo clip, no una evaluación independiente ni prueba de generalización. Los siguientes clips deben medir también personas reales omitidas por este filtro.

## Flujo de clientes y bebidas: la próxima capacidad solicitada

La portada muestra una única demo procesada con varias personas ([Pexels 35545660](https://www.pexels.com/video/busy-cafe-with-customers-ordering-at-counter-35545660/)). Su toma móvil es una demostración visual de seguimiento; para medir zonas de operación se necesita otra grabación fija. La referencia previa de Artisti queda documentada históricamente en SOURCES.md y ya no está incrustada.

El objetivo operativo se amplía a **personas → preparación de bebida → puesta en entrega → retirada**. Para implementarlo con evidencia:

1. Conseguir una grabación autorizada de cámara fija que muestre acceso/flujo, estación de preparación y punto de entrega; puede requerir dos vistas sincronizadas.
2. Detectar y seguir tazas/vasos por separado de personas. Contar una misma taza en 100 frames debe producir un objeto, no 100 bebidas.
3. Definir eventos observables: objeto entra a estación, sale hacia entrega, queda disponible, se retira. Ver una taza no demuestra que se preparó un café; retirarla no demuestra pago.
4. Etiquetar manualmente una muestra y distinguir devolución, reutilización, tazas vacías, jarras, bandejas, oclusiones y varios vasos en un mismo pedido.
5. Comparar conteos de eventos y tiempos contra esa referencia; cruzar POS si la pregunta es venta o conversión.

**Estado:** detección de tazas y esos eventos aún no implementados. La demo procesada de 36 s continúa limitada a personas/zonas. Medimos la operación agregada, no desempeño individual del barista.


## Presentación actual · 9 de octubre de 2026

La marca pública es Pulso Local. La portada usa un montaje de 27 segundos de cafetería, restaurante/bar y tienda con métricas ficticias rotuladas. Es una demostración del concepto autorizada por el usuario, separada de la validación del motor. Los pedidos, consumos, roles y conteos de preparación de ese montaje están escritos en `docs/showcase/scenario.json`; no son capacidades implementadas ni resultados del modelo. Las demos anteriores se conservan como evidencia técnica.
