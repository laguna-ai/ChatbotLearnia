import logging
import azure.functions as func
import json
from .index_query import get_docs
from .SysPrompt import sysPrompt
from .Chat_Response import get_completion_from_messages, plantilla_sys
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    # Get JSON of data
    request_json = req.get_json()
    logging.info("## JSON CONTENTS ##: %s", str(request_json))
    prompt = request_json["text"]

    try:
        history = request_json["sessionInfo"]["parameters"]["context"]
    except KeyError:
        history = sysPrompt
        parameters = ["nombre", "procedencia", "organizacion"]
        questions = [
            "¿Cuál es tu nombre?",
            "¡Gracias! ¿De qué país/ciudad nos escribes?",
            "¿A qué Universidad / Empresa representas?",
        ]
        for i, p in enumerate(parameters):
            history.append({"role": "assistant", "content": questions[i]})
            var_p = request_json["sessionInfo"]["parameters"][p]
            history.append({"role": "user", "content": var_p})
        history.append(
            {
                "role": "assistant",
                "content": "Gracias por compartirnos tus datos. ¿En qué te puedo ayudar?",
            }
        )

    history.append({"role": "user", "content": prompt})

    # Respuesta del bot, añadir prompt_usuario y respuesta_bot al historial
    context = get_docs(prompt)
    history.append({"role": "system", "content": plantilla_sys(context)})

    try:
        respuesta = get_completion_from_messages(history)[0]
        history.pop()  # delete the context prompt
        history.append({"role": "assistant", "content": respuesta})

    except HttpResponseError as e:
        respuesta = "Error en el llamado a openAI: " + str(e)

    # logging.info(f'## Historial ## : {History}')

    logging.info("Usuario: %s", prompt)
    logging.info("Chatbot: %s", respuesta)

    # Construimos la respuesta JSON manualmente y la retornamos usando func.HttpResponse
    response_body = json.dumps(
        {
            "sessionInfo": {
                "parameters": {
                    "context": history,
                }
            },
            "fulfillmentResponse": {"messages": [{"text": {"text": [respuesta]}}]},
        }
    )

    return func.HttpResponse(
        body=response_body, status_code=200, mimetype="application/json"
    )
