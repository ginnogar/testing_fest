# Aca se implementan las pruebas unitarias para el servidor de chat. 
# Con el fin de verificar que las funciones del servidor se comporten como se espera.
# Usa unittest y mock para simular y verificar el comportamiento de los clientes.

import unittest
from unittest.mock import Mock
from server import broadcast, remove_client, list_users, send_private_message, handle_command, clients, usernames

class TestServer(unittest.TestCase):

    def setUp(self):
        """Preparar un entorno limpio antes de cada prueba."""
        clients.clear()
        usernames.clear()

    # Verifica que los mensajes se envían correctamente.
    def test_broadcast(self):
        """Verificar que broadcast envía mensajes a todos los clientes excepto al emisor."""
        client1 = Mock()
        client2 = Mock()
        client3 = Mock()

        clients.extend([client1, client2, client3])
        message = b"Hola a todos"

        # Ejecutar broadcast
        broadcast(message, client1)

        # Verificar que otros clientes recibieron el mensaje
        client2.send.assert_called_once_with(message)
        client3.send.assert_called_once_with(message)

        # Verificar que el emisor no recibió nada
        client1.send.assert_not_called()

    # Asegura que los clientes se eliminan de la lista.
    def test_remove_client(self):
        """Verificar que remove_client elimina al cliente y notifica a los demás."""
        client = Mock()
        clients.append(client)
        usernames.append("usuario1")

        # Eliminar cliente
        remove_client(client)

        # Verificar que el cliente fue eliminado
        self.assertNotIn(client, clients)
        self.assertNotIn("usuario1", usernames)

        # Verificar que el cliente fue cerrado
        client.close.assert_called_once()

    # Verificar que los demás clientes fueron notificados
    def test_list_users(self):
        """Verificar que list_users envía la lista de usuarios conectados al cliente."""
        client = Mock()
        usernames.extend(["usuario1", "usuario2"])

        # Ejecutar list_users
        list_users(client)

        # Verificar que la lista de usuarios fue enviada correctamente
        expected_message = "Usuarios conectados:\nusuario1\nusuario2".encode('utf-8')
        client.send.assert_called_once_with(expected_message)

    # Verificar que los mensajes privados se envían correctamente.
    def test_send_private_message(self):
        """Verificar que send_private_message envía un mensaje privado al destinatario."""
        sender = Mock()
        receiver = Mock()
        clients.extend([sender, receiver])
        usernames.extend(["sender_user", "receiver_user"])

        command = "/msg receiver_user Hola"
        send_private_message(command, sender)

        # Verificar que el receptor recibió el mensaje privado
        expected_message = "Mensaje privado de sender_user: Hola".encode('utf-8')
        receiver.send.assert_called_once_with(expected_message)

        # Verificar que el emisor no recibió ningún mensaje
        sender.send.assert_not_called()

    # Verificar que los comandos validos e invalidos son manejados correctamente.
    def test_unknown_command(self):
        """Verificar que los comandos desconocidos envían un mensaje de error al cliente."""
        client = Mock()

        # Comando no reconocido
        handle_command("/unknown", client)

        # Verificar el mensaje de error
        client.send.assert_called_once_with("Comando no reconocido.".encode('utf-8'))

if __name__ == '__main__':
    unittest.main()
