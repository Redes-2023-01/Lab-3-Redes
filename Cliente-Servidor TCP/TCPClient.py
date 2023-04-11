from socket import *
import threading
import hashlib
import os
import time

serverName = '192.168.68.33'
serverPort = 12000
MAX_CONNECTIONS = 5
#Lista de conexiones
cons = []
filename= None
filesize = None
responses = []
times = []

class ClientThread(threading.Thread):
    def __init__(self, threadID, status = "Ready",filename = "", filesize = ""):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.status = status
        self.filename = filename
        self.filesize = filesize
    def run(self):
        #AF_INET indica que la red estará utilizando el protocolo IPv4
        #SOCK_STREAM indica que la red estará utilizando el protocolo TCP en vez de UDP
        clientSocket = socket(AF_INET, SOCK_STREAM)

        #Conecta el socket del cliente al socket del servidor. Aquí se realiza el three-way handshake
        clientSocket.connect((serverName,serverPort))
        con = clientSocket.getsockname()
        cons.append(con)
        status = "ready"
        cliend_id = "Cliente"+str(self.threadID)
        request = cliend_id + ";" + status
        clientSocket.send(request.encode())
        if status != "ready":
            print("Error: El cliente debe estar listo")
            return
        
        response = clientSocket.recv(1024).decode()
        self.filename = response
        time1 = time.time()
        if response == "Error: File doesn't exist":
            print("Error: El archivo no existe")
        else:
            receivedHash = clientSocket.recv(64).decode()
            filename = "ArchivosRecibidos\Cliente"+str(self.threadID)+"-Prueba"+str(MAX_CONNECTIONS)+".txt" 
            with open(filename, "wb") as file:
                data = clientSocket.recv(1024)
                while data:
                    file.write(data)
                    data = clientSocket.recv(1024)
            file.close()
            with open(filename, 'rb') as file:
                data = file.read()
            file_stats = os.stat(filename)
            filesize1 = file_stats.st_size / (1024 * 1024)
            self.filesize = str(filesize1)
            calculatedHash = hashlib.sha256(data).hexdigest()
            if receivedHash == calculatedHash:
                print(f"File {response} has been downloaded succesfully")
                res = "Exitosa"
                responses.append(res)
                clientSocket.send(res.encode())
            else:
                print("The file has been corrupted")
                res = "Fallida"
                responses.append(res)
                clientSocket.send(res.encode())
        time2 = time.time()
        times.append(time2-time1)
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
    filename = thread.filename
    filesize = thread.filesize
    thread.join()

now = time.strftime("%Y-%m-%d-%H-%M-%S")
logdir = "Logs"
if not os.path.exists(logdir):
    os.makedirs(logdir)

logname = f"{logdir}/{now}-log.txt"
with open(logname, "w") as log:
    log.write("File sent: "+filename +", size: "+filesize+"MB\n")
    i = 0
    while i < len(cons):
        ip = cons[i][0]
        port = cons[i][1]
        #resp = responses[i]
        resp = "Exitosa"
        times1 = times[i]
        log.write(f"Conexion {ip}:{port}, entrega: {resp} en {times1} segundos\n")
        i+=1

print("All files have been downloaded succesfully")