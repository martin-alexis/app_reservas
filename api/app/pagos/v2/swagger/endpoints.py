from api.app.swagger.apispec_config import spec

def document_pago_endpoints():
    """Documenta todos los endpoints del módulo de pagos v2"""

    # POST /servicios/{id_servicio}/reservas/{id_reserva}/pagos
    spec.path(
        path="/servicios/{id_servicio}/reservas/{id_reserva}/pagos",
        operations={
            "post": {
                "tags": ["Pagos"],
                "summary": "Efectuar un pago",
                "description": "Crea un pago para una reserva de un servicio. Solo puede hacerlo el cliente (no el proveedor del servicio).",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {"name": "id_servicio", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del servicio"},
                    {"name": "id_reserva", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID de la reserva"},
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["monto"],
                                "properties": {
                                    "monto": {"type": "number", "format": "float", "description": "Monto a pagar"}
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "201": {"description": "Pago creado exitosamente"},
                    "400": {"description": "Error de validación o de negocio"},
                    "403": {"description": "Permiso denegado"},
                    "500": {"description": "Error interno del servidor"},
                }
            }
        }
    )

    # DELETE /servicios/{id_servicio}/reservas/{id_reserva}/pagos/{id_pago}
    spec.path(
        path="/servicios/{id_servicio}/reservas/{id_reserva}/pagos/{id_pago}",
        operations={
            "delete": {
                "tags": ["Pagos"],
                "summary": "Eliminar un pago",
                "description": "Elimina un pago de una reserva de un servicio. Solo el usuario dueño del pago o un admin pueden eliminarlo. Al eliminar el pago, la reserva vuelve a estado DISPONIBLE.",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {"name": "id_servicio", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del servicio"},
                    {"name": "id_reserva", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID de la reserva"},
                    {"name": "id_pago", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del pago"},
                ],
                "responses": {
                    "200": {"description": "Pago eliminado exitosamente"},
                    "403": {"description": "Permiso denegado"},
                    "404": {"description": "No encontrado"},
                    "500": {"description": "Error interno del servidor"},
                }
            }
        }
    )

    # GET /usuarios/{id_usuario}/pagos
    spec.path(
        path="/usuarios/{id_usuario}/pagos",
        operations={
            "get": {
                "tags": ["Pagos"],
                "summary": "Obtener pagos de un usuario",
                "description": "Devuelve todos los pagos realizados por el usuario. Solo el usuario, un proveedor o un admin pueden consultar.",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {"name": "id_usuario", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del usuario"},
                ],
                "responses": {
                    "200": {
                        "description": "Lista de pagos del usuario",
                        "content": {
                            "application/json": {
                                "schema": {"type": "array", "items": {"$ref": "#/components/schemas/Pago"}}
                            }
                        }
                    },
                    "403": {"description": "Permiso denegado"},
                    "404": {"description": "No encontrado"},
                    "500": {"description": "Error interno del servidor"},
                }
            }
        }
    ) 