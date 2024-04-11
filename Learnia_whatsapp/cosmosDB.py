from azure.cosmos import CosmosClient, exceptions
from RAG.SysPrompt import sysPrompt
import os
import json
import copy

def get_cosmos_container():
    """
    Inicializa y devuelve un cliente de contenedor de Azure Cosmos DB.
    """

    ENDPOINT = "https://learnia-cosmos.documents.azure.com:443/"
    KEY = os.environ["COSMOS_DB_KEY"]
    DATABASE_NAME = "learniaDB"
    CONTAINER_NAME = "sessions"

    # Inicializa el cliente de Cosmos DB con el endpoint y la llave proporcionados
    client = CosmosClient(ENDPOINT, KEY)

    # Obtiene el cliente de la base de datos específica
    database = client.get_database_client(DATABASE_NAME)

    # Obtiene el cliente del contenedor específico
    container = database.get_container_client(CONTAINER_NAME)

    return container


def find_or_create_session(container, tel):
    welcome = False
    try:
        # Intenta buscar directamente el ítem por su id.
        session = container.read_item(item=tel, partition_key="active")
    except exceptions.CosmosResourceNotFoundError:
        # El ítem no existe, así que procedemos a crearlo.
        welcome = True
        session = {
            "id": tel,
            "history": copy.deepcopy(sysPrompt),
            "status": "active"
        }
        container.create_item(body=session)
    except exceptions.CosmosHttpResponseError as e:
        print(f'An error occurred: {e}')
        return None, None
    
    return session["history"], welcome

def update_session(container,tel, new_messages):
    try:
        # Encuentra la sesión específica para actualizar
        session = container.read_item(item=tel, partition_key="active")
        # Actualiza el campo 'history' con los nuevos mensajes
        session['history'].extend(new_messages)
        container.replace_item(item=session['id'], body=session)
    except exceptions.CosmosHttpResponseError as e:
        print(f'An error occurred: {e}')