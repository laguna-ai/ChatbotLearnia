import azure.functions as func


def setup_Meta_webhook(req):
    # Webhook setup in Meta via GET
    if req.method == "GET":
        if req.params.get("hub.verify_token") == "Hola":
            return func.HttpResponse(req.params.get("hub.challenge"))
        else:
            return func.HttpResponse("Error de autenticación")


def manage_WA_status(value):
    # Managment of status messages from WA (delivered, sent, received, etc)
    if "statuses" in value:  # si es un mensaje de status lanzamos status 200
        return func.HttpResponse("Success", status_code=200)


def manage_WA_format(messages):
    message_type = messages["type"]
    # si es reacción, documento, audio, o video, lo omitimos y lanzamos status 200 para evitar errores
    if message_type in [
        "reaction",
        "document",
        "image",
        "audio",
        "video",
        "sticker",
    ]:
        return func.HttpResponse("Success", status_code=200)


def get_personal_info(messages, value):
    tel = messages["from"]
    message = messages["text"]["body"]
    name = value["contacts"][0]["profile"]["name"]
    return tel, message, name
