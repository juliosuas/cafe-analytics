# Componentes y licencias

La selección prioriza licencias permisivas en el detector, el runtime y el código de analytics. Mantén los avisos y licencias al redistribuir.

| Componente | Versión usada | Licencia principal / fuente |
|---|---|---|
| Código propio, tracking, zonas, reportes | 0.1.0 | Apache-2.0, `LICENSE` y `NOTICE` |
| YOLOX-S ONNX oficial | release 0.1.1rc0 | Apache-2.0 del [proyecto oficial](https://github.com/Megvii-BaseDetection/YOLOX/blob/main/LICENSE); detalle sobre pesos en `SOURCES.md` |
| ONNX Runtime | 1.22.1 | [MIT](https://github.com/microsoft/onnxruntime/blob/main/LICENSE) |
| OpenCV | 4.11.0 / opencv-python 4.11.0.86 | Biblioteca [Apache-2.0](https://opencv.org/license/); empaquetado Python MIT y avisos de binarios incluidos |
| NumPy | 2.2.6 | [BSD-3-Clause](https://numpy.org/doc/stable/license.html) |
| SciPy | 1.15.3 | [BSD-3-Clause](https://scipy.org/faq/) |
| Video de supermercado / derivados | Pexels 10901926 | [Pexels License](https://www.pexels.com/license/), separada de la licencia del código |
| FFmpeg / libx264 | Instalación del usuario, opcional | Depende de la compilación; libx264 implica componentes GPL. No incluido ni enlazado al código Python propio; se invoca como programa externo para codificar H.264. |

Los wheels de OpenCV contienen bibliotecas adicionales con sus propios avisos; no debe describirse el paquete binario completo como exclusivamente Apache. `licenses/dependencies/` conserva los avisos encontrados en los paquetes realmente instalados, incluyendo terceros de OpenCV, NumPy y ONNX Runtime. La combinación exacta de bibliotecas del wheel puede variar entre macOS y Ubuntu. Si redistribuyes runtimes o FFmpeg, conserva y revisa los avisos correspondientes a esos binarios concretos.

Dependencias indirectas registradas en `requirements-tested.txt`: coloredlogs (MIT), humanfriendly (MIT), flatbuffers (Apache-2.0), packaging (Apache-2.0/BSD), protobuf (BSD-3-Clause), sympy (BSD) y mpmath (BSD). Herramientas de pruebas: pytest, iniconfig y pluggy (MIT), Pygments (BSD). Los textos distribuidos en los wheels se guardan en `licenses/dependencies/`; flatbuffers no incluía texto de licencia en el wheel inspeccionado, por lo que se añadió el texto oficial de https://github.com/google/flatbuffers/blob/master/LICENSE .

No se depende de Ultralytics, DeepSORT, reconocimiento facial ni servicios comerciales de inferencia. Una licencia permisiva de software no sustituye las condiciones del material audiovisual ni implica certificación de exactitud del sistema.
