from api.app.swagger.apispec_config import spec

def document_reserva_endpoints():
    """Documenta endpoints específicos de reservas v2"""
    
    # GET /api/v2.0/reservas/{id_reserva} - Obtener reserva por ID
    spec.path(
        path="/api/v2.0/reservas/{id_reserva}",
        operations={
            "get": {
                "tags": ["Reservas"],
                "summary": "Obtener reserva por ID",
                "description": (
                    "Obtiene la información de una reserva específica por su ID.\n\n"
                    "No requiere autenticación.\n"
                ),
                "parameters": [
                    {"name": "id_reserva", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID de la reserva"}
                ],
                "responses": {
                    "200": {
                        "description": "Reserva encontrada",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 200,
                                    "message": "Operación exitosa",
                                    "data": {
                                        "id_reservas": 1,
                                        "fecha_creacion_reserva": "2024-01-10T09:00:00Z",
                                        "fecha_inicio_reserva": "2024-01-15T10:00:00Z",
                                        "fecha_fin_reserva": "2024-01-15T12:00:00Z",
                                        "servicios_id": 5,
                                        "estados_reserva": "RESERVADA",
                                        "estado_reserva": {"id_estados_reserva": 2, "estado": "RESERVADA"}
                                    },
                                    "error": None
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Reserva no encontrada",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 404,
                                    "message": "Reserva no encontrada",
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
    
    # POST /api/v2.0/servicios/{id_servicio}/reservas - Crear reserva para un servicio
    spec.path(
        path="/api/v2.0/servicios/{id_servicio}/reservas",
        operations={
            "post": {
                "tags": ["Reservas"],
                "summary": "Crear reserva para un servicio",
                "description": (
                    "Crea una nueva reserva para un servicio específico.\n\n"
                    "**Requiere autenticación JWT y uno de los siguientes roles:** PROVEEDOR o ADMIN.\n"
                    "**Validaciones:**\n"
                    "- Las fechas deben ser válidas y no solaparse con otras reservas.\n"
                    "- El estado debe ser uno de los valores válidos ('DISPONIBLE', 'RESERVADA').\n"
                    "- Solo el proveedor dueño o un ADMIN pueden crear reservas para el servicio.\n"
                ),
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {"name": "id_servicio", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del servicio"}
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "fecha_inicio_reserva": {"type": "string", "format": "date-time", "example": "2024-01-15T10:00:00Z"},
                                    "fecha_fin_reserva": {"type": "string", "format": "date-time", "example": "2024-01-15T12:00:00Z"},
                                    "estados_reserva": {"type": "string", "example": "RESERVADA"}
                                },
                                "required": ["fecha_inicio_reserva", "fecha_fin_reserva", "estados_reserva"]
                            },
                            "example": {
                                "fecha_inicio_reserva": "2024-01-15T10:00:00Z",
                                "fecha_fin_reserva": "2024-01-15T12:00:00Z",
                                "estados_reserva": "RESERVADA"
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Reserva creada exitosamente",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 201,
                                    "message": "Recurso creado con éxito",
                                    "data": {
                                        "id_reservas": 2,
                                        "fecha_creacion_reserva": "2024-01-10T09:00:00Z",
                                        "fecha_inicio_reserva": "2024-01-15T10:00:00Z",
                                        "fecha_fin_reserva": "2024-01-15T12:00:00Z",
                                        "servicios_id": 5,
                                        "estados_reserva": "RESERVADA",
                                        "estado_reserva": {"id_estados_reserva": 2, "estado": "RESERVADA"}
                                    },
                                    "error": None
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Error de validación de campos o solapamiento de fechas",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 422,
                                    "message": "Validation error",
                                    "error": {
                                        "fecha_inicio_reserva": ["La fecha de inicio no puede estar en el pasado."],
                                        "fecha_fin_reserva": ["La fecha de fin debe ser posterior a la de inicio."],
                                        "estados_reserva": ["Estado inválido."],
                                        "non_field_errors": ["Ya existe una reserva en ese horario."]
                                    },
                                    "data": None
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
                        "description": "Prohibido (sin permisos o sin roles suficientes)",
                        "content": {
                            "application/json": {
                                "examples": {
                                    "Sin permisos sobre el recurso": {
                                        "value": {
                                            "status": "error",
                                            "code": 403,
                                            "message": "Acceso prohibido",
                                            "error": "No tienes permisos para realizar esta acción",
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
                        "description": "Servicio no encontrado",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 404,
                                    "message": "Servicio no encontrado",
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
    
    # PATCH /api/v2.0/servicios/{id_servicio}/reservas/{id_reserva} - Actualizar reserva
    spec.path(
        path="/api/v2.0/servicios/{id_servicio}/reservas/{id_reserva}",
        operations={
            "patch": {
                "tags": ["Reservas"],
                "summary": "Actualizar reserva",
                "description": (
                    "Actualiza la información de una reserva existente.\n\n"
                    "**Requiere autenticación JWT y uno de los siguientes roles:** PROVEEDOR o ADMIN.\n"
                    "**Validaciones:**\n"
                    "- Solo los campos enviados serán actualizados.\n"
                    "- Las fechas deben ser válidas y no solaparse con otras reservas.\n"
                    "- Permisos: solo el proveedor dueño o un ADMIN pueden modificar la reserva.\n"
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
                            "schema": {"$ref": "#/components/schemas/Reserva"},
                            "example": {
                                "fecha_inicio_reserva": "2024-01-15T11:00:00Z",
                                "fecha_fin_reserva": "2024-01-15T13:00:00Z",
                                "estados_reserva": "RESERVADA"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Reserva actualizada exitosamente",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 200,
                                    "message": "Operación exitosa",
                                    "data": {
                                        "id_reservas": 1,
                                        "fecha_creacion_reserva": "2024-01-10T09:00:00Z",
                                        "fecha_inicio_reserva": "2024-01-15T11:00:00Z",
                                        "fecha_fin_reserva": "2024-01-15T13:00:00Z",
                                        "servicios_id": 5,
                                        "estados_reserva": "RESERVADA",
                                        "estado_reserva": {"id_estados_reserva": 2, "estado": "RESERVADA"}
                                    },
                                    "error": None
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Error de validación de campos o solapamiento de fechas",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 422,
                                    "message": "Validation error",
                                    "error": {
                                        "fecha_inicio_reserva": ["La fecha de inicio no puede estar en el pasado."],
                                        "fecha_fin_reserva": ["La fecha de fin debe ser posterior a la de inicio."],
                                        "estados_reserva": ["Estado inválido."],
                                        "non_field_errors": ["Ya existe una reserva en ese horario."]
                                    },
                                    "data": None
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
                        "description": "Prohibido (sin permisos o sin roles suficientes)",
                        "content": {
                            "application/json": {
                                "examples": {
                                    "Sin permisos sobre el recurso": {
                                        "value": {
                                            "status": "error",
                                            "code": 403,
                                            "message": "Acceso prohibido",
                                            "error": "No tienes permisos para realizar esta acción",
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
                        "description": "Servicio o reserva no encontrada",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 404,
                                    "message": "Servicio o reserva no encontrada",
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
    
    # DELETE /api/v2.0/servicios/{id_servicio}/reservas/{id_reserva} - Eliminar reserva
    spec.path(
        path="/api/v2.0/servicios/{id_servicio}/reservas/{id_reserva}",
        operations={
            "delete": {
                "tags": ["Reservas"],
                "summary": "Eliminar reserva",
                "description": (
                    "Elimina una reserva existente.\n\n"
                    "**Requiere autenticación JWT y uno de los siguientes roles:** PROVEEDOR o ADMIN.\n"
                    "**Permisos:** Solo el proveedor dueño o un ADMIN pueden eliminar la reserva.\n"
                ),
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {"name": "id_servicio", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del servicio"},
                    {"name": "id_reserva", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID de la reserva a eliminar"}
                ],
                "responses": {
                    "200": {
                        "description": "Reserva eliminada exitosamente",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 200,
                                    "message": "Operación exitosa",
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
                        "description": "Prohibido (sin permisos o sin roles suficientes)",
                        "content": {
                            "application/json": {
                                "examples": {
                                    "Sin permisos sobre el recurso": {
                                        "value": {
                                            "status": "error",
                                            "code": 403,
                                            "message": "Acceso prohibido",
                                            "error": "No tienes permisos para realizar esta acción",
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
                        "description": "Servicio o reserva no encontrada",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 404,
                                    "message": "Servicio o reserva no encontrada",
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