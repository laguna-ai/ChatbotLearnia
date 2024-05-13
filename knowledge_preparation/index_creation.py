from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os


openai_api_key = os.environ["OPENAI_API_KEY"]


def create_index(config_archivos_csv, output_dir='.'):
    """
    Crea una base de conocimientos a partir de una lista de archivos CSV con configuraciones específicas.

    :param config_archivos_csv: Lista de diccionarios con configuraciones de archivos CSV. 
                                Cada diccionario debe tener las claves: 'file_path', 'encoding', y 'delimiter'.
    :param output_dir: Directorio donde se guardará la base de datos vectorial. Por defecto es el directorio actual.
    """
    # Cargar y combinar todos los datos de los archivos CSV
    datos_combinados = []
    for config in config_archivos_csv:
        loader = CSVLoader(file_path=config['file_path'], encoding=config['encoding'], csv_args={'delimiter': config['delimiter']})
        datos = loader.load()
        datos_combinados.extend(datos)
    # ver datos    
    print(datos_combinados)

    # Crear embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_documents(datos_combinados, embeddings)

    # Guardar la base de datos vectorial
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    vectorstore.save_local(output_dir)
    print(f"Base de conocimientos creada y guardada en {output_dir}")


# Ejemplo de uso
dir="csv_conocimientos"
config_archivos_csv = [
     {'file_path': f"{dir}/general.csv", 
     'encoding': 'UTF-8', 
     'delimiter': ';'},
    {'file_path': f"{dir}/cursos.csv", 
     'encoding': 'UTF-8', 
     'delimiter': ';'},
    {'file_path': f"{dir}/FAQ.csv", 
     'encoding': 'UTF-8', 
     'delimiter': ','}
]
output_dir = "index"

create_index(config_archivos_csv, output_dir)
