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
