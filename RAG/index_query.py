from langchain_openai import OpenAIEmbeddings
import numpy as np
from pgvector.psycopg import register_vector
import os


key = os.environ["OPENAI_API_KEY"]


def search(query, k, score_threshold):
    return query + str(k) + score_threshold


def get_docs(conn, query):
    Embeddings = OpenAIEmbeddings(openai_api_key=key, model="text-embedding-3-small")
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
