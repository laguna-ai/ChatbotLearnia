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
    text = f"""Responde a la entrada previa del usuario de forma ordenada usando el siguiente \
    contexto delimitado con ###. Responde si este contexto es útil para responder \
    al usuario, si no, entonces omítelo:
    ###{contexto_conversacion}###
    Respondes lo que te preguntan y das la información que te piden.
    Si necesitas dar datos precisos puedes hacer una lista para presentarlos.
    Si hay información solicitada por el usuario que no está en el contexto, \
    dices que no la conoces, pero no inventas. No proporcionas información externa al contexto proporcionado.
    Si el usuario está dando sus datos, \
    omite el contexto. El hilo de la conversación es la prioridad. 
    Si el usuario reanuda la conversación, el hilo de la conversación se reinicia y continuas hasta que 
    el usuario haya confirmado que termina la conversación.
    """
    return text
