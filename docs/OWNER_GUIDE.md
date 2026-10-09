# Analytics para decidir sin estar en el local

## El resultado que buscamos

Un dueño debe poder revisar en pocos minutos qué ocurrió durante el día, qué merece atención y qué puede hacer después. El producto final no será una colección de cajas sobre un video: será un resumen de operación, con evidencia verificable y límites claros.

**Hoy:** análisis local por ejecución, con CSV/JSON, video, reporte técnico y un resumen para el dueño (`owner.html`) que enlaza máximos de ocupación con su evidencia. **Pendiente:** lectura continua de cámaras, entrega remota, comparación automática por horarios y alertas. El dueño puede consultar el reporte terminado que alguien le comparta; todavía no hay un servicio que lo genere y envíe solo.

## De observación a acción

| Situación a investigar | Qué observar | Qué más hace falta | Posible acción y cómo comprobarla |
|---|---|---|---|
| Acumulación junto a la barra | Ocupación alta y permanencia prolongada en zona definida | Confirmar manualmente que es una fila; registrar inicio de atención | Probar apoyo en esa franja; comparar espera real y ventas con días equivalentes |
| Área poco utilizada | Pocos IDs y persona-segundos frente a otras zonas | Revisar visibilidad de cámara, apertura del área y circulación | Cambiar señalización o distribución; comparar uso posterior |
| Pasillo congestionado | Alta ocupación y trayectorias que se concentran | Validar que no es un error por perspectiva/oclusiones | Reubicar un exhibidor; medir flujo y congestión después |
| Variación de afluencia | Cruces de una línea en el acceso real | Validar dirección, errores y cobertura de todos los accesos | Adaptar preparación/turnos solo tras varios días representativos |
| Caída repentina de actividad | Menos observaciones | Confirmar cámara activa y horario de operación | Investigar primero calidad de datos; no concluir que faltan clientes |

Estas son hipótesis de uso, **no recomendaciones deducidas de la demo**. La demo de barra dura 36 segundos; la de supermercado, 11.37. Ninguna permite evaluar una operación comercial.

## Cómo debería ser el resumen diario (diseño, aún no implementado)

1. **Cobertura:** horas analizadas, interrupciones y calidad suficiente/insuficiente.
2. **Qué cambió:** ocupación, afluencia validada y permanencia frente a una línea base comparable.
3. **Excepciones:** períodos que cruzaron umbrales definidos para ese negocio, no números universales.
4. **Evidencia:** zona, horario, señal medida y un fragmento de video accesible solo al dueño autorizado.
5. **Próximo paso:** una hipótesis revisable, no una afirmación causal.
6. **Seguimiento:** acción tomada, fecha, costo si el dueño lo aporta y resultado observado.

El informe debe decir “datos insuficientes” cuando falte cobertura. Un cero de entradas no puede significar al mismo tiempo cámara apagada y negocio vacío.

## Lo que no podemos afirmar con este MVP

- Permanencia en una zona **no equivale** a tiempo de espera, atención, compra o abandono.
- ID de sesión **no equivale** a cliente único, visitante recurrente o identidad real.
- Un pico de ocupación **no prueba** falta de personal.
- No se calculan ventas, ticket promedio, rentabilidad o conversión sin datos de POS y definiciones consistentes.
- El sistema no mide desempeño individual de empleados ni satisfacción de clientes.
- Una correlación antes/después no demuestra que una acción causó la mejora.

## Primer piloto recomendado

Definir una sola pregunta operacional. Ejemplo: “¿En qué franjas debemos revisar acumulación junto a la barra?”. Seleccionar cámara fija, definir la zona con el encargado y usar varios períodos representativos. Etiquetar manualmente una muestra. Si se quiere medir espera, marcar entrada a la fila e inicio real de atención, no usar dwell como sustituto automático.

Revisar primero tasa de cobertura, errores de conteo y pérdida de IDs. Acordar con el dueño el error tolerable antes de usar los resultados para decidir. Guardar cambios operativos en una bitácora y comparar días equivalentes. [Protocolo de validación](VALIDATION.md).

## Explorar otros negocios

La [web pública](https://juliosuas.github.io/pulso-local/#negocios) traduce el método a seis giros con preguntas y datos faltantes. [Estrategia y backlog](PRODUCT_STRATEGY.md) explica cómo validar cada caso sin reutilizar ciegamente las zonas o conclusiones de una cafetería.
