# Café Analytics — MVP local

Detecta personas en un video o webcam, mantiene IDs durante la sesión y calcula actividad por zonas. Todo se procesa en tu computadora. No utiliza reconocimiento facial, embeddings de identidad ni inferencia de género, edad o emociones.

**Para ver el resultado sin instalar nada:** abre la [demo pública](https://juliosuas.github.io/cafe-analytics/) o `docs/report.html` desde un clon del repositorio. Incluye un video real de supermercado ya procesado, heatmap, trayectorias y enlaces a CSV/JSON. El archivo `docs/media/demo.mp4` también abre directamente en QuickTime o VLC.

## Qué incluye

- Detector YOLOX-S / ONNX, filtrado a la clase persona.
- Tracking geométrico original: filtro de Kalman, asociación húngara y segunda pasada con detecciones de menor confianza. Confirmación tras 3 detecciones; conserva el ID hasta 1 segundo sin detección. No hay identificación entre cámaras o sesiones.
- Polígonos convexos configurables con coordenadas normalizadas; editor visual sin servidor ni dependencias web.
- Permanencia observada y visitas por ID/zona, ocupación máxima, líneas de conteo bidireccional con histéresis y validación de cruce del segmento.
- Video anotado, trayectorias CSV e imagen, heatmap acumulado en persona-segundos y reporte HTML.
- Modelo y clip original descargables desde sus fuentes oficiales y verificables con SHA256. No requiere cuentas, claves ni internet después de instalar.

## Ejecutar en macOS Apple Silicon

Configuración recomendada: macOS 14 o superior, Python 3.12 **arm64**, al menos 4 GB de RAM libre. Se probó realmente en macOS 15.7.4 arm64 con Python 3.12.14; usa CPU, no requiere CUDA, PyTorch ni MPS.

Si ya tienes Homebrew:

```bash
brew install python@3.12 ffmpeg
```

Desde la raíz del repositorio `cafe-analytics`:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[test]'
python scripts/download_assets.py
cafe-analytics run --source assets/retail.mp4 --config configs/demo.json --output runs/mi-demo
open runs/mi-demo/report.html
```

`download_assets.py` descarga el modelo y el clip original al clonar; si ya existen, verifica sus hashes. No sobrescribe archivos con hash distinto. Evita Python 3.14 y terminales bajo Rosetta con estas versiones fijadas. Si usas Python de python.org y falla HTTPS por certificados, ejecuta el instalador de certificados de esa distribución.

## Ejecutar en Ubuntu

Instrucciones para Ubuntu 22.04/24.04, Python 3.10–3.12. Ubuntu 24.04 con Python 3.12 fue verificado en GitHub Actions el 8 de octubre de 2026, incluyendo el clip completo; Ubuntu 22.04 y webcam física no se probaron en esta publicación.

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip ffmpeg libgl1 libglib2.0-0
```

Desde la carpeta del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[test]'
python scripts/download_assets.py
cafe-analytics run --source assets/retail.mp4 --config configs/demo.json --output runs/mi-demo
xdg-open runs/mi-demo/report.html
```

En Ubuntu sin escritorio, omite `--preview` y abre el reporte desde una computadora con navegador. No instales simultáneamente `opencv-python` y `opencv-python-headless`. La versión de OpenCV elegida permite la vista previa de webcam con escritorio.

## Analizar tu video y dibujar zonas

```bash
cafe-analytics configure --source /ruta/mi-cafeteria.mp4 --output mi-editor.html
```

Abre `mi-editor.html` con doble clic. Marca los vértices en orden, pon un nombre y guarda cada zona. Para un acceso, elige “Línea de acceso” y marca dos puntos. La flecha `IN` señala la dirección de entrada; el botón “Invertir entrada” cambia la última línea. Descarga `zonas.json` y cópialo a la carpeta del proyecto.

```bash
cafe-analytics run --source /ruta/mi-cafeteria.mp4 --config zonas.json --output runs/cafeteria-01
```

El editor de ejemplo `docs/editor.html` usa el primer fotograma del video demo. Las zonas son convexas y no deben cruzarse consigo mismas; divide una zona cóncava en varias. Se admite superposición, pero el mismo ID aportará tiempo a cada zona superpuesta. Las coordenadas están entre 0 y 1, con origen en la esquina superior izquierda; son independientes de la resolución.

Sitúa la cámara fija, con el suelo y las personas completos si es posible. El ancla predeterminada es el centro inferior de la caja (aproximación a los pies). Para vista cenital se puede elegir el centro de la caja. Las zonas y el heatmap están en el plano de imagen: no hay calibración métrica ni corrección de perspectiva.

Una línea horizontal dibujada de izquierda a derecha tiene su lado positivo debajo; `negative_to_positive` cuenta entrada hacia abajo. `positive_to_negative` invierte la dirección. Las apariciones/desapariciones de una persona **no** cuentan como entrada/salida: debe cruzar la línea finita.

## Webcam opcional

Primero genera el editor desde la misma cámara y encuadre:

```bash
cafe-analytics configure --webcam 0 --output editor-webcam.html
```

Dibuja y descarga las zonas, luego:

```bash
cafe-analytics run --webcam 0 --config zonas.json --output runs/webcam-01 --max-seconds 60 --preview
```

`Q` cierra la vista previa y guarda resultados; `Ctrl+C` también finaliza y exporta. Sin `--max-seconds`, la captura continúa hasta detenerla. El índice 0 es habitual; prueba 1 si tu cámara es otra.

En macOS permite acceso a Cámara a la aplicación desde la que ejecutas Python (Terminal o Codex) en Ajustes del Sistema → Privacidad y seguridad → Cámara. Cierra otras aplicaciones que estén usando el dispositivo. En Ubuntu verifica acceso a `/dev/video0` y que tu sesión tenga permiso para la cámara.

La cámara física **no se activó ni verificó** durante esta entrega. La rama de captura se prueba con una fuente simulada. Usa tiempo monotónico de captura para sus métricas; el MP4 de webcam se escribe a FPS nominales y puede reproducirse más rápido si la inferencia no alcanza tiempo real. Los tiempos reales están en CSV/JSON. A 9 FPS de procesamiento, una cámara a 30 FPS no implica análisis en tiempo real de todos sus fotogramas.

## Salidas de cada ejecución

| Archivo | Contenido |
|---|---|
| `report.html` | Reporte local con reproductor y mapas |
| `annotated.mp4` | Cajas, IDs, zonas, línea, contadores y trayectorias |
| `summary.json` | Configuración, entorno, rendimiento, resumen de zonas y cruces |
| `zones.csv` | IDs observados, visitas, permanencia y ocupación máxima por zona |
| `visits.csv` | Inicio, última observación, segundos observados y motivo de cierre por visita |
| `tracks.csv` | Primera/última observación confirmada, tiempo observado y muestras por ID |
| `events.csv` | Cada cruce: tiempo, ID, línea y dirección `in`/`out` |
| `trajectories.csv` | Posición normalizada por ID y fotograma; incluye UUID de sesión |
| `heatmap.jpg` / `trajectories.jpg` | Visualización sobre el primer fotograma |
| `heatmap.csv` / `heatmap_seconds.npy` | Matriz 90 × 160 con persona-segundos sin suavizar |
| `config.json` / `preview.jpg` | Configuración exacta y fotograma anotado |

El video usa H.264 si encuentra FFmpeg con libx264; sin él conserva MP4V, que puede requerir QuickTime/VLC en lugar del navegador. FFmpeg es una herramienta externa opcional, no se redistribuye con el proyecto. El video no conserva audio.

Las carpetas de salida existentes con contenido se rechazan para no sobrescribir resultados; elige un nombre nuevo. Para abrir por HTTP, opcionalmente:

```bash
python -m http.server 8765 --bind 127.0.0.1
```

Abre `http://127.0.0.1:8765/runs/mi-demo/report.html`. Solo escucha en esta computadora.

## Cómo interpretar las métricas

- **ID confirmado no significa cliente único.** Puede fragmentarse tras una oclusión larga o intercambiarse cuando dos personas se cruzan. No distingue empleados de clientes y no identifica visitas repetidas de la misma persona.
- La permanencia suma diferencias entre timestamps de observaciones consecutivas del mismo ID dentro de la misma zona. Interpola huecos de hasta **0.5 s**; excluye huecos mayores y el intervalo incierto de cambio de zona. El tiempo empieza cuando el ID se confirma, no en su primera detección tentativa.
- Una visita se cierra al salir, perder seguimiento o terminar el video. `censored=true` indica cierre sin salida observada: no interpretar su duración como una visita completa. La media del reporte incluye estas visitas parciales y es una media de **tiempo observado**, no tiempo total de estancia.
- El heatmap acumula segundos entre observaciones confirmadas y se suaviza únicamente para la imagen; la matriz conserva valores originales. Sumar todos los píxeles devuelve los persona-segundos observados. No usar el color para comparar sesiones de distinta duración: su escala se normaliza por sesión.
- La histéresis evita contar el temblor cerca de la línea. Se cuenta cada cruce válido, por lo que una misma persona puede cruzar varias veces. No se suman indiscriminadamente puertas consecutivas para estimar clientes únicos.
- Videos con cortes o cámara móvil requieren dividir tomas y recalibrar. Se recomienda video de FPS constantes. Para archivos se usan timestamps del contenedor; si fallan, se registra `fps_fallback`. El MP4 se escribe a los FPS nominales: el tiempo de reproducción puede diferir en entradas de FPS variable.
- `--confidence 0.4` controla nuevas pistas y `--low-score 0.12` permite recuperar pistas existentes. Bajar demasiado la confianza aumenta falsos positivos. `--threads 4` y `--width 960` son valores iniciales. El detector siempre trabaja a 640 × 640.
- El estado conserva resúmenes por ID y eventos; los puntos detallados se escriben incrementalmente a CSV. Para una operación de muchas horas, divide sesiones y planifica retención de archivos. Este MVP no es un servicio multicanal ni un sistema de facturación, aforo legal o prevención de robos.

## Verificación reproducible

```bash
python -m pytest -q -W error
python scripts/verify_run.py runs/mi-demo
```

`VERIFICATION.md` documenta la ejecución real y sus límites. La comprobación de integridad decodifica **todo** el MP4, cruza CSV contra JSON, valida segundos de visitas y comprueba conservación del heatmap. No mide precisión contra anotaciones humanas.

## Licencias y fuente

El código propio y YOLOX usan Apache-2.0; ONNX Runtime usa MIT; NumPy/SciPy usan BSD. El video conserva la licencia de Pexels. Consulta `THIRD_PARTY.md`, `SOURCES.md`, `NOTICE` y `licenses/` para procedencia, hashes y condiciones de redistribución. No se instala Ultralytics ni se usa su licencia AGPL.
