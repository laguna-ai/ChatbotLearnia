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
    "Como descargo los resultados del test?",
    "para que sirven las rutas ?",
    "cómo hago para inscribirme en la plataforma?",
    "Cuales son las habilidades?",
    "Cuales son los perfiles?",
    "como se presenta el test",
    "donde veo los resultados",
    "Qué son los perfiles?",
    "quiero saber cómo realizar una ruta ?",
    "donde puedo ver las rutas asignadas",
    "que es boldinn",
    "como reseteo mi contraseña",
    "cuantos diagnosticos debo presentar",
    "¿Cómo agrego un usuario a un equipo?",
    "que mide el diagnostico individual",
    "que es un desafio",
    "como asigno una ruta",
    "qué es Boldinn?",
    "Cómo funciona Boldinn?",
    "Sabes de que se trata la habilidad de liderar?",
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
