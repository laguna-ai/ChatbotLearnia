from Postgres.postgres import create_postgres_connection
from langchain_openai import OpenAIEmbeddings
import os

key = os.environ["OPENAI_API_KEY"]


def create_vectorstore(splits):

    inputs = [item.page_content for item in splits]
    Embeddings = OpenAIEmbeddings(openai_api_key=key, model="text-embedding-3-small")
    embeddings = Embeddings.embed_documents(texts=inputs)

    with create_postgres_connection() as conn:  # pylint: disable=E1129
        for content, embedding in zip(inputs, embeddings):
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
                    (content, embedding),
                )
    print("Índice creado en postgres!")


