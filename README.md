# HTTP Server from Scratch

Servidor web básico hecho desde cero con sockets en Python.

## Características

- Soporte para peticiones `GET`
- Tipos MIME detectados automáticamente
- Respuestas `200`, `403`, `404`, `405`
- Listado automático de archivos en carpetas
- Acceso a logs en JSON vía `/logs`

## Uso

1. Coloca tus archivos web en la carpeta `www/`
2. Ejecuta `server.py`
3. Abre `http://localhost:8080` en tu navegador
