from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

# Configuración de apispec para OpenAPI 3
spec = APISpec(
    title="Booking API",
    version="2.0",
    openapi_version="3.0.3",
    plugins=[MarshmallowPlugin()],
    info={
        "description": (
            "Booking App es una API de reservas orientada a la gestión integral de servicios de todo tipo. "
            "Permite a usuarios y proveedores publicar, buscar, reservar y gestionar servicios de manera eficiente.\n\n"
            "Módulos principales: usuarios, servicios, reservas, pagos y preguntas.\n"
            "Características: API RESTful versionada, autenticación JWT y Google OAuth, roles y permisos, documentación Swagger/OpenAPI, validaciones robustas, integración con servicios externos (Cloudinary, Google)."
        ),
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
    
    try:
        from api.app.login.v2.swagger.initializer import initialize_login_documentation
        initialize_login_documentation()
    except ImportError as e:
        print(f"⚠️  No se pudo cargar documentación de login: {e}")
    
    # Aquí se pueden agregar más módulos en el futuro
    # from api.app.pagos.v2.swagger.initializer import initialize_pago_documentation
    # initialize_pago_documentation()
    
    print("✅ Documentación completa inicializada") 