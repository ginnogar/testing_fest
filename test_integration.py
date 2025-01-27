# Description: Pruebas de integración para el servidor de chat.
# Prubas de integracion que validen la interaccion entre componentes.
# Simula escenarios reales como la desconexion de clientes y mensajes simultaneos.

from unittest.mock import Mock
from server import broadcast, clients, remove_client

# Mensajes enviados a multiples clientes. 
# Se espera que el mensaje sea enviado a todos los clientes excepto al emisor.
def test_multiple_clients_message():
    """Simula múltiples clientes conectados y verifica que los mensajes se distribuyan correctamente."""
    client1 = Mock()
    client2 = Mock()
    client3 = Mock()

    # Añadir los clientes a la lista de clientes
    clients.extend([client1, client2, client3])
    
    message = b"Hola, todos!"

    # Ejecutar broadcast (enviar el mensaje a todos excepto al emisor)
    broadcast(message, client1)

    # Verificar que el mensaje fue enviado a los otros clientes
    client2.send.assert_called_once_with(message)
    client3.send.assert_called_once_with(message)

    # Verificar que el cliente 1 no recibe el mensaje
    client1.send.assert_not_called()

# Implementa pruebas que simulen desconexiones inesperadas. 
# Manejo de desconexión de clientes.
def test_client_disconnect():
    """Simula la desconexión de un cliente mientras otros siguen activos."""
    client1 = Mock()
    client2 = Mock()

    # Añadir los clientes
    clients.extend([client1, client2])

    # Simulamos que client1 se desconecta
    clients.remove(client1)
    client1.close()

    # Enviar mensaje de client2
    message = b"Hola desde client2"
    broadcast(message, client2)

    # Verificar que el mensaje fue enviado a client2 (no a client1 que ya está desconectado)
    client2.send.assert_called_once_with(message)

    # Verificar que client1 no recibió el mensaje
    client1.send.assert_not_called()

# Mensajes privados entre clientes.
# Se espera que el mensaje sea enviado solo al cliente destinatario.
def test_multiple_simultaneous_messages():
    """Simula el envío de mensajes simultáneos por parte de varios clientes."""
    client1 = Mock()
    client2 = Mock()
    client3 = Mock()

    # Añadir los clientes
    clients.extend([client1, client2, client3])

    # Mensajes de cada cliente
    message1 = b"Mensaje de client1"
    message2 = b"Mensaje de client2"
    message3 = b"Mensaje de client3"

    # Simulamos que todos los clientes envían un mensaje
    broadcast(message1, client1)
    broadcast(message2, client2)
    broadcast(message3, client3)

    # Verificar que cada cliente reciba los mensajes enviados por los otros
    client2.send.assert_any_call(message1)  # Cliente 2 recibe mensaje de Cliente 1
    client3.send.assert_any_call(message1)  # Cliente 3 recibe mensaje de Cliente 1
    client1.send.assert_any_call(message2)  # Cliente 1 recibe mensaje de Cliente 2
    client3.send.assert_any_call(message2)  # Cliente 3 recibe mensaje de Cliente 2
    client1.send.assert_any_call(message3)  # Cliente 1 recibe mensaje de Cliente 3
    client2.send.assert_any_call(message3)  # Cliente 2 recibe mensaje de Cliente 3
