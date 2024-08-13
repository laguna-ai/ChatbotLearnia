import logging
import azure.functions as func
from .SendWA import sendWA
from .request_manager import (
    setup_Meta_webhook,
    manage_WA_status,
    manage_WA_format,
    get_personal_info,
)
from RAG.conversation_manager import respond_message
from Postgres.postgres import (
    create_postgres_connection,
    find_or_create_session,
    update_session,
)


def main(req: func.HttpRequest) -> func.HttpResponse:

    # Only used in the configuration of Meta for developers
    setup_response = setup_Meta_webhook(req)
    if setup_response:
        return setup_response

    # Get JSON of data
    info = req.get_json()
    value = info["entry"][0]["changes"][0]["value"]
    logging.info("## JSON CONTENTS ## : %s", info)

    # Managment of status messages from WA (delivered, sent, received, etc).
    status_response = manage_WA_status(value)
    if status_response:
        return status_response

    # Management of message format (discard other than text)
    messages = value["messages"][0]
    format_response = manage_WA_format(messages)
    if format_response:
        return format_response

    tel, message = get_personal_info(messages)

    with create_postgres_connection() as conn:  # pylint: disable=E1129
        History, welcome = find_or_create_session(conn, tel)
        respuesta_texto, new_messages = respond_message(conn, message, History)
        sendWA(respuesta_texto, tel, welcome)
        # logging.info("Usuario: %s", message)
        # logging.info("Chatbot: %s", respuesta_texto)
        update_session(conn, tel, new_messages)

    return func.HttpResponse("Success", status_code=200)
