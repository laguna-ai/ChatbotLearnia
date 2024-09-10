# get a list of files in onedrive for Redimed folder
from .authentication import get_token
import requests
import json
import io
import pandas as pd

graph_url="https://graph.microsoft.com/v1.0"
site_ID = "lagunaai.sharepoint.com,9a2e4810-7465-473b-831b-62c1032b1015,4e47b86c-7705-4994-a0b3-861e3fcdcaa9"
list_ID = "fc2df33e-880f-41a7-b623-eff93a22c8bd" # lista de resúmenes de conversaciones de Learnia

def post_request(url, body):
    token = get_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    return response

def add_to_list(data, site_id=site_ID, list_id=list_ID):
    url = f"{graph_url}/sites/{site_id}/lists/{list_id}/items"
    response = post_request(url, data)
    if response.status_code == 201:
        print("Item agregado exitosamente.")
        #print(json.dumps(response.json(), indent=4))
    else:
        print(f"Error al agregar el item: {response.status_code}")
        #print(response.text)

def get_response(url):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response

# Get dataframe from excel file with known id

def get_df(file_id, site_id=site_ID):
    url = f"{graph_url}/sites/{site_id}/drive/items/{file_id}/content"
    response = get_response(url)
    df = pd.read_excel(io.BytesIO(response.content))
    return df



