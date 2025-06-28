from api.app.swagger.apispec_config import spec

def register_reserva_schemas():
    """Registra esquemas específicos de reservas en apispec"""
    
    # Verificar si los esquemas ya están registrados para evitar duplicados
    registered_schemas = set(spec.components.schemas.keys())
    
    # Solo registrar el esquema principal de Reserva
    # Los esquemas relacionados (EstadoReserva) se registran automáticamente
    # por apispec cuando se importan los archivos de esquemas
    if "Reserva" not in registered_schemas:
        from api.app.reservas.schemas.schema_reservas import ReservasSchema
        spec.components.schema("Reserva", schema=ReservasSchema)
    
    # Los siguientes esquemas se registran automáticamente por apispec cuando se importan
    # No los registramos manualmente para evitar duplicados
    # - EstadoReserva (EstadosReservaSchema) 