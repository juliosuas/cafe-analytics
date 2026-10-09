# Fuentes y procedencia

Consultadas el 3 de octubre de 2026.

## Video demo

- Título de la página: **Customers Shopping at Supermarket**.
- Autor: **Suika Chan**.
- Página: https://www.pexels.com/video/customers-shopping-at-supermarket-10901926/
- Descarga pública: https://videos.pexels.com/video-files/10901926/10901926-hd_1920_1080_30fps.mp4
- Licencia: **Pexels License**, https://www.pexels.com/license/
- Archivo descargado por el script (no versionado en Git): `assets/retail.mp4`, sin modificar, 1920 × 1080, 30 FPS, 341 fotogramas (11.3667 s).
- SHA256: `93e3f7aa893d781e61de49855d736662ab32b54d026f008a55b285b06cdbfd0b`.

Pexels permite descargar, usar y modificar sus videos gratuitamente, incluido el uso comercial sujeto a sus condiciones. No es una licencia de código abierto ni dominio público. No vender copias sin modificar, no sugerir respaldo de las personas o marcas retratadas, no redistribuir como biblioteca de stock ni usar personas identificables de manera ofensiva. La atribución no es obligatoria según esa página, pero se conserva por trazabilidad. Este video se usa como material de demostración de software; no se afirma que las personas o Pexels respalden el producto.

La escena es un supermercado real con oclusiones y cuerpos parcialmente cortados. Las dos zonas y la línea virtual son ilustrativas; no se ve una puerta de acceso real. La ejecución verifica funcionamiento, no exactitud de visitas ni aforo. Para un piloto comercial, usar una toma fija propia con acceso y suelo visibles y medir errores contra un conteo manual.

No se entrenó ni ajustó ningún modelo con este video. Las imágenes y el video anotado son derivados del mismo material y no quedan relicenciados bajo Apache-2.0.

## Detector

- Proyecto oficial: https://github.com/Megvii-BaseDetection/YOLOX
- Licencia del repositorio: https://github.com/Megvii-BaseDetection/YOLOX/blob/main/LICENSE (Apache-2.0).
- Guía oficial y enlaces a pesos: https://github.com/Megvii-BaseDetection/YOLOX/tree/main/demo/ONNXRuntime
- Release: `0.1.1rc0`, archivo oficial `yolox_s.onnx`.
- Descarga: https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_s.onnx
- SHA256: `c5c2d13e59ae883e6af3b45daea64af4833a4951c92d116ec270d9ddbe998063`.
- Entrada: BGR float32, 1 × 3 × 640 × 640, valores 0–255, relleno 114.
- Salida: 1 × 8400 × 85, decodificación de grids/strides; confianza persona = objectness × probabilidad de clase 0. NMS 0.45.

Se conserva la licencia y atribución del proyecto oficial que distribuye los pesos. No se encontró una licencia separada del archivo ONNX en la guía del release; la clasificación permisiva se basa en la licencia del proyecto distribuidor, no en una garantía sobre cada imagen de entrenamiento COCO. No se redistribuye el dataset COCO.

## Demo de cafetería de barra · añadida en 0.1.1

- **Autor:** Ron Lach. **Título de fuente:** Man Ordering at a Café.
- Página: https://www.pexels.com/video/man-ordering-at-a-cafe-8430969/
- Licencia: https://www.pexels.com/license/ (consultada el 8 de octubre de 2026, hora de Ciudad de México).
- Archivo: https://videos.pexels.com/video-files/8430969/8430969-uhd_4096_2160_25fps.mp4
- Original: 4096×2160, 25 FPS, 36 segundos, 900 fotogramas.
- SHA256: `37c732b261d16cf8fe23b6a2f4745b0c321b18c5b7680657ed2e47ab0e28cebd`.
- Descarga reproducible: `python scripts/download_assets.py --demo cafe`. El original se guarda en `assets/cafe-counter.mp4`, excluido de Git.
- Derivados de análisis publicados en `docs/cafe/`: video con anotaciones y sin audio, preview, mapas, reportes y datos. No se relicencia el material audiovisual como Apache-2.0. Las personas y marcas del clip no respaldan este proyecto.
- Es material de stock para una demostración técnica: encuadre cercano, oclusiones y cuerpos recortados. No es CCTV, un caso de éxito ni evidencia de la operación diaria de esa cafetería. No se evalúa a las personas retratadas ni se presentan fallas de su servicio.
- Configuración: `configs/cafe-counter.json`, ancla en centro de caja por pies ocultos. Zonas de imagen a ambos lados de la barra, sin líneas de entrada/salida ni clasificación empleado/cliente. El centro no reconstruye una posición física sobre el piso.

## Referencia histórica de operación (retirada de portada)

- **Autor:** Artisti Coffee Roasters. **Video:** See how a professional barista makes coffee working solo, duración observada en el reproductor 29:09.
- Reproductor original: https://www.youtube.com/watch?v=RKAva1OK8i4
- Publicación del autor: https://artisti.com.au/blogs/training/working-solo-in-a-busy-espresso-bar-barista-work-flow-and-multi-tasking
- El autor describe aproximadamente 30 minutos atendiendo pedidos y preparando café durante la mañana. Inspección visual: en 14:34 se ve llegada a la barra y vasos sobre el mostrador; en otros momentos se ve preparación en la máquina.
- Anteriormente se enlazó mediante YouTube en 14:34; ya no se incorpora a la portada. **No se descargó, modificó ni republicó el video. No se encontró una licencia permisiva para incorporarlo como dataset o asset del repositorio.** Es una referencia de observación, no nuestra demo analizada ni una relación comercial con el autor.
- Tiene cambios de encuadre; no es una grabación continua de una sola cámara para medir trayectorias o tiempos sin segmentación. No se publican conteos inferidos de tazas, clientes o pedidos sobre ese video.


## Video protagonista: cafetería con varias personas

- Autor: **Sururi Ballıdağ Director**. Título: **Busy Cafe with Customers Ordering at Counter**.
- Fuente: https://www.pexels.com/video/busy-cafe-with-customers-ordering-at-counter-35545660/
- Licencia Pexels: https://www.pexels.com/license/ (consultada el 8 de octubre de 2026). Permite modificación y uso web; no se implica respaldo de las personas o marcas. El audiovisual conserva esta licencia, separada del código Apache-2.0.
- Archivo procesado: https://videos.pexels.com/video-files/35545660/15059172_2560_1440_30fps.mp4
- Descarga: 2560×1440, 30000/1001 FPS, aproximadamente 10.28 s. La ficha de Pexels anuncia otras dimensiones originales; esta es la variante descargada.
- SHA256: `c71710a841291aa530a9596735ef8989464bc1fb11bd6c965144b552fed6f3b9`.
- Original en `assets/cafe-flow.mp4`, excluido de Git. Descargador: `--demo cafe-flow`; configuración: `configs/cafe-flow.json`. Derivados del análisis en `docs/flow/`; H.264 sin audio.
- Es una toma real con varias personas, utilizada como ilustración del seguimiento. **La cámara se mueve**: única zona = encuadre completo; sin puertas ni roles. Trayectorias y heatmap contienen movimiento de cámara. No se usan como evidencia de espera, circulación física o desempeño de ese establecimiento.
- La portada contiene un solo reproductor local de esta demo. Los ejemplos de barra y supermercado siguen disponibles como archivos técnicos independientes.

## Candidatos pendientes de elección · 9 de octubre de 2026

La página `docs/candidatos.html` reproduce desde los proveedores originales estos candidatos; no son nuevas salidas del modelo ni sustituyen aún al video principal:

1. [A busy elegant bar — Mixkit 4043](https://mixkit.co/free-stock-video/a-busy-elegant-bar-4043/). La ficha declara Mixkit Stock Video Free License para uso personal/comercial. Video acelerado; la escala de tiempo real no está documentada. Fuente del reproductor: https://assets.mixkit.co/videos/4043/4043-720.mp4
2. [People Inside the Coffee Shop — Nazim Zafri / Pexels 3135925](https://www.pexels.com/video/people-inside-the-coffee-shop-3135925/). Licencia Pexels. Fuente del reproductor: https://videos.pexels.com/video-files/3135925/3135925-hd_1920_1080_30fps.mp4
3. [People are eating at tables in a food court — Nazim Zafri / Pexels 18533896](https://www.pexels.com/video/people-are-eating-at-tables-in-a-food-court-18533896/). Licencia Pexels. Fuente del reproductor: https://videos.pexels.com/video-files/18533896/18533896-hd_1920_1080_30fps.mp4

Fuentes y fichas consultadas el 9 de octubre de 2026. Las personas, negocios y marcas no respaldan el proyecto. Clips breves para elegir una escena visual; no acreditan pedidos, productividad, permanencias de dos horas ni ritmos horarios. No se extrapolan las repeticiones del video. Los archivos externos pueden cambiar o dejar de estar disponibles; cada tarjeta enlaza a la fuente.

## Montaje ilustrativo de Pulso Local · 9 de octubre de 2026

Por solicitud del usuario, la portada usa un único montaje de 27 segundos con datos ficticios. Todos los cuadros llevan el rótulo «DEMO ILUSTRATIVA · DATOS SIMULADOS». Los roles, pedidos, cantidades, visitas, compras y tiempos están escritos por diseño; **no proceden del pipeline ni describen hechos del material original**. No se clasifica ni evalúa a las personas retratadas. Los autores y marcas no respaldan el producto.

- 0–9 s: cafetería, Nazim Zafri / Pexels 3135925 (fuente y licencia indicadas arriba). Input `assets/marketing-cafe.mp4`, SHA256 `226924eb46bcafbd3d3dd6f1ad0aed6b35d45e58730fd692dd12c915e5eeae5a`.
- 9–18 s: restaurante/bar, Mixkit 4043, Mixkit Stock Video Free License. Input `assets/business-demo.mp4`, SHA256 `c2f9850f00c8d01e8c938f9452cbeebe7252d65a1088e85c349548d6eb517565`. La fuente es time-lapse; el montaje no infiere el tiempo real de esa grabación.
- 18–27 s: tienda, Suika Chan / Pexels 10901926 (fuente, licencia y SHA256 indicados al inicio). Input `assets/retail.mp4`.
- Derivados: `docs/showcase/demo.mp4` (H.264 1280×720, 30 FPS, sin audio), `poster.jpg` y `scenario.json`. El JSON contiene solo el guion de cifras ficticias.
- Renderer: `scripts/render_marketing_demo.py`, utiliza FFmpeg con drawtext y tipografías del sistema. Para reproducir, guarda los tres archivos en las rutas de input anteriores desde sus URLs documentadas; no hay llamadas de inferencia. Los originales no se versionan; los derechos audiovisuales siguen bajo las licencias de las fuentes, no Apache-2.0.


### Cuadros e IDs en el montaje

La revisión visual del montaje usa `scripts/render_showcase_tracking.py` para normalizar 9 s por escena a 30 FPS y ejecutar YOLOX-S con el tracker del proyecto. Los IDs llevan prefijos C/R/T y se reinician por escena. Se publican cajas y trazas visuales sin reconocimiento facial. Los roles y cifras de las tarjetas siguen siendo ficticios y no están vinculados al ID de ninguna persona. `scripts/render_marketing_demo.py --tracking-dir runs/showcase-tracking` coloca las tarjetas en una banda superior separada; salida 1280×960. Los resultados intermedios quedan en `runs/showcase-tracking`, excluidos de Git.
