from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
import os


def auth_sharepoint():
    ####################################################################################################
    #                       AUTENTICACIÓN
    ############################################################################
    SITE_URL = "https://lagunaai.sharepoint.com/sites/Learnia"
    USERNAME = os.environ["USERNAME_AZ"]
    PASSWORD = os.environ["PASSWORD"]
    user_credentials = UserCredential(USERNAME, PASSWORD)
    sp_context = ClientContext(SITE_URL).with_credentials(user_credentials)
    sp_context.load(sp_context.web)
    sp_context.execute_query()
    return sp_context


context = auth_sharepoint()


def add_to_Sharepoint_list(analysis):
    List = context.web.lists.get_by_title("chatbot_insights")  # CONECTAMOS A LA LISTA
    List.add_item(analysis)
    List.execute_query()
