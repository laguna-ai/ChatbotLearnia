import azure.functions as func
from azure.core.exceptions import ResourceNotFoundError
import logging
from azure.storage.blob import BlobServiceClient
from datetime import datetime, timedelta
import pytz

################################################################################################
#########      Crear una conexión con  almacenamiento blob  ####################################
################################################################################################
connect_str = "DefaultEndpointsProtocol=https;AccountName=historialconversaciones;AccountKey=1IyXT4sLXaaDhLf8Ljp6rxUO9juwpB1bBkdOiqC+9vyqeGTdMr7KpVc6PgZcQc+S4GWkMpkeRP+++AStiJs2AQ==;EndpointSuffix=core.windows.net"
my_blob_service_client = BlobServiceClient.from_connection_string(connect_str)
my_container_name = "conversacioneslernia"

def delete_blobs_after_24_hours(
    blob_service_client: BlobServiceClient, container_name: str
):
    container_client = blob_service_client.get_container_client(container_name)
    for blob in container_client.list_blobs():
        blob_client = container_client.get_blob_client(blob.name)
        # Crear una zona horaria UTCZ
        utc = pytz.utc
        # Localizar el objeto datetime que no tiene zona horaria
        now = utc.localize(datetime.now())
        # Comparar con el objeto datetime que tiene zona horaria
        try:
            if blob_client.exists() and blob.creation_time + timedelta(hours=23) < now:
                blob_client.delete_blob()
        except ResourceNotFoundError as e:
            logging.info("El blob || %s || no fue encontrado.", blob.name)

def main(mytimer: func.TimerRequest) -> None:  # pylint: disable=unused-argument
    # Call the function to delete all blobs in the container that are older than 24 hours
    delete_blobs_after_24_hours(my_blob_service_client, my_container_name)





