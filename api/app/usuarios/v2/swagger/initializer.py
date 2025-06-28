from api.app.usuarios.v2.swagger.schemas import register_usuario_schemas
from api.app.usuarios.v2.swagger.endpoints import document_usuario_endpoints

def initialize_usuario_documentation():
    """Inicializa toda la documentación del módulo de usuarios v2"""
    
    # Registrar esquemas específicos de usuarios
    register_usuario_schemas()
    
    # Documentar endpoints específicos de usuarios
    document_usuario_endpoints()
    
    print("✅ Documentación del módulo usuarios v2 inicializada correctamente") 