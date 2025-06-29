from api.app.swagger.apispec_config import spec

def document_pregunta_endpoints():
    """Documenta todos los endpoints del módulo de preguntas"""
    
    # Endpoint GET /servicios/{id_servicio}/preguntas
    spec.path(
        path="/servicios/{id_servicio}/preguntas",
        operations={
            "get": {
                "tags": ["Preguntas"],
                "summary": "Obtener preguntas de un servicio",
                "description": "Obtiene todas las preguntas asociadas a un servicio específico",
                "parameters": [
                    {
                        "name": "id_servicio",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID del servicio"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Lista de preguntas obtenida exitosamente",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Pregunta"}
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Servicio no encontrado",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "error": {"type": "string"},
                                        "message": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Error interno del servidor"
                    }
                }
            },
            "post": {
                "tags": ["Preguntas"],
                "summary": "Crear una nueva pregunta",
                "description": "Crea una nueva pregunta para un servicio específico. Solo usuarios autenticados pueden crear preguntas.",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "id_servicio",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID del servicio"
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["pregunta"],
                                "properties": {
                                    "pregunta": {
                                        "type": "string",
                                        "description": "Texto de la pregunta",
                                        "maxLength": 255
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Pregunta creada exitosamente",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Pregunta"}
                            }
                        }
                    },
                    "400": {
                        "description": "Datos de entrada inválidos",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "error": {"type": "string"},
                                        "message": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "No autorizado - Token requerido"
                    },
                    "403": {
                        "description": "Prohibido - No tienes permisos para crear preguntas en este servicio"
                    },
                    "404": {
                        "description": "Servicio no encontrado"
                    },
                    "500": {
                        "description": "Error interno del servidor"
                    }
                }
            }
        }
    )
    
    # Endpoint POST /servicios/{id_servicio}/preguntas/{id_pregunta}/respuestas
    spec.path(
        path="/servicios/{id_servicio}/preguntas/{id_pregunta}/respuestas",
        operations={
            "post": {
                "tags": ["Preguntas"],
                "summary": "Crear respuesta a una pregunta",
                "description": "Crea una respuesta para una pregunta específica. Solo proveedores del servicio pueden responder.",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "id_servicio",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID del servicio"
                    },
                    {
                        "name": "id_pregunta",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID de la pregunta"
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["respuesta"],
                                "properties": {
                                    "respuesta": {
                                        "type": "string",
                                        "description": "Texto de la respuesta",
                                        "maxLength": 255
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Respuesta creada exitosamente",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Pregunta"}
                            }
                        }
                    },
                    "400": {
                        "description": "Datos de entrada inválidos",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "error": {"type": "string"},
                                        "message": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "No autorizado - Token requerido"
                    },
                    "403": {
                        "description": "Prohibido - Solo el proveedor del servicio puede responder"
                    },
                    "404": {
                        "description": "Servicio o pregunta no encontrada"
                    },
                    "500": {
                        "description": "Error interno del servidor"
                    }
                }
            }
        }
    )
    
    # Endpoint DELETE /servicios/{id_servicio}/preguntas/{id_pregunta}
    spec.path(
        path="/servicios/{id_servicio}/preguntas/{id_pregunta}",
        operations={
            "delete": {
                "tags": ["Preguntas"],
                "summary": "Eliminar una pregunta",
                "description": "Elimina una pregunta específica. Solo el proveedor del servicio o el autor de la pregunta pueden eliminarla.",
                "security": [{"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "id_servicio",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID del servicio"
                    },
                    {
                        "name": "id_pregunta",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID de la pregunta"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Pregunta eliminada exitosamente",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {"type": "string"},
                                        "data": {"type": "object"}
                                    }
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "No autorizado - Token requerido"
                    },
                    "403": {
                        "description": "Prohibido - No tienes permisos para eliminar esta pregunta"
                    },
                    "404": {
                        "description": "Servicio o pregunta no encontrada"
                    },
                    "500": {
                        "description": "Error interno del servidor"
                    }
                }
            }
        }
    ) 