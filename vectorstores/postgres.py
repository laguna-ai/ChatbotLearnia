from Postgres.postgres import create_postgres_connection
from RAG.index_query import choose_embeddings


def create_vectorstore(splits):

    inputs = [item.page_content for item in splits]
    Embeddings = choose_embeddings()
    embeddings = Embeddings.embed_documents(texts=inputs)

    with create_postgres_connection() as conn:  # pylint: disable=E1129
        for content, embedding in zip(inputs, embeddings):
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
                    (content, embedding),
                )
    print("Índice creado en postgres!")
