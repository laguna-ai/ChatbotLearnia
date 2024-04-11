import pytest
import json
from simulation.user_messages import basic_number
from Postgres.postgres import create_postgres_connection as get_connection
from simulation.async_simulation import main as simulate_async_messages
import asyncio
from azure.core.exceptions import ResourceNotFoundError
from azure.cosmos import CosmosClient, exceptions
import os
n_users = 5
n_iterations = 5
endpoint = "http://localhost:7071/api/Learnia_whatsapp"
# endpoint="https://chatbot-webhooks.azurewebsites.net/api/Learnia_whatsapp"
expected_count = 2 * n_iterations + 1



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

def test_mensajes_enviados_por_usuario():
    # Generar todos los números de teléfono
    telefonos = [f"{basic_number}{i}" for i in range(n_users)] 

    # Conectar a la base de datos
    conn = get_connection()
  
    with conn.cursor() as cur:
        # Ejecutar una sola consulta usando ANY para obtener los conteos de todos los números
        cur.execute("""
            SELECT history
            FROM sessions 
            WHERE id = ANY(%s) 
        """, (telefonos,))
        results = cur.fetchall()

        # Asegurar que cada teléfono tenga el conteo esperado
        i=0
        for r in results:
            history=r[0]
            count=len(history)
            
            assert count == expected_count, f"El conteo de mensajes esperado para {i} era {expected_count}, pero se encontró {count}"
            i+=1
        
        consulta_borrado = "DELETE FROM sessions WHERE id = ANY(%s);"
        cur.execute(consulta_borrado, (telefonos,))
        conn.commit()