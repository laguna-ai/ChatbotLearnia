# get a list of files in onedrive for Redimed folder
from .authentication import get_token
import requests
import pandas as pd
import io

def print_fields(response, fields):
    for user in response.json()["value"]:
        print(20*"***")
        for f in fields:
            print(user[f])

def get_response(url):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response

# Onedrive users

def view_users():
    # Do a request for getting users
    url = "https://graph.microsoft.com/v1.0/users"
    response = get_response(url)
    #print name and mail
    print_fields(response, ["displayName","mail"])

# View my onedrive items

def view_my_items(user_id):
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/drive/root/children"
    response = get_response(url)
    print_fields(response, ["name","id","webUrl"])

# View items from a folder

def view_folder_items(user_id, folder_id):
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/drive/items/{folder_id}/children"
    response = get_response(url)
    print_fields(response, ["name","id","webUrl"])

# Download a file by id

def download_file(user_id, file_id):
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/drive/items/{file_id}/content"
    response = get_response(url)
    with open("MSAL/file.csv","wb") as file:
        file.write(response.content)

# Get dataframe from file

def get_df(user_id, file_id):
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/drive/items/{file_id}/content"
    response = get_response(url)
    df = pd.read_csv(io.BytesIO(response.content), sep=";")
    return df
#view_users()

user_ID = "2593866f-1608-46d9-a5b3-99d4efc86dec"
#view_my_items(user_ID)

folder_ID = "01QJFTYXYDRWA2OZIFENCLR53LKU6WVML2" # Learnia folder
#view_folder_items(user_ID, folder_ID)

file_ID = "01QJFTYXYIPGT5S5H6ZBG2UHLHPDUXW4QK"
#download_file(user_ID, file_ID)

DF = get_df(user_ID, file_ID)
print(DF)