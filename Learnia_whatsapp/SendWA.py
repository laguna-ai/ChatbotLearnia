from heyoo import WhatsApp
import os

# WA credentials
token = os.environ["WHATSAPP_TOKEN"]
# WA Business id
phoneNumberId = os.environ["PHONE_ID"]
# Initialize WA messages
WAMessage = WhatsApp(token, phoneNumberId)

# Welcome message
bienvenida = """
Prodesa, 30 años construyendo sueños en el territorio nacional.\n
Colibrí: Balcones de Soacha 🤝\n
Soy ChatBot Colibrí. Una inteligencia artificial que te ayudará a resolver todas tus dudas. Estoy aquí para ti.
"""


def sendWA(rta, tel, welcome):
    if welcome:
        WAMessage.send_message(bienvenida + rta, tel)
    else:
        WAMessage.send_message(rta, tel)
