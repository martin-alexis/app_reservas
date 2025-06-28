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
                "description": "Obtiene la información de una reserva específica por su ID",
                "parameters": [
                    {
                        "name": "id_reserva",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID de la reserva"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Reserva encontrada",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "success"},
                                        "code": {"type": "integer", "example": 200},
                                        "message": {"type": "string", "example": "Operación exitosa"},
                                        "data": {"$ref": "#/components/schemas/Reserva"},
                                        "error": {"type": "null"}
                                    }
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Reserva no encontrada",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "error"},
                                        "code": {"type": "integer", "example": 404},
                                        "message": {"type": "string", "example": "Reserva no encontrada"}
                                    }
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
                "description": "Crea una nueva reserva para un servicio específico (solo para proveedores y administradores)",
                "parameters": [
                    {
                        "name": "id_servicio",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID del servicio"
                    }
                ],
                "security": [
                    {
                        "Bearer": []
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "fecha_inicio_reserva": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2024-01-15T10:00:00Z",
                                        "description": "Fecha y hora de inicio de la reserva"
                                    },
                                    "fecha_fin_reserva": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2024-01-15T12:00:00Z",
                                        "description": "Fecha y hora de fin de la reserva"
                                    },
                                    "estados_reserva": {
                                        "type": "string",
                                        "example": "PENDIENTE",
                                        "description": "Estado inicial de la reserva"
                                    }
                                },
                                "required": ["fecha_inicio_reserva", "fecha_fin_reserva", "estados_reserva"]
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Reserva creada exitosamente",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "success"},
                                        "code": {"type": "integer", "example": 201},
                                        "message": {"type": "string", "example": "Recurso creado con éxito"},
                                        "data": {"$ref": "#/components/schemas/Reserva"},
                                        "error": {"type": "null"}
                                    }
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Error de validación",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "error"},
                                        "code": {"type": "integer", "example": 400},
                                        "message": {"type": "string"},
                                        "error": {"type": "object"}
                                    }
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "No autorizado"
                    },
                    "403": {
                        "description": "Prohibido - Se requieren permisos de proveedor o administrador"
                    },
                    "404": {
                        "description": "Servicio no encontrado"
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
                "description": "Actualiza la información de una reserva existente (solo para proveedores y administradores)",
                "parameters": [
                    {
                        "name": "id_servicio",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID del servicio"
                    },
                    {
                        "name": "id_reserva",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID de la reserva"
                    }
                ],
                "security": [
                    {
                        "Bearer": []
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Reserva"},
                            "example": {
                                "fecha_inicio_reserva": "2024-01-15T11:00:00Z",
                                "fecha_fin_reserva": "2024-01-15T13:00:00Z",
                                "estados_reserva": "CONFIRMADA"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Reserva actualizada exitosamente",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "success"},
                                        "code": {"type": "integer", "example": 200},
                                        "message": {"type": "string", "example": "Operación exitosa"},
                                        "data": {"$ref": "#/components/schemas/Reserva"},
                                        "error": {"type": "null"}
                                    }
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Error de validación",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "error"},
                                        "code": {"type": "integer", "example": 400},
                                        "message": {"type": "string"},
                                        "error": {"type": "object"}
                                    }
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "No autorizado"
                    },
                    "403": {
                        "description": "Prohibido - Se requieren permisos de proveedor o administrador"
                    },
                    "404": {
                        "description": "Servicio o reserva no encontrado"
                    }
                }
            },
            "delete": {
                "tags": ["Reservas"],
                "summary": "Eliminar reserva",
                "description": "Elimina una reserva del sistema (solo para proveedores y administradores)",
                "parameters": [
                    {
                        "name": "id_servicio",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID del servicio"
                    },
                    {
                        "name": "id_reserva",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID de la reserva"
                    }
                ],
                "security": [
                    {
                        "Bearer": []
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Reserva eliminada exitosamente",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "success"},
                                        "code": {"type": "integer", "example": 200},
                                        "message": {"type": "string", "example": "Reserva eliminada exitosamente"}
                                    }
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "No autorizado"
                    },
                    "403": {
                        "description": "Prohibido - Se requieren permisos de proveedor o administrador"
                    },
                    "404": {
                        "description": "Servicio o reserva no encontrado"
                    }
                }
            }
        }
    ) 