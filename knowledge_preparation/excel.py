from finish_sessions.Sharepoint import auth_sharepoint
from office365.sharepoint.files.file import File
from io import BytesIO
import pandas as pd
from langchain_core.documents import Document

fields = ["categoria","tema","info"]

def get_excel_docs():
    context=auth_sharepoint()
    relative_url="/sites/Learnia/Documentos compartidos/Contenido Chat Bot.xlsx"
    response = File.open_binary(context, relative_url)
    df = pd.read_excel(BytesIO(response.content))
    
    # Crear una lista para almacenar los pares
    triples = []

    # Iterar sobre cada fila del DataFrame
    for _ , row in df.iterrows():
        # Iterar sobre cada columna excepto la última
        for j in range(len(df.columns) - 1):
            if pd.notna(row.iloc[j]) and pd.notna(row.iloc[j + 1]):
                triples.append((df.columns[j], row.iloc[j], row.iloc[j + 1]))
    # for t in triples:
    #     print("category:",t[0])
    #     print("topic:",t[1])
    #     print("info:",t[2])
    docs = []
    for j,t in enumerate(triples):
        content = "\n ".join([f"{f}: {t[i]}" for i, f in enumerate(fields)])
        meta = {"id": j}
        doc = Document(page_content=content, metadata=meta)
        docs.append(doc)
    return docs

