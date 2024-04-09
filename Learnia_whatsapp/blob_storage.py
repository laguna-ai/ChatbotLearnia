from azure.storage.blob import BlobServiceClient
import json
from azure.core.exceptions import ResourceNotFoundError
import logging
from RAG.SysPrompt import sysPrompt
import copy
from RAG.calculo_costos import openai_api_calculate_cost

################################################################################################
#########      Crear una conexión con  almacenamiento blob  ####################################
################################################################################################
connect_str = "DefaultEndpointsProtocol=https;AccountName=historialconversaciones;AccountKey=1IyXT4sLXaaDhLf8Ljp6rxUO9juwpB1bBkdOiqC+9vyqeGTdMr7KpVc6PgZcQc+S4GWkMpkeRP+++AStiJs2AQ==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = "conversacioneslearnia"
container_client = blob_service_client.get_container_client(container_name)
#################################################################################################


def get_blobs(tel):
    blob = container_client.get_blob_client(tel + ".txt")
    blob_usage = container_client.get_blob_client(tel + "$.txt")
    return blob, blob_usage


def prepare_history(blob, blob_usage):
    try:
        History = json.loads(blob.download_blob(encoding="utf-8").readall())
    except ResourceNotFoundError as e:
        History = copy.deepcopy(sysPrompt)
        Usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_cost": 0}
        welcome = True
        logging.info("No hay historial en blob: %s", e)
        upload_blobs(blob, blob_usage, History, Usage)
    else:
        welcome = False

    return History, welcome


# def update_blobs(blob, blob_usage, History, Usage):
#     blob.upload_blob(json.dumps(History), overwrite=True)
#     blob_usage.upload_blob(json.dumps(Usage), overwrite=True)


def update_blobs(blob, blob_usage, message, respuesta_texto, respuesta_uso):

    History = json.loads(blob.download_blob(encoding="utf-8").readall())
    Usage = json.loads(blob_usage.download_blob(encoding="utf-8").readall())

    History.append({"role": "user", "content": message})
    History.append({"role": "assistant", "content": respuesta_texto})
    Usage["prompt_tokens"] += respuesta_uso.prompt_tokens
    Usage["completion_tokens"] += respuesta_uso.completion_tokens
    Usage["total_cost"] += openai_api_calculate_cost(respuesta_uso)

    upload_blobs(blob, blob_usage, History, Usage)


def upload_blobs(blob, blob_usage, History, Usage):
    blob.upload_blob(json.dumps(History), overwrite=True)
    blob_usage.upload_blob(json.dumps(Usage), overwrite=True)
