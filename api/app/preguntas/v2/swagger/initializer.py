from api.app.preguntas.v2.swagger.schemas import register_pregunta_schemas
from api.app.preguntas.v2.swagger.endpoints import document_pregunta_endpoints

def initialize_pregunta_documentation():
    """Inicializa toda la documentación del módulo de preguntas v2"""
    register_pregunta_schemas()
    document_pregunta_endpoints()
    print("✅ Documentación del módulo preguntas v2 inicializada correctamente") 