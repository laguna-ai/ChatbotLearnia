from heyoo import WhatsApp
import os
from configuration import bienvenida

# WA credentials
token = os.environ["WHATSAPP_TOKEN"]
# WA Business id
phoneNumberId = os.environ["PHONE_ID"]
# Initialize WA messages
WAMessage = WhatsApp(token, phoneNumberId)


def sendWA(rta, tel, welcome):
    if welcome:
        WAMessage.send_message(bienvenida + rta, tel)
    else:
        WAMessage.send_message(rta, tel)
