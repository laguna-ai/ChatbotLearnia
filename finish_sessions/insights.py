from RAG.Chat_Response import get_completion_from_messages
import datetime
from typing import List, Dict, Any
from pydantic import ValidationError
from .pydantic_model import DynamicModel


def summarize(
    history: List[Dict[str, Any]], prompt: str, fields: List[str]
) -> Dict[str, str]:
    history.append({"role": "system", "content": prompt})
    DynamicFieldsModel = DynamicModel.create_dynamic_model(fields)

    for i in range(3):
        try:
            json_string = get_completion_from_messages(history)[0]
            data = DynamicFieldsModel.model_validate_json(json_string)
            return data.model_dump()  # Devolver el diccionario directamente

        except ValidationError as e:
            if i == 2:
                print("Error en la validación del JSON:", e)
                return {field: "indeterminado" for field in fields}


def create_prompt(fields):
    field_phrase = " ".join(f"{i}) {f}" for i, f in enumerate(fields, start=1))
    prompt = f"""A partir del historial anterior, crea un JSON con campos (sin tilde): 
    {field_phrase}
    Estos campos corresponden a información proporcionada por el usuario."""
    return prompt


def get_insights(session):
    # first we extract, static info.
    static = {
        "fecha": datetime.datetime.utcnow(),
        "session_id": session[0],
    }

    # now the info with AI
    basic_fields = ["nombre", "procedencia", "organizacion", "necesidad"]
    basic_prompt = create_prompt(basic_fields)
    optional_fields = [
        "email",
        "numero_de_cursos",
        "presupuesto",
        "curso_de_interes",
        "cargo",
    ]
    optional_prompt = create_prompt(optional_fields)
    optional_prompt += """Aclaraciones:
    -El numero_de_cursos corresponde a los que le interesaron al usuario.
    -El curso_de_interes es el que más le interesó al usuario.
    -El cargo es la posición del usuario en su organización.
    """
    history = session[1]
    basic = summarize(history, basic_prompt, basic_fields)
    optional = summarize(history, optional_prompt, optional_fields)
    return {**static, **basic, **optional}