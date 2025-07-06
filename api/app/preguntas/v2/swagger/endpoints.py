from api.app.swagger.apispec_config import spec

def document_pregunta_endpoints():
    """Documenta todos los endpoints del módulo de preguntas v2"""

    # GET /api/v2.0/servicios/{id_servicio}/preguntas
    spec.path(
        path="/api/v2.0/servicios/{id_servicio}/preguntas",
        operations={
            "get": {
                "tags": ["Preguntas"],
                "summary": "Obtener preguntas de un servicio",
                "description": (
                    "Obtiene todas las preguntas asociadas a un servicio específico.\n\n"
                    "No requiere autenticación.\n"
                ),
                "parameters": [
                    {"name": "id_servicio", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del servicio"}
                ],
                "responses": {
                    "200": {
                        "description": "Lista de preguntas obtenida exitosamente",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 200,
                                    "message": "Operación exitosa",
                                    "data": [
                                        {"id_preguntas": 1, "pregunta": "¿El hotel tiene wifi?", "fecha_pregunta": "2024-01-10T09:00:00Z", "servicios_id": 5, "usuarios_pregunta_id": 2}
                                    ],
                                    "error": None
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

    # POST /api/v2.0/servicios/{id_servicio}/preguntas
    spec.path(
        path="/api/v2.0/servicios/{id_servicio}/preguntas",
        operations={
            "post": {
                "tags": ["Preguntas"],
                "summary": "Crear una nueva pregunta",
                "description": (
                    "Crea una nueva pregunta para un servicio específico.\n\n"
                    "**Requiere autenticación JWT y uno de los siguientes roles:** PROVEEDOR, ADMIN o CLIENTE.\n"
                    "**Validaciones:**\n"
                    "- El campo 'pregunta' es obligatorio y debe ser texto.\n"
                    "- Solo usuarios autenticados pueden crear preguntas.\n"
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
                                "required": ["pregunta"],
                                "properties": {
                                    "pregunta": {"type": "string", "description": "Texto de la pregunta", "maxLength": 255}
                                }
                            },
                            "example": {"pregunta": "¿El hotel tiene wifi gratuito?"}
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Pregunta creada exitosamente",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 201,
                                    "message": "Recurso creado con éxito",
                                    "data": {"id_preguntas": 2, "pregunta": "¿El hotel tiene wifi gratuito?", "fecha_pregunta": "2024-01-11T10:00:00Z", "servicios_id": 5, "usuarios_pregunta_id": 3},
                                    "error": None
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Error de validación de campos",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 422,
                                    "message": "Validation error",
                                    "error": {"pregunta": ["El campo es obligatorio."]},
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

    # POST /api/v2.0/servicios/{id_servicio}/preguntas/{id_pregunta}/respuestas
    spec.path(
        path="/api/v2.0/servicios/{id_servicio}/preguntas/{id_pregunta}/respuestas",
        operations={
            "post": {
                "tags": ["Preguntas"],
                "summary": "Crear respuesta a una pregunta",
                "description": (
                    "Crea una respuesta para una pregunta específica.\n\n"
                    "**Requiere autenticación JWT y uno de los siguientes roles:** PROVEEDOR o ADMIN.\n"
                    "**Validaciones:**\n"
                    "- El campo 'respuesta' es obligatorio y debe ser texto.\n"
                    "- Solo el proveedor dueño o un ADMIN pueden responder preguntas.\n"
                    "- La pregunta debe pertenecer al servicio.\n"
                ),
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {"name": "id_servicio", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del servicio"},
                    {"name": "id_pregunta", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID de la pregunta"}
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["respuesta"],
                                "properties": {
                                    "respuesta": {"type": "string", "description": "Texto de la respuesta", "maxLength": 255}
                                }
                            },
                            "example": {"respuesta": "Sí, el hotel tiene wifi gratuito en todas las habitaciones."}
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Respuesta creada exitosamente",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 200,
                                    "message": "Respuesta creada exitosamente",
                                    "data": {"id_preguntas": 1, "pregunta": "¿El hotel tiene wifi?", "respuesta": "Sí, el hotel tiene wifi gratuito en todas las habitaciones.", "fecha_respuesta": "2024-01-11T12:00:00Z", "usuarios_respuesta_id": 5},
                                    "error": None
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Error de validación de campos",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 422,
                                    "message": "Validation error",
                                    "error": {"respuesta": ["El campo es obligatorio."]},
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
                        "description": "Servicio, pregunta o usuario no encontrado, o la pregunta no pertenece al servicio",
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
                                    "Pregunta no encontrada": {
                                        "value": {
                                            "status": "error",
                                            "code": 404,
                                            "message": "Pregunta no encontrada",
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
                                    "La pregunta no pertenece al servicio": {
                                        "value": {
                                            "status": "error",
                                            "code": 404,
                                            "message": "La pregunta no pertenece a este servicio",
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

    # DELETE /api/v2.0/servicios/{id_servicio}/preguntas/{id_pregunta}
    spec.path(
        path="/api/v2.0/servicios/{id_servicio}/preguntas/{id_pregunta}",
        operations={
            "delete": {
                "tags": ["Preguntas"],
                "summary": "Eliminar pregunta",
                "description": (
                    "Elimina una pregunta específica.\n\n"
                    "**Requiere autenticación JWT y uno de los siguientes roles:** PROVEEDOR, ADMIN o CLIENTE.\n"
                    "**Permisos:** Solo el proveedor dueño, el autor de la pregunta o un ADMIN pueden eliminar la pregunta.\n"
                ),
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {"name": "id_servicio", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del servicio"},
                    {"name": "id_pregunta", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID de la pregunta a eliminar"}
                ],
                "responses": {
                    "200": {
                        "description": "Pregunta eliminada exitosamente",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 200,
                                    "message": "Pregunta eliminada exitosamente",
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
                        "description": "Servicio, pregunta o usuario no encontrado, o la pregunta no pertenece al servicio",
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
                                    "Pregunta no encontrada": {
                                        "value": {
                                            "status": "error",
                                            "code": 404,
                                            "message": "Pregunta no encontrada",
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
                                    "La pregunta no pertenece al servicio": {
                                        "value": {
                                            "status": "error",
                                            "code": 404,
                                            "message": "La pregunta no pertenece a este servicio",
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

    # Endpoint: Obtener pregunta por ID
    spec.path(
        path="/api/v2.0/preguntas/{id_pregunta}",
        operations={
            "get": {
                "tags": ["Preguntas"],
                "summary": "Obtener pregunta por ID",
                "description": "Obtiene la información de una pregunta específica por su ID.",
                "parameters": [
                    {
                        "name": "id_pregunta",
                        "in": "path",
                        "required": True,
                        "description": "ID de la pregunta a consultar",
                        "schema": {"type": "integer"},
                        "example": 456
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Pregunta encontrada",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 200,
                                    "message": "Operación exitosa",
                                    "error": None,
                                    "data": {
                                        "id_preguntas": 456,
                                        "texto": "¿El servicio incluye materiales?",
                                        "servicios_id": 22,
                                        "usuarios_pregunta_id": 3,
                                        "usuarios_respuesta_id": 5,
                                        "fecha_respuesta": "2024-07-01T15:00:00"
                                    }
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Pregunta no encontrada",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 404,
                                    "message": "Pregunta no encontrada",
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