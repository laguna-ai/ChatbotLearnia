import uuid
import requests
import random
import time
import json
import os

# Crear la clase Usuario

basic_number = "57300554000"

PHONE_ID = os.environ["PHONE_ID"]
PHONE_NUMBER = "573202190464"
identifier = "259154270612296"


class Usuario:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def create_message(self, mensaje):
        ID = "wamid." + str(uuid.uuid4())
        timestamp = str(int(time.time()))
        return {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "id": identifier,
                    "changes": [
                        {
                            "value": {
                                "messaging_product": "whatsapp",
                                "metadata": {
                                    "display_phone_number": PHONE_NUMBER,
                                    "phone_number_id": PHONE_ID,
                                },
                                "contacts": [
                                    {
                                        "profile": {"name": self.name},
                                        "wa_id": self.phone,
                                    }
                                ],
                                "messages": [
                                    {
                                        "from": self.phone,
                                        "id": ID,
                                        "timestamp": timestamp,
                                        "text": {"body": mensaje},
                                        "type": "text",
                                    }
                                ],
                            },
                            "field": "messages",
                        }
                    ],
                }
            ],
        }


# Banco de mensajes predefinidos
message_bank = [
    "¿Qué servicios ofrecen para virtualizar programas universitarios?",
    "¿Cuál es el proceso de desarrollo de contenidos a medida para una universidad?",
    "¿Cómo funciona el proceso de adaptación de contenidos existentes para una universidad específica?",
    "¿Qué tipo de contenidos pueden desarrollar para programas universitarios?",
    "¿Tienen experiencia previa en la virtualización de programas específicos o en ciertas áreas de estudio?",
    "¿Cuál es el tiempo estimado de entrega para el desarrollo de contenidos a medida?",
    "¿Cuál es el costo asociado con el desarrollo de contenidos a medida o la adaptación de contenidos existentes?",
    "¿Qué tecnologías o plataformas utilizan para la virtualización de programas universitarios?",
    "¿Cómo se garantiza la calidad y la actualización de los contenidos desarrollados?",
    "¿Ofrecen servicios de consultoría para ayudar a las universidades a diseñar su estrategia de virtualización de programas?",
    "¿Qué recursos o materiales necesitamos proporcionar como universidad para el desarrollo de contenidos?",
    "¿Qué tipo de soporte técnico o de capacitación ofrecen durante y después de la implementación de los contenidos virtualizados?",
    "¿Cómo se gestionan los derechos de autor y la propiedad intelectual de los contenidos desarrollados?",
    "¿Pueden integrar los contenidos desarrollados con sistemas de gestión del aprendizaje (LMS) existentes en nuestra universidad?",
    "¿Qué medidas de accesibilidad y diseño inclusivo aplican a los contenidos desarrollados para garantizar la igualdad de oportunidades?"
    ]

# Función para simular usuarios y mensajes


def simulate_users_messages(num_users, num_iterations):

    # Crear usuarios Dummy
    users = [
        Usuario(f"Usuario_Ficticio_{i}", f"{basic_number}{i}") for i in range(num_users)
    ]

    # Enviar mensajes

    for _ in range(num_iterations):
        for user in users:
            message = random.choice(message_bank)
            json_message = user.create_message(message)
            # Aquí deberías enviar el request HTTP a tu función de Azure, pero lo imprimiré por simplicidad
            print(json.dumps(json_message), type(json_message))
            # Envío
            response = requests.post(
                "http://localhost:7071/api/annie_simple", json=json_message, timeout=10
            )
            print(response.status_code)
