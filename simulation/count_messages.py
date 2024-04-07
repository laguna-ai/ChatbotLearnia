from .async_test import n_users
from Learnia_whatsapp.blob_storage import container_client
import json

# Creamos una lista para almacenar los archivos específicos que queremos buscar
archivos_buscados = [f"57300555000{i}.txt" for i in range(n_users)]

# Consulta y borrado de blobs 

for a in archivos_buscados:
    blob=container_client.get_blob_client(a)
    History=json.loads(blob.download_blob(encoding="utf-8").readall())
    print(a+":",len(History))
    blob.delete_blob()

