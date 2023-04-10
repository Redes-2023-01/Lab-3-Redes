from socket import *
import threading
import hashlib

serverName = '192.168.68.37'
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

        status = "ready"
        cliend_id = "Cliente"+str(self.threadID)
        request = cliend_id + ";" + status
        clientSocket.send(request.encode())

        if status != "ready":
            print("Error: El cliente debe estar listo")
            return

        response = clientSocket.recv(1024).decode()

        if response == "Error: File doesn't exist":
            print("Error: El archivo no existe")
        else:
            receivedHash = clientSocket.recv(1024).decode()
            filename = "ArchivosRecibidos\Cliente"+str(self.threadID)+"-Prueba"+str(MAX_CONNECTIONS)+".txt" 
            with open(filename, "wb") as file:
                data = clientSocket.recv(1024)
                while data:
                    file.write(data)
                    data = clientSocket.recv(1024)
            file.close()
            with open(filename, 'rb') as file:
                data = file.read()
            calculatedHash = hashlib.sha256(data).hexdigest()
            print(f"Hash recibido: {receivedHash}")
            print(f"Hash calculado: {calculatedHash}")
            if receivedHash == calculatedHash:
                print(f"File {response} has been downloaded succesfully")
                clientSocket.send("Exitosa".encode())
            else:
                print("The file has been corrupted")
                clientSocket.send("Fallida".encode())

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

print("All files have been downloaded succesfully")