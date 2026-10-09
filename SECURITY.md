# Seguridad

Este proyecto es un MVP local, no un servicio endurecido para producción. La demo pública no acepta uploads ni ejecuta inferencia en el servidor.

## Reportar un problema

Utiliza la opción privada **Report a vulnerability** en la pestaña Security de este repositorio si está disponible. No publiques credenciales, video privado ni información de clientes en un issue. Si la opción no aparece, abre un issue solicitando un canal privado sin describir detalles sensibles. No se ofrece un SLA de respuesta.

Incluye versión/commit, comportamiento, impacto, pasos mínimos y una reproducción con datos públicos o sintéticos.

## Superficie relevante

Archivos de video e imágenes, modelo ONNX, configuración JSON, HTML generado y dependencias nativas de OpenCV/ONNX Runtime. Procesa archivos y modelos de fuentes confiables; la descarga estándar valida los hashes de los assets oficiales. Los reportes propios pueden revelar rutas locales y contenido visual identificable.

No hay autenticación, aislamiento multiusuario ni retención automática. El servidor opcional de documentación debe escuchar en `127.0.0.1`, como indica la guía. No lo expongas directamente como una plataforma de video para clientes.

En etapa 0.x se prioriza la versión más reciente publicada; no hay compromiso de mantenimiento de ramas anteriores. Esta política no constituye una auditoría de seguridad.
