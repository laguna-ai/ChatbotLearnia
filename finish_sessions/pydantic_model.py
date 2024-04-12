from typing import List, Type
from pydantic import BaseModel, create_model

# Modelo base de Pydantic para validar el JSON
class DynamicModel(BaseModel):
    @classmethod
    def create_dynamic_model(cls, fields: List[str]) -> Type['DynamicModel']:
        # Crear un nuevo modelo con campos dinámicos, todos como strings
        return create_model('DynamicModel', **{field: (str, ...) for field in fields})