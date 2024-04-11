import pytest
import json
from simulation.user_messages import basic_number
from Learnia_whatsapp.cosmosDB import get_cosmos_container
from simulation.async_simulation import main as simulate_async_messages
import asyncio
from azure.core.exceptions import ResourceNotFoundError
from azure.cosmos import CosmosClient, exceptions
import os
n_users = 1
n_iterations = 2
endpoint = "http://localhost:7071/api/Learnia_whatsapp"
# endpoint="https://chatbot-webhooks.azurewebsites.net/api/Learnia_whatsapp"
expected_count = 2 * n_iterations + 1



ENDPOINT = "https://learnia-cosmos.documents.azure.com:443/"
#KEY = os.environ["COSMOS_DB_KEY"]
DATABASE_NAME = "learniaDB"
CONTAINER_NAME = "sessions"


# Inicializa el cliente de Cosmos DB con el endpoint y la llave proporcionados
client = CosmosClient(ENDPOINT, KEY)
# Obtiene el cliente de la base de datos específica
database = client.get_database_client(DATABASE_NAME)
# Obtiene el cliente del contenedor específico
container = database.get_container_client(CONTAINER_NAME)

# Función de limpieza para ser llamada después de cada prueba


# def limpiar_archivos():
#     for i in range(n_users):
#         archivo_usuario = f"{basic_number}{i}.txt"
#         archivo_usuario_tmp = f"{basic_number}{i}$.txt"
#         try:
#             blob = container_client.get_blob_client(archivo_usuario)
#             blob.delete_blob()
#             blob_tmp = container_client.get_blob_client(archivo_usuario_tmp)
#             blob_tmp.delete_blob()
#         except ResourceNotFoundError as e:
#             print(f"Error al limpiar el blob: {e}")


# Fixture para simular mensajes antes de todas las pruebas y limpiar después


@pytest.fixture(scope="session", autouse=True)
def preparar_y_limpiar():
    # Ejecutar simulación antes de las pruebas
    asyncio.run(simulate_async_messages(n_users, n_iterations, endpoint))
    # Esperar a que todas las pruebas se completen
    yield
    # Ejecutar limpieza después de todas las pruebas
    # limpiar_archivos()


# Prueba para verificar el conteo de mensajes por usuario
#container=get_cosmos_container()

@pytest.mark.parametrize("user_index", range(n_users))
def test_mensajes_enviados_por_usuario(user_index):
    # Conteo de mensajes para el usuario actual
    tel = f"{basic_number}{user_index}"
    
    
   
    try:
        session = container.read_item(item=tel, partition_key="active")
        history = session["history"]
        real_count = len(history)
    except ResourceNotFoundError as e:
        real_count = 0
        print(f"Error al contar mensajes para {tel}: {e}")

    assert (
        real_count == expected_count
    ), f"El conteo de mensajes esperado para {tel} era {expected_count}, pero se encontró {real_count}"
