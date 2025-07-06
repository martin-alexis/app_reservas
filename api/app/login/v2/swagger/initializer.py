from api.app.login.v2.swagger.endpoints import document_login_endpoints

def initialize_login_documentation():
    """Inicializa toda la documentación del módulo de login v2"""
    
    # Documentar endpoints
    document_login_endpoints()
    
    print("✅ Documentación de login v2.0 inicializada") 