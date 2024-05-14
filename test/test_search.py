import pytest
from RAG.index_query import search


def create_metadata(source_name, row):
    D = {"source": f"{source_name}.csv", "row": row}
    return D


# Estructura con queries y metadatos de documentos esperados para cada una
queries_and_expected_docs = [
    (
        "Hay cursos disponibles?",
        [
            create_metadata("FAQ", 15),
        ],
    ),
    (
        "Qué cursos tienen?",
        [
            create_metadata("FAQ", 15),
        ],
    ),
    (
        "Que es Learnia?",
        [
            create_metadata("general", 0),
        ],
    ),
    (
        "cuéntame qué ofrecen",
        [
            create_metadata("general", 0),
            create_metadata("general", 2)
        ],
    ),
    (
        "Cómo funciona LEarnia Lab? qué tiene de innovador?",
        [
            create_metadata("general", 8),
            create_metadata("general", 9),    
        ],
    ),
    (
        "son cursos sobre cualquier tema o área de conocimiento?",
        [
            create_metadata("general", 8),
        ],
    ),
    (
        "en los videos muestran material para las clases de robótica para niños. Esto hace parte de Learnia lab?",
        [
            create_metadata("general", 9),
        ],
    ),
    (
        "cuánto cuesta le programa?",
        [
            create_metadata("FAQ", 6),
        ],
    ),
]


@pytest.mark.parametrize("query,expected_metadata", queries_and_expected_docs)
def test_search_results_include_expected_documents(query, expected_metadata):
    results = search(query, k=3, score_threshold=0.5)
    result_metadata = [doc.metadata for doc in results]

    for expected in expected_metadata:
        assert (
            expected in result_metadata
        ), f"El documento esperado {expected} no se encontró en los resultados de la búsqueda para la query '{query}'"
