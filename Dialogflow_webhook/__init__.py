import logging
import azure.functions as func
from RAG.conversation_manager import respond_message
from Postgres.postgres import create_postgres_connection, upsert_session_history
from .request_manager import get_personal_info, prepare_history, create_webhook_response


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    request_json = req.get_json()
    prompt, session_id = get_personal_info(request_json)
    history = prepare_history(request_json)

    with create_postgres_connection() as conn:  # pylint: disable=E1129
        respuesta, _ = respond_message(conn, prompt, history)
        logging.info("Usuario: %s", prompt)
        logging.info("Chatbot: %s", respuesta)
        upsert_session_history(conn, session_id, history)

    res = create_webhook_response(respuesta, history)

    return res
