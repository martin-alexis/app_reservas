from api.app.swagger.apispec_config import spec

def register_pago_schemas():
    """Registra esquemas específicos de pagos en apispec"""
    registered_schemas = set(spec.components.schemas.keys())
    if "Pago" not in registered_schemas:
        from api.app.pagos.schemas.schema_pagos import PagosSchema
        spec.components.schema("Pago", schema=PagosSchema)
    if "EstadosPago" not in registered_schemas:
        from api.app.pagos.schemas.schema_estados_pago import EstadosPagoSchema
        spec.components.schema("EstadosPago", schema=EstadosPagoSchema) 