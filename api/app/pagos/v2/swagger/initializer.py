from api.app.pagos.v2.swagger.schemas import register_pago_schemas
from api.app.pagos.v2.swagger.endpoints import document_pago_endpoints

def initialize_pago_documentation():
    """Inicializa toda la documentación del módulo de pagos v2"""
    register_pago_schemas()
    document_pago_endpoints()
    print("✅ Documentación del módulo pagos v2 inicializada correctamente") 