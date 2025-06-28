from api.app.swagger.apispec_config import spec

def register_servicio_schemas():
    """Registra esquemas específicos de servicios en apispec"""
    
    # Verificar si los esquemas ya están registrados para evitar duplicados
    registered_schemas = set(spec.components.schemas.keys())
    
    # Solo registrar el esquema principal de Servicio
    # Los esquemas relacionados (TipoServicio, DisponibilidadServicio) se registran automáticamente
    # por apispec cuando se importan los archivos de esquemas
    if "Servicio" not in registered_schemas:
        from api.app.servicios.schemas.schema_servicios import ServiciosSchema
        spec.components.schema("Servicio", schema=ServiciosSchema)
    
    # Los siguientes esquemas se registran automáticamente por apispec cuando se importan
    # No los registramos manualmente para evitar duplicados
    # - TipoServicio (TiposServicioSchema)
    # - DisponibilidadServicio (DisponibilidadServicioSchema) 