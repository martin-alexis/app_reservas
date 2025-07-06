from api.app.swagger.apispec_config import spec

def document_pago_endpoints():
    """Documenta todos los endpoints del módulo de pagos v2 (exhaustivo, fiel al código real)"""

    # POST /api/v2.0/servicios/{id_servicio}/reservas/{id_reserva}/pagos
    spec.path(
        path="/api/v2.0/servicios/{id_servicio}/reservas/{id_reserva}/pagos",
        operations={
            "post": {
                "tags": ["Pagos"],
                "summary": "Efectuar un pago",
                "description": (
                    "Crea un pago para una reserva de un servicio.\n\n"
                    "**Requiere autenticación JWT y rol CLIENTE o ADMIN.**\n"
                    "**Validaciones:**\n"
                    "- El campo 'monto' es obligatorio y debe ser igual al precio del servicio.\n"
                    "- La reserva debe pertenecer al servicio.\n"
                    "- La reserva no debe estar ya reservada.\n"
                    "- El usuario no puede ser el proveedor del servicio.\n"
                ),
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {"name": "id_servicio", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del servicio"},
                    {"name": "id_reserva", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID de la reserva"}
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["monto"],
                                "properties": {
                                    "monto": {"type": "number", "format": "float", "description": "Monto a pagar (debe ser igual al precio del servicio)"}
                                }
                            },
                            "example": {"monto": 1500.00}
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Pago creado exitosamente",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 201,
                                    "message": "Pago creado exitosamente",
                                    "data": None,
                                    "error": None
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Error de validación de campos o negocio",
                        "content": {
                            "application/json": {
                                "examples": {
                                    "Monto incorrecto": {
                                        "value": {
                                            "status": "error",
                                            "code": 422,
                                            "message": "Validation error",
                                            "error": {"monto": ["El pago del servicio tiene que ser exacto."]},
                                            "data": None
                                        }
                                    },
                                    "Campo requerido": {
                                        "value": {
                                            "status": "error",
                                            "code": 422,
                                            "message": "Validation error",
                                            "error": {"monto": ["Missing data for required field."]},
                                            "data": None
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "No autenticado o token inválido",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 401,
                                    "message": "No autorizado",
                                    "error": "Token de autenticación faltante o inválido.",
                                    "data": None
                                }
                            }
                        }
                    },
                    "403": {
                        "description": "Prohibido (sin permisos o lógica de negocio)",
                        "content": {
                            "application/json": {
                                "examples": {
                                    "Usuario es proveedor": {
                                        "value": {
                                            "status": "error",
                                            "code": 403,
                                            "message": "Acceso prohibido",
                                            "error": "El proveedor del servicio no puede efectuar el pago de su propio servicio.",
                                            "data": None
                                        }
                                    },
                                    "Reserva ya reservada": {
                                        "value": {
                                            "status": "error",
                                            "code": 403,
                                            "message": "Acceso prohibido",
                                            "error": "Esta reserva ya está reservada.",
                                            "data": None
                                        }
                                    },
                                    "Sin roles requeridos": {
                                        "value": {
                                            "status": "error",
                                            "code": 403,
                                            "message": "Acceso prohibido",
                                            "error": "No tienes los roles requeridos para acceder a este recurso.",
                                            "data": None
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Servicio, reserva o usuario no encontrado, o la reserva no pertenece al servicio",
                        "content": {
                            "application/json": {
                                "examples": {
                                    "Servicio no encontrado": {
                                        "value": {
                                            "status": "error",
                                            "code": 404,
                                            "message": "Servicio no encontrado",
                                            "error": None,
                                            "data": None
                                        }
                                    },
                                    "Reserva no encontrada": {
                                        "value": {
                                            "status": "error",
                                            "code": 404,
                                            "message": "Reserva no encontrada",
                                            "error": None,
                                            "data": None
                                        }
                                    },
                                    "Usuario no encontrado": {
                                        "value": {
                                            "status": "error",
                                            "code": 404,
                                            "message": "Usuario no encontrado",
                                            "error": None,
                                            "data": None
                                        }
                                    },
                                    "La reserva no pertenece al servicio": {
                                        "value": {
                                            "status": "error",
                                            "code": 404,
                                            "message": "La reserva no pertenece a este servicio",
                                            "error": None,
                                            "data": None
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Error interno del servidor",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 500,
                                    "message": "Ha ocurrido un error",
                                    "error": "Descripción del error interno",
                                    "data": None
                                }
                            }
                        }
                    }
                }
            }
        }
    )

    # GET /api/v2.0/usuarios/{id_usuario}/pagos
    spec.path(
        path="/api/v2.0/usuarios/{id_usuario}/pagos",
        operations={
            "get": {
                "tags": ["Pagos"],
                "summary": "Obtener pagos de un usuario",
                "description": (
                    "Devuelve todos los pagos realizados por el usuario.\n\n"
                    "**Requiere autenticación JWT y rol CLIENTE, PROVEEDOR o ADMIN.**\n"
                    "**Permisos:** Solo el usuario, un proveedor o un admin pueden consultar.\n"
                ),
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {"name": "id_usuario", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del usuario"}
                ],
                "responses": {
                    "200": {
                        "description": "Lista de pagos del usuario",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 200,
                                    "message": None,
                                    "data": [
                                        {
                                            "id_pagos": 1,
                                            "fecha_pago": "2024-06-01T12:00:00Z",
                                            "monto": 1500.0,
                                            "reservas_id": 2,
                                            "estados_pago_id": 1,
                                            "usuarios_id": 5
                                        }
                                    ],
                                    "error": None
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "No autenticado o token inválido",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 401,
                                    "message": "No autorizado",
                                    "error": "Token de autenticación faltante o inválido.",
                                    "data": None
                                }
                            }
                        }
                    },
                    "403": {
                        "description": "Prohibido (sin permisos)",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 403,
                                    "message": "Acceso prohibido",
                                    "error": "No tienes permisos para realizar esta acción",
                                    "data": None
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Usuario no encontrado",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 404,
                                    "message": "Usuario no encontrado",
                                    "error": None,
                                    "data": None
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Error interno del servidor",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 500,
                                    "message": "Ha ocurrido un error",
                                    "error": "Descripción del error interno",
                                    "data": None
                                }
                            }
                        }
                    }
                }
            }
        }
    )

    # DELETE /api/v2.0/servicios/{id_servicio}/reservas/{id_reserva}/pagos/{id_pago}
    spec.path(
        path="/api/v2.0/servicios/{id_servicio}/reservas/{id_reserva}/pagos/{id_pago}",
        operations={
            "delete": {
                "tags": ["Pagos"],
                "summary": "Eliminar un pago",
                "description": (
                    "Elimina un pago de una reserva de un servicio.\n\n"
                    "**Requiere autenticación JWT y rol CLIENTE, PROVEEDOR o ADMIN.**\n"
                    "**Permisos:** Solo el usuario dueño del pago o un admin pueden eliminarlo. Al eliminar el pago, la reserva vuelve a estado DISPONIBLE.\n"
                ),
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {"name": "id_servicio", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del servicio"},
                    {"name": "id_reserva", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID de la reserva"},
                    {"name": "id_pago", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del pago"}
                ],
                "responses": {
                    "200": {
                        "description": "Pago eliminado exitosamente",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 200,
                                    "message": "Pago eliminado exitosamente",
                                    "data": None,
                                    "error": None
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "No autenticado o token inválido",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 401,
                                    "message": "No autorizado",
                                    "error": "Token de autenticación faltante o inválido.",
                                    "data": None
                                }
                            }
                        }
                    },
                    "403": {
                        "description": "Prohibido (sin permisos o lógica de negocio)",
                        "content": {
                            "application/json": {
                                "examples": {
                                    "No dueño ni admin": {
                                        "value": {
                                            "status": "error",
                                            "code": 403,
                                            "message": "Acceso prohibido",
                                            "error": "No tienes permisos para eliminar este pago",
                                            "data": None
                                        }
                                    },
                                    "Sin roles requeridos": {
                                        "value": {
                                            "status": "error",
                                            "code": 403,
                                            "message": "Acceso prohibido",
                                            "error": "No tienes los roles requeridos para acceder a este recurso.",
                                            "data": None
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Servicio, reserva, pago o usuario no encontrado, o la reserva/pago no pertenece al recurso correspondiente",
                        "content": {
                            "application/json": {
                                "examples": {
                                    "Servicio no encontrado": {
                                        "value": {
                                            "status": "error",
                                            "code": 404,
                                            "message": "Servicio no encontrado",
                                            "error": None,
                                            "data": None
                                        }
                                    },
                                    "Reserva no encontrada": {
                                        "value": {
                                            "status": "error",
                                            "code": 404,
                                            "message": "Reserva no encontrada",
                                            "error": None,
                                            "data": None
                                        }
                                    },
                                    "Pago no encontrado": {
                                        "value": {
                                            "status": "error",
                                            "code": 404,
                                            "message": "Pago no encontrado",
                                            "error": None,
                                            "data": None
                                        }
                                    },
                                    "Usuario no encontrado": {
                                        "value": {
                                            "status": "error",
                                            "code": 404,
                                            "message": "Usuario no encontrado",
                                            "error": None,
                                            "data": None
                                        }
                                    },
                                    "La reserva no pertenece al servicio": {
                                        "value": {
                                            "status": "error",
                                            "code": 404,
                                            "message": "La reserva no pertenece a este servicio",
                                            "error": None,
                                            "data": None
                                        }
                                    },
                                    "El pago no pertenece a la reserva": {
                                        "value": {
                                            "status": "error",
                                            "code": 404,
                                            "message": "El pago no pertenece a esta reserva",
                                            "error": None,
                                            "data": None
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Error interno del servidor",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 500,
                                    "message": "Ha ocurrido un error",
                                    "error": "Descripción del error interno",
                                    "data": None
                                }
                            }
                        }
                    }
                }
            }
        }
    )

    # Endpoint: Obtener pago por ID
    spec.path(
        path="/api/v2.0/pagos/{id_pago}",
        operations={
            "get": {
                "tags": ["Pagos"],
                "summary": "Obtener pago por ID",
                "description": "Obtiene la información de un pago específico por su ID.",
                "parameters": [
                    {
                        "name": "id_pago",
                        "in": "path",
                        "required": True,
                        "description": "ID del pago a consultar",
                        "schema": {"type": "integer"},
                        "example": 123
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Pago encontrado",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 200,
                                    "message": "Operación exitosa",
                                    "error": None,
                                    "data": {
                                        "id_pagos": 123,
                                        "monto": 1000.0,
                                        "fecha_pago": "2024-07-01T12:00:00",
                                        "usuarios_id": 1,
                                        "reservas_id": 10,
                                        "estados_pago_id": 2
                                    }
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Pago no encontrado",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 404,
                                    "message": "Pago no encontrado",
                                    "error": None,
                                    "data": None
                                }
                            }
                        }
                    }
                }
            }
        }
    ) 