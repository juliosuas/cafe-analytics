# Decisions: alcance comercial y comunicación

Revisión documental: 9 de octubre de 2026. Estado del proyecto: diseño de integración, sin inferencia Decisions ejecutada.

## Qué podemos ofrecer

La base contractual permite integrar la API en aplicaciones para usuarios finales ([OpenAI Services Agreement, §2.2](https://openai.com/policies/services-agreement/)). Esto da una vía para comercializar Pulso Local como producto propio sujeto al contrato y políticas aplicables; no autoriza revender cuentas o claves. Decisions continúa en beta, por lo que disponibilidad y comportamiento pueden cambiar.

Propuesta de negocio: un piloto de alcance acordado —una cámara, una pregunta de operación, validación y un informe— seguido, si demuestra utilidad, por instalación y servicio mensual de operación/soporte con consumo de API presupuestado. No hay precios finales, clientes, ahorro o retorno demostrado en este repositorio. Antes de contratar, verificar las condiciones aplicables a la cuenta, los derechos sobre el video y el tratamiento de datos del local.

El código Apache-2.0 permite uso comercial con sus obligaciones; la API es un servicio externo de pago y no hereda esa licencia. Las grabaciones de terceros mantienen sus licencias separadas: [procedencia](SOURCES.md) y [dependencias](THIRD_PARTY.md).

## Qué dice la página

- “Integración propuesta con Decisions API y GPT-6 Luna”. Es el estado real hoy.
- Escenarios: ocupación de mesas, entregas observadas y contexto en caja, sujetos a validación específica.
- Invitación a preparar un piloto, sin reserva ficticia, cupos inventados ni promesas de ventas.
- Videos externos con autor y enlace original. Distinguir presentación oficial, demo independiente y producto propio.

No usar “ya funciona con GPT-6”, “partner de OpenAI”, “productividad exacta”, “24/7 garantizado” ni promesas de precisión o rentabilidad. El nombre del producto sigue siendo Pulso Local. Las [guías de marca](https://openai.com/brand/) prohíben implicar patrocinio o respaldo inexistente; se usa una referencia textual, sin logotipo ni marca conjunta.

## Qué debe ocurrir antes de vender la capacidad como disponible

1. Demostrar inferencia real con cuenta habilitada y material autorizado.
2. Medir precisión, cobertura, duplicados, latencia y costo sobre video reservado de un local; [protocolo técnico](DECISIONS.md).
3. Mostrar errores e incertidumbre en el reporte, además de aciertos. Validar utilidad con el dueño.
4. Definir alcance, soporte, límites de consumo, retención y acceso privado. La integración activa enviaría recortes a OpenAI: no anunciar procesamiento enteramente local.
5. Publicar evidencia reproducible de la versión evaluada y recién entonces actualizar el estado de la web.

## Videos referenciados

| Video original | Autor / fecha | Uso en la página |
|---|---|---|
| [Introducing the Decisions API](https://www.youtube.com/watch?v=FB6oCmrIj-Y) | OpenAI, 6 octubre 2026 | Presentación oficial; capítulo de decisiones a partir de imágenes en 1:17, demostración robótica en 3:05. |
| [OpenAI’s Decisions API just dropped. Here’s how it compares to Jev.](https://www.youtube.com/watch?v=uTU5Ihgl_7Q) | Mark Kashef, 7 octubre 2026 | Demo independiente; inspección visual en 4:22 y revisión de reporte en 7:19. |

Se comprobaron títulos, autores y disponibilidad en los reproductores originales. Se incrustan mediante el reproductor de YouTube, sin descargar, editar ni redistribuir archivos. No se les asigna Apache-2.0 ni se asume una licencia abierta. Su reproducción depende de YouTube y del permiso de inserción del autor; siempre se ofrece enlace alternativo. No son clientes, colaboradores ni validadores de Pulso Local. Son demostraciones de tecnología, no evidencia de despliegue comercial ni resultados nuestros.

Fuentes técnicas vigentes: [Decisions](https://developers.openai.com/api/docs/guides/decisions), [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna) y [controles de datos](https://developers.openai.com/api/docs/guides/your-data).
