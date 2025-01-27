# Description: Servidor de chat que permite a los clientes conectarse y enviar mensajes a otros usuarios.
# El servidor maneja comandos especiales como /list para listar usuarios, /quit para desconectarse y /msg para enviar mensajes privados.
import socket
import threading

host = '127.0.0.1'
port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

print("Servidor de chat iniciado en el puerto 12345. Esperando conexiones...")

clients = []
usernames = []

def broadcast(message, _client):
    """Envía un mensaje a todos los clientes excepto al emisor."""
    for client in clients:
        if client != _client:
            try:
                client.send(message)
            except:
                client.close()
                remove_client(client)

def handle_message(client):
    """Maneja los mensajes recibidos de los clientes."""
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                if not validate_message(message):
                    client.send("Mensaje inválido: vacío o demasiado largo.".encode('utf-8'))
                    continue
                if message.startswith('/'):
                    handle_command(message, client)
                else:
                    broadcast(message.encode('utf-8'), client)
            else:
                remove_client(client)
                break
        except:
            remove_client(client)
            break

def handle_command(command, client):
    """Maneja los comandos del chat (listado, desconectar, mensajes privados)."""
    if command.startswith('/list'):
        list_users(client)
    elif command.startswith('/quit'):
        remove_client(client)
    elif command.startswith('/msg'):
        send_private_message(command, client)
    else:
        client.send("Comando no reconocido.".encode('utf-8'))

def list_users(client):
    """Envía la lista de usuarios conectados al cliente."""
    user_list = "Usuarios conectados:\n" + "\n".join(usernames)
    client.send(user_list.encode('utf-8'))

def send_private_message(command, client):
    """Envía un mensaje privado a otro usuario."""
    parts = command.split(' ', 2)
    if len(parts) < 3:
        client.send("Uso: /msg <usuario> <mensaje>".encode('utf-8'))
        return
    target_username = parts[1]
    message = parts[2]
    if target_username in usernames:
        target_index = usernames.index(target_username)
        target_client = clients[target_index]
        target_client.send(f"Mensaje privado de {usernames[clients.index(client)]}: {message}".encode('utf-8'))
    else:
        client.send("Usuario no encontrado.".encode('utf-8'))

# Manejo de desconexión de clientes.
def remove_client(client):
    """Elimina un cliente desconectado de la lista de clientes."""
    if client in clients:
        index = clients.index(client)
        username = usernames[index]
        broadcast(f'ChatBot: {username} desconectado'.encode('utf-8'), client)
        clients.remove(client)
        usernames.remove(username)
        client.close()

# Validar que el mensaje no esté vacío ni exceda los 200 caracteres
# para evitar problemas con el envío de mensajes.
# Se utilizo la TDD para implementar la función validate_message
def validate_message(message):
    """Valida que el mensaje no esté vacío ni exceda los 200 caracteres."""
    return bool(message) and len(message) <= 200

def receive_connections():
    """Recibe conexiones de clientes y les asigna un nombre de usuario."""
    while True:
        client, address = server_socket.accept()
        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode('utf-8')

        clients.append(client)
        usernames.append(username)

        print(f'{username} se conectó desde {str(address)}')

        message = f"ChatBot: {username} entró al chat!".encode("utf-8")
        broadcast(message, client)
        client.send("Conectado al servidor".encode("utf-8"))

        thread = threading.Thread(target=handle_message, args=(client,))
        thread.start()

if __name__ == "__main__":
    print("Servidor de chat iniciado en el puerto 12345. Esperando conexiones...")
    receive_connections()
