import socket
import threading
import os
import mimetypes
from datetime import datetime
import json

HOST = "localhost"
PORT = 8080

logs = []


def parsea_get(data):
    linea = data.split('\r\n')
    divide = linea[0].split(' ')
    metodo = divide[0]
    ruta = divide[1]
    version = divide[2]
    return metodo, ruta, version


def gestion_client(cliente_socket, direccion):
    try:
        data = cliente_socket.recv(1024).decode('utf-8')
        metodo, ruta, version = parsea_get(data)
        
        if metodo != "GET":
            codigo = 405

            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ip = direccion[0]

            log = {
                "timestamp": fecha,
                "ip": ip,
                "ruta": ruta,
                "codigo": codigo
            }

            logs.append(log)
            with open("logs.json", "w") as f:
                json.dump(logs, f, indent=2)
            print(f"[{log['timestamp']}] {log['ip']} - \"{log['ruta']}\" -> {log['codigo']}")

            respuesta = "HTTP/1.1 405 Method Not Allowed\r\n\r\n<h1>405 Method Not Allowed</h1>"
            cliente_socket.sendall(respuesta.encode('utf-8'))
            return

        if ruta == '/':
            ruta = '/index.html'

        archivo = os.path.join("www", ruta.strip("/"))

        # Seguridad: solo servir archivos dentro de www
        ruta_absoluta = os.path.abspath(archivo)
        raiz_absoluta = os.path.abspath("www")
        if ruta == '/logs':
            codigo = 200
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ip = direccion[0]

            log = {
                "timestamp": fecha,
                "ip": ip,
                "ruta": ruta,
                "codigo": codigo
            }

            logs.append(log)
            with open("logs.json", "w") as f:
                json.dump(logs, f, indent=2)

            print(f"[{log['timestamp']}] {log['ip']} - \"{log['ruta']}\" -> {log['codigo']}")

            respuesta_json = json.dumps(logs).encode('utf-8')
            cabecera = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(respuesta_json)}\r\n\r\n"
            cliente_socket.sendall(cabecera.encode('utf-8') + respuesta_json)
            return

        if not ruta_absoluta.startswith(raiz_absoluta):
            respuesta = "HTTP/1.1 403 Forbidden\r\n\r\n<h1>403 Forbidden</h1>"
            codigo = 403

            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ip = direccion[0]

            log = {
                "timestamp": fecha,
                "ip": ip,
                "ruta": ruta,
                "codigo": codigo
            }
            
            logs.append(log)
            with open("logs.json", "w") as f:
                json.dump(logs, f, indent=2)

            print(f"[{log['timestamp']}] {log['ip']} - \"{log['ruta']}\" -> {log['codigo']}")

            cliente_socket.sendall(respuesta.encode('utf-8'))
            return

        if os.path.isfile(archivo):
            with open(archivo, "rb") as f:
                contenido = f.read()
                
            tipo, _ = mimetypes.guess_type(archivo)
            if tipo is None:
                tipo = "application/octet-stream"

            cabecera = f"HTTP/1.1 200 OK\r\nContent-Type: {tipo}\r\nContent-Length: {len(contenido)}\r\n\r\n"

            codigo = 200

            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ip = direccion[0]

            log = {
                "timestamp": fecha,
                "ip": ip,
                "ruta": ruta,
                "codigo": codigo
            }
            
            logs.append(log)
            with open("logs.json", "w") as f:
                json.dump(logs, f, indent=2)

            print(f"[{log['timestamp']}] {log['ip']} - \"{log['ruta']}\" -> {log['codigo']}")
            cliente_socket.sendall(cabecera.encode('utf-8') + contenido)

        else:
            codigo = 404
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ip = direccion[0]

            log = {
                "timestamp": fecha,
                "ip": ip,
                "ruta": ruta,
                "codigo": codigo
            }
            
            logs.append(log)
            with open("logs.json", "w") as f:
                json.dump(logs, f, indent=2)

            print(f"[{log['timestamp']}] {log['ip']} - \"{log['ruta']}\" -> {log['codigo']}")
            cuerpo = "<h1>404 Not Found</h1>"
            cabecera = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: {}\r\n\r\n".format(len(cuerpo))
            cliente_socket.sendall(cabecera.encode('utf-8') + cuerpo.encode('utf-8'))

    except Exception as e:
        print(f"[Error] {e}")
    finally:
        cliente_socket.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Servidor activo.")
    s.bind((HOST,PORT))
    s.listen(10)

    while True:
        socket_cliente, direccion = s.accept()
        threading.Thread(target=gestion_client, args=(socket_cliente,direccion), daemon=True).start()
