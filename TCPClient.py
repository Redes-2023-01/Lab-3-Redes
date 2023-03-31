from socket import *
import threading

serverName = '192.168.68.24'
serverPort = 12000
MAX_CONNECTIONS = 5

class ClientThread(threading.Thread):
    def __init__(self, threadID, status = "Ready"):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.status = status
    def run(self):
        #AF_INET indica que la red estará utilizando el protocolo IPv4
        #SOCK_STREAM indica que la red estará utilizando el protocolo TCP en vez de UDP
        clientSocket = socket(AF_INET, SOCK_STREAM)

        #Conecta el socket del cliente al socket del servidor. Aquí se realiza el three-way handshake
        clientSocket.connect((serverName,serverPort))

        filename = "1.txt"
        clientSocket.send(filename.encode())

        response = clientSocket.recv(1024).decode()

        if response == "Error: El archivo no existe":
            print("Error: El archivo no existe")
        else:
            with open("ArchivosRecibidos\Cliente"+str(self.threadID)+"-Prueba"+str(MAX_CONNECTIONS)+".txt", "wb") as file:
                data = clientSocket.recv(1024)
                while data:
                    file.write(data)
                    data = clientSocket.recv(1024)

            print(f"Archivo {filename} descargado exitosamente")

        clientSocket.close()

# Crear una lista de hilos para los 25 clientes concurrentes
threads = []
for i in range(MAX_CONNECTIONS):
    thread = ClientThread(i)
    threads.append(thread)

# Iniciar todos los hilos
for thread in threads:
    thread.start()

# Esperar a que todos los hilos terminen
for thread in threads:
    thread.join()

print("Todos los archivos han sido descargados exitosamente")