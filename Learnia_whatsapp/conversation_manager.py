from azure.core.exceptions import HttpResponseError
from openai.types.completion_usage import CompletionUsage
from RAG.index_query import get_docs
from RAG.Chat_Response import get_completion_from_messages, plantilla_sys


def respuesta_sin_costo(texto):
    uso = CompletionUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0)
    return texto, uso


def respond_message(message, History):
    History.append({"role": "user", "content": message})

    context = get_docs(message)
    History.append({"role": "system", "content": plantilla_sys(context)})

    try:
        respuesta = get_completion_from_messages(History)
        respuesta_texto = respuesta[0]
        respuesta_uso = respuesta[1]

    except HttpResponseError as e:
        respuesta_texto, respuesta_uso = respuesta_sin_costo(
            "Error en el llamado a openAI: " + str(e)
        )
    History.pop()  # delete the context prompt
    return respuesta_texto, respuesta_uso, History
