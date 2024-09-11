from langchain_openai import OpenAIEmbeddings, AzureOpenAIEmbeddings
import numpy as np
from pgvector.psycopg import register_vector
import os
from configuration import OAI_provider, config_OAI, config_AOAI

key = os.environ["OPENAI_API_KEY"]


def search(query, k, score_threshold):
    return query + str(k) + score_threshold

def choose_embeddings():
    if OAI_provider=="openai":
        return OpenAIEmbeddings(openai_api_key=config_OAI["key"],
                                model=config_OAI["embeddings"],)
    elif OAI_provider=="azure":
        return AzureOpenAIEmbeddings(
            azure_endpoint=config_AOAI["endpoint"],
            deployment=config_AOAI["embeddings_deployment"],
            openai_api_key=config_AOAI["key"],
            chunk_size=config_AOAI["chunk_size"],
            )


def get_docs(conn, query):
    Embeddings = choose_embeddings()
    query_embedding = np.array(Embeddings.embed_query(text=query))
    # print("query embedding:", type(query_embedding))
    register_vector(conn)
    with conn.cursor() as cur:
        results = cur.execute(
            "SELECT content FROM documents ORDER BY embedding <=> %s LIMIT 4;",
            (query_embedding,),
        ).fetchall()

    doc_string = "\n\n".join([r[0] for r in results])
    return doc_string
