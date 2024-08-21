from .excel import get_excel_docs
from vectorstores.postgres import create_vectorstore

def update_postgres_knowledge():
    docs = get_excel_docs()
    create_vectorstore(docs)

update_postgres_knowledge()
