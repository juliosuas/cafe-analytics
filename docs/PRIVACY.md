# Datos y privacidad

El núcleo ejecuta inferencia local. No envía videos a un servicio de IA ni necesita una cuenta. El descargador consulta las fuentes oficiales del modelo y la demo; la instalación consulta el registro de paquetes. El README utiliza badges externos de shields.io. La demo de GitHub Pages se sirve desde GitHub y solo contiene material público de Pexels.

**Sin reconocimiento facial no significa que el video sea anónimo.** Las salidas MP4/JPG conservan a las personas y otros elementos de la escena. Los IDs son etiquetas técnicas sin identidad asignada, pero sus trayectorias y horarios requieren un manejo adecuado al contexto.

| Se guarda | Dónde |
|---|---|
| Video anotado e imágenes | Carpeta de cada ejecución |
| Puntos, tiempos, IDs y cruces | CSV/JSON de la ejecución |
| Configuración y ruta de fuente | `config.json` / `summary.json` |
| Modelo y demo pública original | `models/` y `assets/` |

No hay borrado automático, cifrado propio, usuarios, autenticación ni controles de acceso integrados. Usa el control de acceso del sistema operativo y elimina sesiones según la política del local. Los usuarios deben determinar permisos, avisos y retención aplicables a su operación antes de usar videos de clientes o empleados; este documento describe comportamiento técnico, no sustituye esa evaluación.

`runs/`, modelos, videos originales y credenciales se excluyen de Git. Solo la demo pública revisada se copia a `docs/`. Antes de compartir un reporte propio, revisa video, imágenes y `source`; evita subirlos a issues públicos. En la fase remota habrá que separar datos agregados de evidencia de video y añadir autorización de acceso y retención explícita.

La portada reproduce un archivo MP4 de demo servido desde GitHub Pages. No incorpora reproductores externos de YouTube. El video muestra personas identificables de una fuente pública licenciada; el procesamiento no identifica sus rostros. Los reportes de negocios reales deben mantenerse privados.


La demo principal de Pulso Local es un montaje ilustrativo con datos ficticios incrustados y etiquetados. Los roles y métricas no describen a las personas retratadas ni proceden de seguimiento individual. Los reportes técnicos anteriores siguen identificados como ejecuciones del motor.
