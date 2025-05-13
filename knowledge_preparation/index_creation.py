from langchain_text_splitters import RecursiveCharacterTextSplitter
from io import BytesIO
from docx import Document as DocxDocument
from vectorstores.postgres import create_vectorstore
from MSAL.search import get_all_files_info, get_file_content
from langchain_core.documents import Document
from pypdf import PdfReader


def create_sharepoint_index():
    """Crea una base de conocimientos desde SharePoint con DOCX y PDF en memoria"""
    
    # 1. Obtener y filtrar archivos
    valid_files = [
        item for item in get_all_files_info() 
        if item['type'] == 'file' and 
        item['name'].lower().endswith(('.pdf', '.docx'))
    ]
    
    all_docs = []
    
    # 2. Procesamiento común en función
    for file_info in valid_files:
        try:
            file_bytes = get_file_content(file_info['id'])
            base_metadata = {
                "source": file_info['path'],
                "file_name": file_info['name']
            }
            
            # Procesamiento específico por tipo
            if file_info['name'].lower().endswith('.docx'):
                doc = DocxDocument(BytesIO(file_bytes))
                text_content = "\n".join(p.text for p in doc.paragraphs)
                all_docs.append(Document(
                    page_content=text_content,
                    metadata=base_metadata
                ))
                
            elif file_info['name'].lower().endswith('.pdf'):
                pdf = PdfReader(BytesIO(file_bytes))
                for page_num, page in enumerate(pdf.pages, 1):
                    all_docs.append(Document(
                        page_content=page.extract_text(),
                        metadata={
                            **base_metadata,
                            "page": page_num,
                            "total_pages": len(pdf.pages)
                        }
                    ))
            
        except Exception as e:
            print(f"Error procesando {file_info['name']}: {str(e)}")
            continue

    # 3. Dividir y formatear documentos
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=15
    )
    
    all_splits = text_splitter.split_documents(all_docs)
    
    # Añadir metadatos al contenido
    for split in all_splits:
        metadata = split.metadata
        split.page_content = (
            f"ARCHIVO: {metadata['file_name']}\n"
            f"RUTA: {metadata['source']}\n\n"
            f"{split.page_content}"
        )
    
    print(f"Total de splits generados: {len(all_splits)}")
    
    # 6. Crear vectorstore
    create_vectorstore(all_splits)
create_sharepoint_index()