import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

# ChatGPT completion
llm_name = "gpt-3.5-turbo"


def get_completion_from_messages(messages, model=llm_name, temperature=0):
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message.content, response.usage


def plantilla_sys(contexto_conversacion):
    text = f"""Responde a la entrada previa del usuario usando el siguiente \
    contexto delimitado con ###, si este contexto es útil para responder \
    al usuario, si no, entonces omítelo:
    ###{contexto_conversacion}###
    Si hay información solicitada por el usuario que no está en el contexto, \
    dices que no la conoces, pero no inventas.
    Es muy importante que priorices la fluidez en la conversación y que \
    no repitas las mismas respuestas para evitar la frustración del usuario.
    No hablas de cosas diferentes a Learnia, como \
    matemáticas, deportes, música, etc..
    """
    return text