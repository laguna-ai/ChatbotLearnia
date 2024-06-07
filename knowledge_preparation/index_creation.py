from langchain.document_loaders.csv_loader import CSVLoader
import os
from vectorstores.postgres import create_vectorstore

openai_api_key = os.environ["OPENAI_API_KEY"]


def create_index(config_archivos_csv):
    """
    Crea una base de conocimientos en postgres a partir de una lista de archivos CSV con configuraciones específicas.

    :param config_archivos_csv: Lista de diccionarios con configuraciones de archivos CSV.
                                Cada diccionario debe tener las claves: 'file_path', 'encoding', y 'delimiter'.
    """
    # Cargar y combinar todos los datos de los archivos CSV
    datos_combinados = []
    for config in config_archivos_csv:
        loader = CSVLoader(
            file_path=config["file_path"],
            encoding=config["encoding"],
            csv_args={"delimiter": config["delimiter"]},
        )
        datos = loader.load()
        datos_combinados.extend(datos)
    # ver datos
    print("DATOS:", datos_combinados)

    # Crear embeddings
    create_vectorstore(datos_combinados)


# Ejemplo de uso
Dir = "csv_conocimientos"
conf_archivos_csv = [
    {"file_path": f"{Dir}/general.csv", "encoding": "UTF-8", "delimiter": ";"},
    {"file_path": f"{Dir}/cursos.csv", "encoding": "UTF-8", "delimiter": ","},
    {"file_path": f"{Dir}/FAQ.csv", "encoding": "latin-1", "delimiter": ";"},
]

create_index(conf_archivos_csv)
