from azure.core.exceptions import HttpResponseError
from .index_query import get_docs
from .Chat_Response import get_completion_from_messages, plantilla_sys


def respond_message(message, History):
    History.append({"role": "user", "content": message})

    context = get_docs(message)
    History.append({"role": "system", "content": plantilla_sys(context)})

    try:
        respuesta = get_completion_from_messages(History)
        respuesta_texto = respuesta[0]

    except HttpResponseError as e:
        respuesta_texto = "Error en el llamado a openAI: " + str(e)

    History.pop()  # delete the context prompt
    History.append({"role": "assistant", "content": respuesta_texto})
    
    new_messages =History[-2:]

    return respuesta_texto, new_messages
