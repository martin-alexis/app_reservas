from api.app.reservas.v2.swagger.schemas import register_reserva_schemas
from api.app.reservas.v2.swagger.endpoints import document_reserva_endpoints

def initialize_reserva_documentation():
    """Inicializa toda la documentación del módulo de reservas v2"""
    
    # Registrar esquemas específicos de reservas
    register_reserva_schemas()
    
    # Documentar endpoints específicos de reservas
    document_reserva_endpoints()
    
    print("✅ Documentación del módulo reservas v2 inicializada correctamente") 