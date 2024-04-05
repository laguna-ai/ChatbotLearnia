from azure.core.exceptions import HttpResponseError
from openai.types.completion_usage import CompletionUsage
from RAG.index_query import get_docs
from RAG.Chat_Response import get_completion_from_messages, plantilla_sys
from RAG.calculo_costos import openai_api_calculate_cost


def respuesta_sin_costo(texto):
    uso = CompletionUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0)
    return texto, uso

def respond_message(message, History):
    History.append({"role": "user", "content": message})
    
    # número de interacciones previas
    n = len(History)
    # respuestas de texto y uso
    if n == 2:
        respuesta_texto, respuesta_uso = respuesta_sin_costo("¿Cuál es tu nombre?")
    elif n == 4:
        respuesta_texto, respuesta_uso = respuesta_sin_costo(
            "¡Gracias! ¿De qué país/ciudad nos escribes?"
        )
    elif n == 6:
        respuesta_texto, respuesta_uso = respuesta_sin_costo(
            "¿A qué Universidad / Empresa representas?"
        )
    elif n == 8:
        respuesta_texto, respuesta_uso = respuesta_sin_costo(
            "Gracias por compartirnos tus datos. ¿En qué te puedo ayudar?"
        )
    else:
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

def update_history(respuesta_texto, respuesta_uso, History, Usage):
    History.append({"role": "assistant", "content": respuesta_texto})
    Usage["prompt_tokens"] += respuesta_uso.prompt_tokens
    Usage["completion_tokens"] += respuesta_uso.completion_tokens
    Usage["total_cost"] += openai_api_calculate_cost(respuesta_uso)
    return History, Usage

    