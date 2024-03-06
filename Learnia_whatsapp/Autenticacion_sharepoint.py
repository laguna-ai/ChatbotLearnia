from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.fields.creation_information import FieldCreationInformation
from office365.sharepoint.fields.field import FieldType
import os


def auth_sharepoint():
    ####################################################################################################
    #                       AUTENTICACIÓN
    ############################################################################
    SITE_URL = "https://lagunaai.sharepoint.com/sites/ConversacionesChatbots"
    USERNAME = os.environ["USERNAME_AZ"]
    PASSWORD = os.environ["PASSWORD"]
    user_credentials = UserCredential(USERNAME, PASSWORD)
    sp_context = ClientContext(SITE_URL).with_credentials(user_credentials)
    sp_context.load(sp_context.web)
    sp_context.execute_query()
    return sp_context


context = auth_sharepoint()
# Creación y verificación de campos o columnas de la lista de sharepoint
# evitamos la creacion de muchos columnas con el "mismo nombre"

#################################################
#           LISTA QUE VAMOS A MODIFICAR
#################################################
sp_list = context.web.lists.get_by_title("Development_Colibrí")  # CONECTAMOS A LA LISTA

# Define la información para la creación del campo
content = FieldCreationInformation(
    "Content", FieldType.Note
)  # se define un campo que recibe multiples lineas de texto
number_cel_inf = FieldCreationInformation(
    "User_ID", FieldType.Text
)  # se define un campo que recibe una unica linea de texto
nombre_inf = FieldCreationInformation("User_Name", FieldType.Text)

# Verifica si los campos ya existen
fields = sp_list.fields
context.load(fields)
context.execute_query()

field_names = [field.internal_name for field in fields]
print(field_names)


def contains_any(name_of_field, strings):
    # Retorna True si el nombre del campo contiene alguna de las cadenas en la lista strings
    # False si el nombre del campo no está la cadena en la lista de strings
    for s in strings:
        if s in name_of_field:
            return True
    return False


fields_to_create = ["User_ID", "User_Name", "Content"]
# Recorre los nombres de los campos a crear
for field_name in fields_to_create:
    # si el valor de la función es falso, osea el nombre del campo que queremos no está creado en sharepoint...
    if not contains_any(field_name, field_names):
        # Crea el campo correspondiente según la lista de campos que deseamos crear
        if "User_ID" in fields_to_create:
            number_cel = sp_list.fields.add(number_cel_inf)
        if "User_Name" in fields_to_create:
            nombre_inf = sp_list.fields.add(nombre_inf)
        if "Content" in fields_to_create:
            contenido = sp_list.fields.add(content)
    # print(field_names)
    context.execute_query()
