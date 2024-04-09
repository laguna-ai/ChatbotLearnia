import logging
import azure.functions as func
from .SendWA import sendWA
from .List_Sharepoint import upload_list_sharepoint
from .request_manager import (
    setup_Meta_webhook,
    manage_WA_status,
    manage_WA_format,
    get_personal_info,
)
from .conversation_manager import respond_message, update_history
from .blob_storage import get_blobs, prepare_history, update_blobs


def main(req: func.HttpRequest) -> func.HttpResponse:

    # Only used in the configuration of Meta for developers
    setup_response = setup_Meta_webhook(req)
    if setup_response:
        return setup_response

    # Get JSON of data
    info = req.get_json()
    value = info["entry"][0]["changes"][0]["value"]
    logging.info(f'## JSON CONTENTS ## : {info}')

    # Managment of status messages from WA (delivered, sent, received, etc).
    status_response = manage_WA_status(value)
    if status_response:
        return status_response

    # Management of message format (discard other than text)
    messages = value["messages"][0]
    format_response = manage_WA_format(messages)
    if format_response:
        return status_response

    tel, message, name = get_personal_info(messages, value)

    blob, blob_usage = get_blobs(tel)

    History, Usage, welcome = prepare_history(blob, blob_usage)

    respuesta_texto, respuesta_uso, History = respond_message(message, History)

    sendWA(respuesta_texto, tel, welcome)

    logging.info("Usuario: %s", message)
    logging.info("Chatbot: %s", respuesta_texto)

    # History, Usage = update_history(respuesta_texto, respuesta_uso, History, Usage)

    # update_blobs(blob, blob_usage, History, Usage)

    update_blobs(blob, blob_usage, message, respuesta_texto, respuesta_uso)

    #upload_list_sharepoint(tel, name, message, respuesta_texto)

    return func.HttpResponse("Success", status_code=200)
