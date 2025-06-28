from api.app.swagger.apispec_config import spec

def register_usuario_schemas():
    """Registra esquemas específicos de usuarios en apispec"""
    
    # Verificar si los esquemas ya están registrados para evitar duplicados
    registered_schemas = set(spec.components.schemas.keys())
    
    # Solo registrar el esquema principal de Usuario
    # Los esquemas relacionados (UsuarioRol, TipoUsuario, Rol) se registran automáticamente
    # por apispec cuando se importan los archivos de esquemas
    if "Usuario" not in registered_schemas:
        from api.app.usuarios.schemas.schema_usuarios import UsuariosSchema
        spec.components.schema("Usuario", schema=UsuariosSchema)
    
    # Los siguientes esquemas se registran automáticamente por apispec cuando se importan
    # No los registramos manualmente para evitar duplicados
    # - UsuarioRol (UsuariosTieneRolesSchema)
    # - TipoUsuario (TiposUsuarioSchema) 
    # - Rol (RolesSchema) 