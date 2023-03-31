import os
import hashlib
from socket import *
import threading
import queue

MAX_CONNECTIONS = 5

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(MAX_CONNECTIONS)

print('The server is ready to receive')

# Función para enviar un archivo a un cliente
def send_file(connectionSocket, filename):
    # Verificar si el archivo existe
    if os.path.isfile(filename):
        # Abrir el archivo y calcular su hash
        with open(filename, 'rb') as file:
            data = file.read()
            filehash = hashlib.md5(data).hexdigest()

        # Enviar el hash y los datos del archivo al cliente
        connectionSocket.send(data)
        connectionSocket.send(filehash.encode())
        

    else:
        # Si el archivo no existe, enviar un mensaje de error al cliente
        connectionSocket.send(b"Error: El archivo no existe")

    connectionSocket.close()

# Función para procesar las solicitudes de los clientes
def process_requests():
    # Cola de solicitudes de los clientes
    requests_queue = queue.Queue()

    while True:
        # Aceptar conexiones entrantes
        connectionSocket, addr = serverSocket.accept()
        print(f"Connection from {addr}")
        filename = connectionSocket.recv(1024).decode()

        # Agregar la solicitud del cliente a la cola
        requests_queue.put((connectionSocket, filename))

        # Verificar si hay suficientes clientes en la cola para enviar el archivo
        if requests_queue.qsize() >= MAX_CONNECTIONS:
            # Crear un hilo para enviar el archivo a todos los clientes en la cola
            threads = []
            for _ in range(MAX_CONNECTIONS):
                connectionSocket, filename = requests_queue.get()
                thread = threading.Thread(target=send_file, args=(connectionSocket, filename))
                threads.append(thread)
                thread.start()

            # Esperar a que todos los hilos terminen antes de continuar
            for thread in threads:
                thread.join()

# Iniciar el procesamiento de solicitudes en un hilo separado
thread = threading.Thread(target=process_requests)
thread.start()