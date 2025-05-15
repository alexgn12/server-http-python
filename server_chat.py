import socket
import threading

HOST = 'localhost'
PORT = 46578
clientes = {}

def procesar_comando(cliente_socket, mensaje):
    if mensaje == "/usuarios":
        respuesta = ", ".join(clientes.values())
        cliente_socket.send(f"[Servidor]: Usuarios conectados: {respuesta}".encode('utf-8'))
def gestion_client(cliente_socket):
    try:
        nombre = cliente_socket.recv(1024).decode('utf-8')
        clientes[cliente_socket] = nombre
        print(f"🔔 {nombre} se ha unido")

        while True:
            data = cliente_socket.recv(1024)
            mensaje = data.decode('utf-8')
            if mensaje.startswith("/"):
                procesar_comando(cliente_socket, mensaje)
            if not data:
                break
            broadcast(data, cliente_socket)
    except:
        pass
    finally:
        nombre = clientes.get(cliente_socket, "Desconocido")
        del clientes[cliente_socket]
        broadcast(f"❌ {nombre} ha salido del chat".encode('utf-8'), cliente_socket)
        cliente_socket.close()

def broadcast(mensaje, socket_emisor):
    nombre_emisor = clientes.get(socket_emisor, "Anonimo")
    try:
        mensaje = mensaje.decode('utf-8')
    except:
        mensaje = "<mensaje inválido>"
    for socket_cliente in clientes:
        if socket_cliente != socket_emisor:
            try:
                socket_cliente.send(f"[{nombre_emisor}]: {mensaje}".encode('utf-8'))
            except:
                pass

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Servidor activo.")
    s.bind((HOST, PORT))
    s.listen(10)

    while True:
        socket_cliente, direccion = s.accept()
        threading.Thread(target=gestion_client, args=(socket_cliente,), daemon=True).start()
