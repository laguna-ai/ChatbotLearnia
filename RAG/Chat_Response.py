import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

# ChatGPT completion
llm_name = "gpt-4o"


def get_completion_from_messages(messages, model=llm_name, temperature=0):
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message.content, response.usage


def plantilla_sys(contexto_conversacion):
    preguntas = """
    -¿Cuál es tu nombre?
    -¿De qué país/ciudad nos escribes?
    -¿A qué universidad/empresa representas?
    -correo electrónico (para enviar información adicional).
    -cantidad de cursos que se quieren hacer o actualizar.
    -presupuesto estimado para el proyecto o precio objetivo.
    -si hay un curso en especial que se esté buscando.
    """
    text = f"""Responde brevemente a la entrada previa del usuario usando el siguiente\
    contexto delimitado con ###, si este contexto es útil para responder\
    al usuario, si no, entonces omítelo:
    ###{contexto_conversacion}###
    Si hay información solicitada por el usuario que no está en el contexto, \
    dices que no la conoces, pero no inventas.
    Si el usuario está dando sus datos, omite el contexto. 
    Es muy importante que priorices la fluidez en la conversación y que \
    no repitas las mismas respuestas para evitar la frustración del usuario.
    No hablas de cosas diferentes a Learnia, como \
    matemáticas, deportes, música, etc..
    
    *Preguntas que puedes hacer sin forzar y conservando el orden y el flujo de la conversación*:
    {preguntas}
    
    *A continuación responde en máximo un párrafo de 45 palabras*
    """
    return text
