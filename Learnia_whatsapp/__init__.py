import logging
import azure.functions as func
from .SendWA import sendWA
from .request_manager import (
    setup_Meta_webhook,
    manage_WA_status,
    manage_WA_format,
    get_personal_info,
)
from .conversation_manager import respond_message
from .postgres import create_postgres_connection, find_or_create_session, update_session


def main(req: func.HttpRequest) -> func.HttpResponse:

    # Only used in the configuration of Meta for developers
    setup_response = setup_Meta_webhook(req)
    if setup_response:
        return setup_response

    # Get JSON of data
    info = req.get_json()
    value = info["entry"][0]["changes"][0]["value"]
    # logging.info(f'## JSON CONTENTS ## : {info}')

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

    conn = create_postgres_connection()

    History, welcome = find_or_create_session(conn,tel)
    
    respuesta_texto, respuesta_uso, History = respond_message(message, History)

    sendWA(respuesta_texto, tel, welcome)

    logging.info("Usuario: %s", message)
    logging.info("Chatbot: %s", respuesta_texto)
    
    update_session(conn, tel, History[-2:])
    
    conn.close()

    return func.HttpResponse("Success", status_code=200)
