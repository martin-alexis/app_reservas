from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

# Configuración de apispec para OpenAPI 3
spec = APISpec(
    title="Booking API",
    version="2.0",
    openapi_version="3.0.3",
    plugins=[MarshmallowPlugin()],
    info={
        "description": "API para sistema de reservas y servicios",
        "contact": {
            "name": "Booking API Support"
        }
    }
)


# Definir el esquema de seguridad global para JWT Bearer
spec.components.security_scheme(
    "bearerAuth",
    {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "Autenticación JWT usando el esquema Bearer. Ejemplo: 'Bearer {token}'"
    }
)

def initialize_all_documentation():
    """Inicializa toda la documentación de la API de forma modular"""
    
    # Importar e inicializar documentación de cada módulo
    try:
        from api.app.usuarios.v2.swagger.initializer import initialize_usuario_documentation
        initialize_usuario_documentation()
    except ImportError as e:
        print(f"⚠️  No se pudo cargar documentación de usuarios: {e}")
    
    try:
        from api.app.servicios.v2.swagger.initializer import initialize_servicio_documentation
        initialize_servicio_documentation()
    except ImportError as e:
        print(f"⚠️  No se pudo cargar documentación de servicios: {e}")
    
    try:
        from api.app.reservas.v2.swagger.initializer import initialize_reserva_documentation
        initialize_reserva_documentation()
    except ImportError as e:
        print(f"⚠️  No se pudo cargar documentación de reservas: {e}")
    
    try:
        from api.app.preguntas.v2.swagger.initializer import initialize_pregunta_documentation
        initialize_pregunta_documentation()
    except ImportError as e:
        print(f"⚠️  No se pudo cargar documentación de preguntas: {e}")
    
    try:
        from api.app.pagos.v2.swagger.initializer import initialize_pago_documentation
        initialize_pago_documentation()
    except ImportError as e:
        print(f"⚠️  No se pudo cargar documentación de pagos: {e}")
    
    # Aquí se pueden agregar más módulos en el futuro
    # from api.app.pagos.v2.swagger.initializer import initialize_pago_documentation
    # initialize_pago_documentation()
    
    print("✅ Documentación completa inicializada") 