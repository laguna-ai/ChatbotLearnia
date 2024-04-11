def get_personal_info(messages):
    tel = messages["from"]
    message = messages["text"]["body"]
    return tel, message#, name
