# Lab-3-Redes

## Pasos generales

1. Descargar una imagen de escritorio de linux con distribución ubuntu 20.04 o 18.04 y correr una máquina virtual desde VMWare con esto
2. Correr los comandos "sudo apt update" y "sudo apt -y install net-tools" para poder obtener las direcciones ip de las máquinas virtuales
3. Desde la pestaña de VMWare pasar la configuración de conexión de NAT a Bridged para que la máquina virtual tome su propia dirección virtual y no use la del ordenador
4. Con el comando truncate crear los archivos necesarios (truncate -s 1M 1.txt)

## Para correr Cliente/Servidor UDP (Java)

1. Crear los siguientes archivos "100MB_file.bin" de 100MB y "250MB_file.bin" de 250MB y guardar ambos archivos en la carpeta Files.
2. Correr UDPServer, al correrlo preguntara que archivo se desea enviar, elegir ocion 1 o 2 y continuar.
3. En el codigo de UDPClient en la linea 28, cambiar "192.168.10.6" por el ip del servidor, la linea de codigo es la siguiente "InetAddress serverIPAddress = InetAddress.getByName("192.168.10.6");"
4. Correr UDPClient, al correrlo preguntara cuantos cleintes se quieren crear, elegir entre un numero del 1 al 25.

## Para correr Cliente/Servidor TCP (python)

1. Crear los archivos "100.txt" y "250.txt": truncate -s 100M 100.txt
2. Descargar python a la máquina virtual (puede ser entre 3.7 y 3.10)
3. (Preferiblemente) Instalar Visual Studio Code en la máquina del servidor y clonar el repositorio o descargar el archivo TCPserver.py
4. Consultar la dirección de la máquina virtual con ifconfig
5. Correr el archivo de python TCPserver.py desde la terminal de la VM
6. Cambiar la dirección ip a la que se conecta el cliente para que coincida con la dirección actual de la máquina virtual
7. Correr el archivo TCPclient.py desde la máquina propia
8. Revisar los archivos guardados por el cliente y los logs creados tanto por el servidor como por el cliente
