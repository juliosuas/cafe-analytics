# Pulso Local + Decisions: evaluación de factibilidad

9 de octubre de 2026 · Evaluación documental y del código local. No se hicieron llamadas de inferencia a Decisions, no se enviaron videos y no se validó acceso de la cuenta, precisión o latencia. El resultado es una recomendación de piloto, no una integración terminada.

## Dictamen

Es técnicamente viable añadir Decisions como un clasificador visual opcional sobre el motor local. Recomiendo empezar por estado de mesas y posibles entregas en una zona bien visible. El riesgo principal está en la calidad de observación y en transformar clasificaciones repetidas en eventos únicos. Seguir durante horas a una persona, reconocer un pedido y atribuir producción a un empleado son problemas adicionales.

## Capacidades oficiales relevantes

[Guía de Decisions](https://developers.openai.com/api/docs/guides/decisions): beta con `gpt-6-luna`, endpoint `/v1/decisions`; devuelve predicados probabilísticos, categorías o puntuaciones. Permite preguntas independientes sobre evidencia compartida. El SDK Python documentado empieza en 3.26.0. Precio: USD 0.10 por millón de tokens de entrada; sin cargos de salida o caché en ese endpoint, con excepciones de región/contexto largo.

[Referencia del endpoint](https://developers.openai.com/api/reference/resources/decisions/methods/create): texto e imágenes; para el piloto se proponen recortes codificados en base64. No admite archivos de video, audio, file IDs ni llamadas a herramientas. Puede devolver rechazo; `usage.input_tokens` permite registrar consumo real.

La guía anuncia una aceleración relativa frente a Responses; no aporta una latencia garantizada para nuestro caso. No debe venderse como una garantía de tiempo real en cámaras. Las probabilidades requieren evaluación con ejemplos propios.

## Qué se puede construir

| Métrica o función | Factibilidad estimada | Implementación y límite |
|---|---|---|
| Mesa libre/ocupada/no visible | Buena candidata inicial | Recorte por mesa; clasificar estado, exigir persistencia y mantener cobertura. Mesa ocupada no significa misma persona. |
| Mesa con vasos/platos por retirar | Candidata, requiere evaluación | Definir evidencia visible y distinguir mesa sin personas de pertenencias dejadas. No inferir suciedad que no se ve. |
| Persona sentada durante dos horas | Condicionada | Video continuo, asiento visible y sesión estable. Guardar huecos como desconocidos. El tracker geométrico actual no garantiza identidad durante horas. |
| Entrega o retirada de bebida | Experimental | Secuencia corta antes/durante/después; clasificar evento, asociar zona/objeto y deduplicar ventanas. |
| Doce cafés preparados por hora | Más difícil que entregas | Ver preparación completa y distinguir taza vacía, bebida terminada, entrega, devolución y reutilización. Empezar por “entregas observadas en barra”. |
| Ese cliente pidió un café | Requiere pedidos/POS o anotación | La cámara no confirma orden, cobro, tipo de bebida ni titular de la compra. Enlazar mesa/ticket explícitamente. |
| Producción de un barista concreto | Fase posterior | Rol/estación asignado por configuración, evidencia suficiente y revisión de atribución. Empezar por estación, sin identificación facial. |
| Entradas, ocupación, tiempo en zona | Ya hay base local | Mantener cálculo en el motor; Decisions se reserva para criterios semánticos. |
| Ventas y conversión | Integración adicional | Cruces validados + tickets/POS; no confundir presencia con compra. |

Estas clasificaciones son juicio de ingeniería basado en la entrada disponible y el código, no resultados de un benchmark de Decisions.

## Diseño de integración propuesto

1. El proceso local conserva detección, tracking, zonas y reloj de captura. El video completo permanece local.
2. Un selector conserva un buffer y detecta cambios relevantes en mesa/barra. Para estados lentos, probar capturas cada 5–30 segundos. Para entregas, probar ráfagas con imágenes antes/durante/después: un muestreo lento puede perderlas.
3. Un trabajador separado envía recortes útiles con timestamps, zona e instrucciones limitadas a hechos visibles. Ensayar, por ejemplo, 3–5 imágenes por evento; es un parámetro de prueba, no una receta validada. Incluir categoría “no se puede determinar”.
4. El registro de eventos conserva evidencia, probabilidad, versión de pregunta/modelo y estados pendiente/confirmado/incierto. La duración se calcula localmente. Solo sumar una entrega tras una transición confirmada; reiniciar al terminar el episodio. Un periodo de bloqueo fijo por sí solo puede fusionar entregas legítimas: hace falta asociación espacial/temporal y, posiblemente, tracking de tazas.
5. Agregar por mesa, zona y franja horaria. Cada tarjeta enlaza al instante original. Un rechazo, timeout o imagen ilegible produce dato desconocido, nunca cero ventas o ausencia de actividad.

Concurrencia limitada, cola acotada y descarte de trabajos obsoletos mantienen el análisis local funcionando aunque la API falle. Respuestas retrasadas se ordenan por tiempo de captura. Los reintentos reutilizan un identificador interno de evento para no duplicar sus efectos. Registrar tokens, latencia, errores y cobertura.

## Ajuste al repositorio actual

- `cafe_analytics/cli.py` ya produce timestamps, trayectorias, ocupación y resumen por sesión.
- `cafe_analytics/tracker.py` mantiene IDs geométricos y, por defecto, pierde pistas tras un segundo sin observación. Esto limita la atribución a una persona durante horas.
- `cafe_analytics/analytics.py` registra cruces. `events.csv` actualmente significa cruce de línea: añadir un archivo separado para eventos semánticos, sin cambiar silenciosamente ese contrato.
- `pyproject.toml` no incluye un cliente OpenAI. Proponer una dependencia opcional, proveedor desactivado por defecto y una configuración independiente para conservar el modo local.
- La web pública es estática. La clave de API y el trabajador deben vivir en el servicio local/backend, nunca en GitHub Pages. Los reportes privados de un negocio requieren otra superficie distinta a la demo pública.
- Las tarjetas de la demo siguen siendo simuladas. Su aspecto no prueba capacidad de reconocimiento o precisión.

## Economía: escenario explícito, no cotización

Hipótesis: 12 horas diarias, 30 días al mes, **1,000 tokens de entrada totales por solicitud**, una solicitud por intervalo por cámara. Esa cifra de tokens es un supuesto que incluye imagen/texto/preguntas; no una medición ni una equivalencia fija por imagen. Tarifa estándar del endpoint documentada arriba.

| Intervalo | Solicitudes/día/cámara | USD/mes/cámara | USD/mes/3 cámaras |
|---|---:|---:|---:|
| 30 s | 1,440 | 4.32 | 12.96 |
| 5 s | 8,640 | 25.92 | 77.76 |
| 1 s | 43,200 | 129.60 | 388.80 |

Costo = solicitudes × tokens de entrada por solicitud / 1,000,000 × USD 0.10. Si cada solicitud usa 5,000 tokens, multiplicar estas cifras por cinco. Varios recortes por cámara, ráfagas, reintentos o más horas añaden consumo. No incluye infraestructura, hardware, almacenamiento, impuestos ni recargos regionales. El consumo del piloto se presupuestará con `usage.input_tokens`, no estimando un precio fijo por fotograma.

## Primera prueba recomendada

- Un local, una cámara fija y una zona visible de entrega; agregar mesas solo si el encuadre lo permite. Empezar con 60–120 minutos continuos autorizados; extender si no hay suficientes eventos. Para comprobar permanencias de dos horas, grabar más de dos horas con margen antes y después.
- Usar material original sin cuadros/textos simulados, sin acelerar ni repetir. Los clips actuales sirven para humo técnico, no para validar tiempos, frecuencias ni rendimiento real.
- Etiquetar manualmente estados y entregas, incluyendo casos negativos, devolución de vasos, manos ocultas y personas cruzando. Objetivo orientativo: al menos 100 entregas y negativos suficientes; no es una certificación estadística. Separar bloques/turnos de ajuste y evaluación para evitar filtrar fotogramas casi idénticos.
- Comparar método local simple y método con Decisions usando el mismo conjunto de evaluación. Reportar precisión, recall, duplicados, error del conteo por intervalo, cobertura, p50/p95 de latencia y costo por hora de cámara.
- Umbral de aceptación propuesto para un piloto informativo: precisión de entregas >=95%, recall >=90% y error de conteo <=10%, con tamaño de muestra y limitaciones visibles. Son objetivos por acordar/medir, no cifras alcanzadas. Para mesa ocupada, medir exactitud por estado y error en los cambios de ocupación.
- Entregable: video con evidencia revisable, eventos JSON/CSV y un reporte de comparación. Solo después convertir “entregas observadas” en alertas o intentar “bebidas preparadas”.

## Datos y operación

Esta extensión cambia el producto de local a híbrido cuando se activa: los recortes seleccionados salen hacia la API. Enviar únicamente las regiones necesarias, mantener acceso privado y documentar retención. No asumir ZDR por defecto: [controles de datos oficiales](https://developers.openai.com/api/docs/guides/your-data) detallan elegibilidad. No se requieren reconocimiento facial ni atributos demográficos para este piloto.

## Recomendación

Avanzar con una prueba acotada de **estado de mesas + entregas observadas por estación**. Dejar la continuidad de IDs, cálculo de tiempos, deduplicación y agregación en nuestro sistema. Integrar POS para pedidos/ventas y mantener las métricas agregadas por estación, sin evaluar el desempeño individual. Antes de una integración real falta comprobar acceso a Decisions, consumir una muestra autorizada y medir su precisión, costo y latencia reales.


## Contrato propuesto de eventos (todavía no implementado)

Escribir `semantic-events.jsonl` separado de los cruces actuales. Cada registro tendría `event_id`, `session_id`, `camera_id`, `zone_id`, `captured_at`, `window_start`, `window_end`, `event_type`, `status`, `evidence_refs`, `model`, `question_version`, `probability`, `input_tokens` y `latency_ms`. Las referencias de evidencia serían privadas; no subir imágenes reales del cliente a GitHub Pages. Los IDs de eventos se generan localmente y se reutilizan en reintentos.

Estados: candidato → confirmado / incierto / descartado. Mantener el original y la revisión humana. Una clasificación repetida no crea otra entrega. Un fotograma perdido abre un hueco de cobertura; no prolonga automáticamente una permanencia. No sumar probabilidades para obtener cantidades de cafés.

Ejemplos de preguntas para diseñar el piloto, no prompts validados:

- Mesa: `ocupada`, `sin_personas_visibles`, `no_determinable`. Pertenencias solas no prueban ocupación por una persona.
- Barra: en la secuencia ordenada, ¿se observa una transferencia de una bebida desde el área de entrega hacia fuera de esa área? Una mano que tapa el vaso no confirma una entrega.
- Revisión: ¿el encuadre permite responder? Si no, suspender métricas dependientes y pedir revisar la cámara.

## Secuencia de implementación

1. Dataset autorizado, recortes y anotación manual; manifiesto de fuentes y división por turnos.
2. Adaptador opcional y desactivado por defecto; secreto solo en backend. Comprobar acceso y hacer una prueba pequeña con presupuesto limitado antes de procesar sesiones.
3. Clasificaciones con trazabilidad, límites de concurrencia y presupuesto; estados de error explícitos.
4. Máquina de estados, deduplicación y pruebas de reintento, oclusión, eventos próximos y respuestas fuera de orden.
5. Comparación sobre turnos reservados y reporte de métricas/costo. Publicar resultados, incluidos fallos, antes de afirmar que funciona en negocios reales.

Este commit documenta la propuesta; no agrega SDK, llamadas a OpenAI ni una nueva opción de CLI. El motor local mantiene sus dependencias y comportamiento.

## Comercialización y material público

Ver [alcance comercial y criterios de publicación](COMMERCIALIZATION.md). La web presenta una integración propuesta, videos externos y escenarios a validar; los videos no son evidencia de una instalación de Pulso Local.

## Referencias visuales para diseñar el piloto

La [curaduría y procedencia](COMMERCIALIZATION.md) recoge huevos, tacos, limones y cafetería. Solo el caso de huevos declara Decisions / GPT-6 Luna. Los otros sirven para comparar patrones de arquitectura o interfaz, no para demostrar la misma API. Para una barra, el patrón a ensayar es detector → seguimiento de objeto/episodio → selección de imágenes → clasificación → evento deduplicado. Mantener separado el benchmark propio de los videos de promoción de terceros.
