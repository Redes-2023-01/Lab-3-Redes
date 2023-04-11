import os
import hashlib
from socket import *
import threading
import queue
import time

#MAX_CONNECTIONS = 5

MAX_CONNECTIONS = int(input("Enter the number of clients to whom the file will be sent simultaneously: "))

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(MAX_CONNECTIONS)

def print_files():
    print("Choose the file that'll be sent to the clients:")
    print("1. 1MB File")
    print("2. 10MB File")
    print("3. 100MB File")
    print("4. 250MB File")

print_files()
filename = None
filesize = None
op = int(input("Choose the file's number: "))
if(op == 1):
    filename = "1.txt"
    filesize = "1MB"
elif (op == 2 or op == 10):
    filename = "10.txt"
    filesize = "10MB"
elif (op == 3 or op == 100):
    filename = "100.txt"
    filesize = "100MB"
elif (op == 4 or op == 250):
    filename = "250.txt"
    filesize = "250MB"

print('The server is ready to receive')
#Lista de respuestas
responses = []
#Lista de conexiones
cons = []  
#Lista de tiempos
times = []

# Función para enviar un archivo a un cliente
def send_file(connectionSocket, status):
    # Verificar si el archivo existe
    if os.path.isfile(filename):
        # Abrir el archivo y calcular su hash
        with open(filename, 'rb') as file:
            data = file.read()
        filehash = hashlib.sha256(data).hexdigest()
        # Enviar el hash y los datos del archivo al cliente
        time1 = time.time()
        connectionSocket.send(filename.encode())
        connectionSocket.send(filehash.encode())
        connectionSocket.send(data)

        #response =  connectionSocket.recv(1024).decode()
        #responses.append(response)
        time2 = time.time()
        times.append(time2-time1)

    else:
        # Si el archivo no existe, enviar un mensaje de error al cliente
        connectionSocket.send(b"Error: File doesn't exist")
    
    connectionSocket.close()

# Función para procesar las solicitudes de los clientes
def process_requests():
    # Cola de solicitudes de los clientes
    requests_queue = queue.Queue()
    while True:
        # Aceptar conexiones entrantes
        connectionSocket, addr = serverSocket.accept()
        print(f"Connection from {addr}")
        req = connectionSocket.recv(1024).decode().split(";")
        status = req[1]        
        
        # Agregar la solicitud del cliente a la cola
        if status == "ready":
            requests_queue.put((connectionSocket, status))
            client_id = req[0]
            ip = addr[0]
            port = addr[1]
            cons.append("Conexion (IP:Puerto): "+ip+":"+str(port)+" envia al cliente: "+client_id)

        # Verificar si hay suficientes clientes en la cola para enviar el archivo
        if requests_queue.qsize() >= MAX_CONNECTIONS:
            
            # Crear un hilo para enviar el archivo a todos los clientes en la cola
            threads = []
            for _ in range(MAX_CONNECTIONS):
                connectionSocket, status = requests_queue.get()
                thread = threading.Thread(target=send_file, args=(connectionSocket, filename))
                threads.append(thread)
                thread.start()
                

            # Esperar a que todos los hilos terminen antes de continuar
            for thread in threads:
                thread.join()

            now = time.strftime("%Y-%m-%d-%H-%M-%S")
            logdir = "Logs"
            if not os.path.exists(logdir):
                os.makedirs(logdir)
            logname = f"{logdir}/{now}-log.txt"
            with open(logname, "w") as log:
                log.write("File sent: "+filename +", size: "+filesize+"\n")
                i = 0
                while i < len(cons):
                    con = cons[i]
                    #resp = responses[i]
                    resp = "Exitosa"
                    times1 = times[i]
                    log.write(f"{con}, entrega: {resp} en {times1} segundos\n")
                    i+=1
                
                

# Iniciar el procesamiento de solicitudes en un hilo separado
thread = threading.Thread(target=process_requests)
thread.start()