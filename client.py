# Description: Cliente de chat en tiempo real con sockets en Python.
# El cliente se conecta al servidor y puede enviar mensajes a todos los usuarios conectados.
import socket
import threading

username = input("Ingresa tu username: ")

host = '127.0.0.1'
port = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def receive_message():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "@username":
                client.send(username.encode("utf-8"))
            else:
                print(message)
        except:
            print("Ocurrió un error. Desconectado del servidor.")
            client.close()
            break

def write_message():
    while True:
        message = input('')
        if message.startswith('/'):
            client.send(message.encode('utf-8'))
        else:
            message = f"{username}: {message}"
            try:
                client.send(message.encode('utf-8'))
            except:
                print("Ocurrió un error al enviar el mensaje.")
                client.close()
                break

receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

write_thread = threading.Thread(target=write_message)
write_thread.start()