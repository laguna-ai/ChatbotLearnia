# get a list of files in onedrive for Redimed folder
from .authentication import get_token
import requests
import pandas as pd
import io
import json

graph_url="https://graph.microsoft.com/v1.0"

def print_fields(response, fields):
    for user in response.json()["value"]:
        print(20*"***")
        for f in fields:
            if f in user.keys():
                print(user[f])
            else:
                print(f"Warning: no field *{f}*")

def get_response(url):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response

def post_request(url, body):
    token = get_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    return response

# Onedrive users

def view_users():
    # Do a request for getting users
    url = f"{graph_url}/users"
    response = get_response(url)
    #print name and mail
    print_fields(response, ["displayName","mail"])

# View my onedrive items

def view_my_items(user_id):
    url = f"{graph_url}/{user_id}/drive/root/children"
    response = get_response(url)
    print_fields(response, ["name","id","webUrl"])

# View items from a folder

def view_folder_items(user_id, folder_id):
    url = f"{graph_url}/users/{user_id}/drive/items/{folder_id}/children"
    response = get_response(url)
    print_fields(response, ["name","id","webUrl"])

# Download a file by id

def download_file(user_id, file_id):
    url = f"{graph_url}/users/{user_id}/drive/items/{file_id}/content"
    response = get_response(url)
    with open("MSAL/file.csv","wb") as file:
        file.write(response.content)

# Get dataframe from file

def get_df(user_id, file_id):
    url = f"{graph_url}/users/{user_id}/drive/items/{file_id}/content"
    response = get_response(url)
    df = pd.read_csv(io.BytesIO(response.content), sep=";")
    return df

# Sharepoint sites

def view_sites():
    # Do a request for getting (Sharepoint) sites
    url = f"{graph_url}/sites"
    response = get_response(url)
    print_fields(response, ["name","id","webUrl"])

# View site items

def view_site_items(site_id):
    url = f"{graph_url}/sites/{site_id}/drive/root/children"
    response = get_response(url)
    print_fields(response, ["name","id","webUrl"])

# View site lists

def view_site_lists(site_id):
    url = f"{graph_url}/sites/{site_id}/lists"
    response = get_response(url)
    print_fields(response, ["name","id","webUrl","description"])

# Get list by id

def get_list(site_id, list_id):
    url = f"{graph_url}/sites/{site_id}/lists/{list_id}/items?expand=fields"
    response = get_response(url)
    for row in response.json()["value"]:
        print(json.dumps(row["fields"], indent=4))
    #print_fields(response, ["name","id","webUrl","description"])

def add_to_list(site_id, list_id, data):
    url = f"{graph_url}/sites/{site_id}/lists/{list_id}/items"
    response = post_request(url, data)
    if response.status_code == 201:
        print("Item agregado exitosamente.")
        #print(json.dumps(response.json(), indent=4))
    else:
        print(f"Error al agregar el item: {response.status_code}")
        #print(response.text)
    

#view_users()

user_ID = "2593866f-1608-46d9-a5b3-99d4efc86dec"
#view_my_items(user_ID)

folder_ID = "01QJFTYXYDRWA2OZIFENCLR53LKU6WVML2" # Learnia folder
#view_folder_items(user_ID, folder_ID)

file_ID = "01QJFTYXYIPGT5S5H6ZBG2UHLHPDUXW4QK"
#download_file(user_ID, file_ID)

#DF = get_df(user_ID, file_ID)
#print(DF)

#view_sites()

site_ID = "lagunaai.sharepoint.com,64bc137b-c45d-4353-8d50-4a8f32bdc66d,2ee35200-a5e9-4425-bcc5-a6d917106e2e"
#view_site_items(site_ID)

#view_site_lists(site_ID)

list_ID = "687a4024-9e38-4380-a3b5-250b4bee2633" # lista de resúmenes de conversaciones de Venus Tattoo
#get_list(site_ID,list_ID)

info = {
    "session_id": "dfMessenger-55793814-98c0-41c7-ba1c-ab8469be3f6c",
    "nombre": "Mickey",
    "procedencia": "Disney",
    "email": "indeterminado",
    "numero_de_cursos": "100",
    "presupuesto": "US 1M",
    "curso_de_interes": "indeterminado",
    "cargo": "indeterminado",
    "necesidad": "Disney courses",
    "fecha": "2024-09-5T12:00:24Z",
    "organizacion": "Disney World",
}

info = {
    "fecha": "2024-09-5T12:00:24Z",
    "session_id": "46546456456",
    "nombre": "Mickey",
    "ubicacion": "Disney",
    "descripcion": "indeterminado",
    "medidas": "5x5",
    "zona_del_cuerpo": "pecho",
}

add_to_list(site_ID, list_ID, {"fields": info})