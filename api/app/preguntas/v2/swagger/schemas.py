from api.app.swagger.apispec_config import spec

def register_pregunta_schemas():
    """Registra esquemas específicos de preguntas y respuestas en apispec"""
    
    # Verificar si los esquemas ya están registrados para evitar duplicados
    registered_schemas = set(spec.components.schemas.keys())
    
    # Registrar esquemas de preguntas
    if "Pregunta" not in registered_schemas:
        from api.app.preguntas.schemas.schema_preguntas import PreguntaSchema
        spec.components.schema("Pregunta", schema=PreguntaSchema)
    
    # Registrar esquema de respuesta
    if "Respuesta" not in registered_schemas:
        from api.app.preguntas.schemas.schema_respuestas import RespuestaSchema
        spec.components.schema("Respuesta", schema=RespuestaSchema)
    
    # Registrar esquemas relacionados que se usan en preguntas
    if "Servicio" not in registered_schemas:
        from api.app.servicios.schemas.schema_servicios import ServiciosSchema
        spec.components.schema("Servicio", schema=ServiciosSchema)
    
    if "Usuario" not in registered_schemas:
        from api.app.usuarios.schemas.schema_usuarios import UsuariosSchema
        spec.components.schema("Usuario", schema=UsuariosSchema) 