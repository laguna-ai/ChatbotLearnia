import openai
from configuration import OAI_provider,config_OAI, config_AOAI

if OAI_provider=="openai":
    client=openai
    llm=config_OAI["llm"]
elif OAI_provider=="azure":
    client = openai.AzureOpenAI(
    azure_endpoint=config_AOAI["endpoint"],
    api_key=config_AOAI["key"],
    api_version=config_AOAI["api_version"],
    )
    llm=config_OAI["llm_deployment"]


def get_completion_from_messages(messages, 
                                 model=config_AOAI["llm_deployment"], 
                                temperature=0):
    response = client.chat.completions.create(
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
