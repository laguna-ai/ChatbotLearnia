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
from openai.types.completion_usage import CompletionUsage


# autenticamos y creamos columnas en sharepoint
auth = auth_sharepoint()

################################################################################################
#########      Crear una conexión con  almacenamiento blob  ####################################
################################################################################################
connect_str = "DefaultEndpointsProtocol=https;AccountName=historialconversaciones;AccountKey=1IyXT4sLXaaDhLf8Ljp6rxUO9juwpB1bBkdOiqC+9vyqeGTdMr7KpVc6PgZcQc+S4GWkMpkeRP+++AStiJs2AQ==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = "conversacioneslearnia"
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
    # número de interacciones previas
    n= len(History)
    # respuestas de texto y uso
    if n==2:
        respuesta_texto, respuesta_uso = respuesta_sin_costo("¿Cuál es tu nombre?")
    elif n==4:
        respuesta_texto, respuesta_uso = respuesta_sin_costo("¡Gracias! ¿De qué país/ciudad nos escribes?")
    elif n==6:
        respuesta_texto, respuesta_uso = respuesta_sin_costo("¿A qué Universidad / Empresa representas?")
    elif n==8:
        respuesta_texto, respuesta_uso = respuesta_sin_costo("Gracias por compartirnos tus datos. ¿En qué te puedo ayudar?")
    else:
        context = get_docs(message)
        History.append({"role": "system", "content": plantilla_sys(context)})

        try:
            respuesta = get_completion_from_messages(History)
            respuesta_texto = respuesta[0]
            respuesta_uso = respuesta[1]
            
        except HttpResponseError as e:
            respuesta_texto, respuesta_uso = respuesta_sin_costo("Error en el llamado a openAI: " + str(e))
        History.pop()  # delete the context prompt
    
    # se envia la respuesta a Whatsapp
    sendWA(respuesta_texto, tel, welcome)
    
    logging.info("Usuario: %s", message)
    logging.info("Chatbot: %s", respuesta_texto)
    
    History.append({"role": "assistant", "content": respuesta_texto})
    Usage["prompt_tokens"] += respuesta_uso.prompt_tokens
    Usage["completion_tokens"] += respuesta_uso.completion_tokens
    Usage["total_cost"] += openai_api_calculate_cost(respuesta_uso)

    # actualizamos blob
    blob.upload_blob(json.dumps(History), overwrite=True)
    blob_usage.upload_blob(json.dumps(Usage), overwrite=True)
    # actualizamos lista de sharepoint
    upload_list_sharepoint(tel, name, message, respuesta_texto)
   
    return func.HttpResponse("Success", status_code=200)



def respuesta_sin_costo(texto):
    uso = CompletionUsage(
        prompt_tokens=0, completion_tokens=0, total_tokens=0
        )
    return texto, uso