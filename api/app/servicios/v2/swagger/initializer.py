from api.app.servicios.v2.swagger.schemas import register_servicio_schemas
from api.app.servicios.v2.swagger.endpoints import document_servicio_endpoints

def initialize_servicio_documentation():
    """Inicializa toda la documentación del módulo de servicios v2"""
    
    # Registrar esquemas específicos de servicios
    register_servicio_schemas()
    
    # Documentar endpoints específicos de servicios
    document_servicio_endpoints()
    
    print("✅ Documentación del módulo servicios v2 inicializada correctamente") 