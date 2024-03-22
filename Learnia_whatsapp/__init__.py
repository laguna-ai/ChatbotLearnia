import logging
import azure.functions as func
from .SendWA import sendWA
import json
from .index_query import get_docs
from azure.storage.blob import BlobServiceClient
from .SysPrompt import sysPrompt
from .Chat_Response import get_completion_from_messages, plantilla_sys
from .List_Sharepoint import upload_list_sharepoint
from .Autenticacion_sharepoint import auth_sharepoint
from .calculo_costos import openai_api_calculate_cost
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError

# autenticamos y creamos columnas en sharepoint
auth = auth_sharepoint()

################################################################################################
#########      Crear una conexión con  almacenamiento blob  ####################################
################################################################################################
connect_str = "DefaultEndpointsProtocol=https;AccountName=historialconversaciones;AccountKey=1IyXT4sLXaaDhLf8Ljp6rxUO9juwpB1bBkdOiqC+9vyqeGTdMr7KpVc6PgZcQc+S4GWkMpkeRP+++AStiJs2AQ==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = "conversacioneslernia"
container_client = blob_service_client.get_container_client(container_name)
#################################################################################################


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")
    # Webhook setup in Meta via GET
    if req.method == "GET":
        if req.params.get("hub.verify_token") == "Hola":
            return func.HttpResponse(req.params.get("hub.challenge"))
        else:
            return func.HttpResponse("Error de autenticación")

    # Get JSON of data
    info = req.get_json()
    # logging.info(f'## JSON CONTENTS ## : {info}')

    # Managment of status messages from WA (delivered, sent, received, etc).
    value = info["entry"][0]["changes"][0]["value"]

    if "statuses" in value:  # si es un mensaje de status lanzamos status 200
        return func.HttpResponse("Success", status_code=200)
    elif "messages" in value:
        messages = value["messages"][0]
        message_type = messages["type"]
        # si es reacción, documento, audio, o video, lo omitimos y lanzamos status 200 para evitar errores
        if message_type in [
            "reaction",
            "document",
            "image",
            "audio",
            "video",
            "sticker",
        ]:
            return func.HttpResponse("Success", status_code=200)

    # Get phone and prompt from user
    tel = messages["from"]
    message = messages["text"]["body"]
    name = value["contacts"][0]["profile"]["name"]

    ################################################################################################
    #####################        Prepare history            ########################################
    blob = container_client.get_blob_client(tel + ".txt")
    blob_usage = container_client.get_blob_client(tel + "$.txt")
    try:
        History = json.loads(blob.download_blob(encoding="utf-8").readall())
        Usage = json.loads(blob_usage.download_blob(encoding="utf-8").readall())
    except ResourceNotFoundError as e:
        History = sysPrompt
        Usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_cost": 0}
        welcome = True
        logging.info("No hay historial en blob: %s", e)

    else:
        welcome = False
    History.append({"role": "user", "content": message})
    #############################################################################################
    ######      Respuesta del bot, añadir prompt_usuario y respuesta_bot al historial    ###########
    context = get_docs(message)
    History.append({"role": "system", "content": plantilla_sys(context)})

    try:
        respuesta = get_completion_from_messages(History)
        respuesta_texto = respuesta[0]
        respuesta_uso = respuesta[1]
        History.pop()  # delete the context prompt
        History.append({"role": "assistant", "content": respuesta_texto})
        Usage["prompt_tokens"] += respuesta_uso.prompt_tokens
        Usage["completion_tokens"] += respuesta_uso.completion_tokens
        Usage["total_cost"] += openai_api_calculate_cost(respuesta_uso)

    except HttpResponseError as e:
        respuesta = "Error en el llamado a openAI: " + str(e)

    # logging.info(f'## Historial ## : {History}')

    logging.info("Usuario: %s", message)
    logging.info("Chatbot: %s", respuesta)

    # actualizamos blob
    blob.upload_blob(json.dumps(History), overwrite=True)
    blob_usage.upload_blob(json.dumps(Usage), overwrite=True)
    # actualizamos lista de sharepoint
    upload_list_sharepoint(tel, name, message, respuesta_texto)
    # se envia la respuesta a Whatsapp
    sendWA(respuesta_texto, tel, welcome)
    return func.HttpResponse("Success", status_code=200)
