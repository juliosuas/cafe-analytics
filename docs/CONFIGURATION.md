# Configuración

Ejecuta desde la raíz del repositorio. El archivo JSON define geometría, no identidad de personas.

```json
{
  "anchor": "bottom_center",
  "zones": [
    {"name": "barra", "polygon": [[0.1, 0.4], [0.8, 0.4], [0.8, 0.9], [0.1, 0.9]]}
  ],
  "gates": [
    {"name": "acceso", "points": [[0.2, 0.7], [0.8, 0.7]], "in_direction": "negative_to_positive", "hysteresis": 0.012}
  ]
}
```

Este ejemplo es ilustrativo. Calibra sobre la cámara real; no copies coordenadas de otro local.

| Campo | Regla |
|---|---|
| `anchor` | `bottom_center` (por defecto, aproximación a pies) o `center` (p. ej. cenital) |
| `zones` | Al menos una zona; nombre único dentro de zonas y polígono convexo ≥3 vértices |
| `polygon` | Pares `[x,y]` entre 0 y 1; orden alrededor del borde, sin autointersecciones |
| `gates` | Lista opcional de líneas; puede estar vacía |
| `points` | Dos extremos distintos; longitud normalizada ≥0.01 |
| `in_direction` | `negative_to_positive` o `positive_to_negative` |
| `hysteresis` | Distancia normalizada a la línea; >0 y <0.2, por defecto 0.012 |
| `scene_note` | Nota de contexto que aparece en el reporte |

Origen: arriba a la izquierda; x crece hacia la derecha, y hacia abajo. Para A→B, lado positivo significa producto cruzado `(B−A)×(P−A)>0`. Una línea horizontal de izquierda a derecha cuenta entrada hacia abajo con `negative_to_positive`.

Zonas superpuestas cuentan a la misma persona en ambas. Puntos sobre el borde se consideran dentro. No sumes zonas superpuestas como si fueran grupos excluyentes.

## Opciones del comando `run`

| Opción | Valor inicial | Uso |
|---|---|---|
| `--source` / `--webcam` | Uno obligatorio | Archivo local o índice de cámara |
| `--config` | Obligatorio | Configuración JSON |
| `--model` | `models/yolox_s.onnx` | Modelo oficial compatible 640×640 |
| `--output` | `runs/session` | Carpeta nueva o vacía |
| `--width` | 960 | Ancho par, mínimo 320; detector siempre a 640×640 |
| `--threads` | 4 | Hilos CPU positivos |
| `--confidence` | 0.4 | Detecciones para crear nuevas pistas |
| `--low-score` | 0.12 | Detecciones para recuperar pistas existentes |
| `--max-seconds` | Sin límite | Duración de fuente/captura, positiva |
| `--preview` | Desactivado | Ventana local; Q termina |

Los valores deben satisfacer `0 < low-score <= confidence < 1`. Expiración de pista 1 s, confirmación 3 detecciones y hueco analítico 0.5 s son parámetros internos actuales, no opciones del CLI.

## Filtro de tamaño por cámara (0.1.1)

`min_person_height` es opcional: fracción de la altura de imagen que debe ocupar una caja detectada. Valor por defecto `0` (desactivado); rango `[0, 1)`. Se aplica después del detector y antes del tracker, tanto en video como webcam. Una caja exactamente en el límite se conserva.

La demo de barra usa `0.20`: en la primera ejecución una figura impresa del fondo produjo detecciones pequeñas; el filtro permite excluirlas en este encuadre. **No es un detector de carteles ni una calibración universal.** Puede excluir personas reales pequeñas, lejanas o parcialmente tapadas. Debe contrastarse con anotaciones del local y volver a revisarse si cambia el encuadre. Para medir distancias o una escena profunda se requerirá una calibración más adecuada.

`summary.json.size_filter` registra el umbral y `discarded_detection_samples`: cantidad de cajas descartadas a través de fotogramas, no número de personas ni falsos positivos confirmados. La prueba de regresión del video de barra verifica dos personas visibles en un fotograma inspeccionado, no precisión en todas las escenas.
