# Chat Application with Testing

Este proyecto es una aplicación de chat en tiempo real construida con Python. Admite múltiples clientes, mensajería privada, 
y varios comandos como enumerar usuarios y desconectarse. El proyecto se centra en técnicas de prueba robustas, 
para garantizar confiabilidad y corrección.

## Key Testing Features

- Pruebas unitarias para todas las funcionalidades críticas del servidor (difusión de mensajes, manejo de usuarios, comandos).
- Pruebas de integración para interacciones entre múltiples clientes y el servidor.
- Simulaciones de desconexiones de clientes y mensajería simultánea.
- Enfoque de desarrollo basado en pruebas (TDD) para validar reglas de mensajes.

## Test Structure

1. **Unit Tests:**  

   Localizate en "test_server.py", estos tests valida funciones individuales del servidor como: 

   - Broadcasting messages.
   - Removing clients.
   - Handling commands like `/list`, `/quit`, and `/msg`.

2. **Integration Tests:** 
   Encuentra "test_integration.py" estos tests garantizan que todo el sistema funcione como se espera mediante la simulación:

   - Multiple clients connected to the server.
   - Client disconnections and server behavior.
   - Simultaneous messaging between clients.

## Running the Tests

1. **Run all tests**
   
   Ejecute todos los archivos de prueba (pruebas unitarias y de integración):
   
   pytest

3. **Run specific test file**
   
   Ejecute un archivo de prueba específico para centrarse en un conjunto particular de pruebas:
   
   pytest test_server.py   # Run unit tests
   
   pytest test_integration.py   # Run integration tests

5. **Run with verbose output**
   
   Mostrar resultados de prueba detallados:
   
   pytest -v

Testing Tools and Techniques Used

- Testing Frameworks:
  - unittest for unit tests.
  - pytest for integration tests.

- Mocking:
  Se utiliza para simular interacciones cliente-servidor sin requerir conexiones de red reales.

- Test-Driven Development (TDD):
  Implementa la función validar_message escribiendo pruebas primero y luego la funcionalidad real.
