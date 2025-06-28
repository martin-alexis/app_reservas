from api.app.swagger.apispec_config import spec

def document_servicio_endpoints():
    """Documenta endpoints específicos de servicios v2"""
    
    # GET /api/v2.0/servicios - Obtener todos los servicios
    spec.path(
        path="/api/v2.0/servicios",
        operations={
            "get": {
                "tags": ["Servicios"],
                "summary": "Obtener todos los servicios",
                "description": "Obtiene la lista de todos los servicios disponibles en el sistema",
                "responses": {
                    "200": {
                        "description": "Lista de servicios obtenida exitosamente",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "success"},
                                        "code": {"type": "integer", "example": 200},
                                        "message": {"type": "string", "example": "Operación exitosa"},
                                        "data": {
                                            "type": "array",
                                            "items": {"$ref": "#/components/schemas/Servicio"}
                                        },
                                        "error": {"type": "null"}
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "tags": ["Servicios"],
                "summary": "Crear un nuevo servicio",
                "description": "Crea un nuevo servicio en el sistema (solo para proveedores y administradores)",
                "security": [
                    {
                        "Bearer": []
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "multipart/form-data": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "nombre": {"type": "string", "example": "Servicio de Limpieza"},
                                    "descripcion": {"type": "string", "example": "Servicio profesional de limpieza residencial"},
                                    "precio": {"type": "number", "format": "float", "example": 50.00},
                                    "ubicacion": {"type": "string", "example": "Madrid, España"},
                                    "tipos_servicio": {"type": "string", "example": "LIMPIEZA"},
                                    "disponibilidad_servicio": {"type": "string", "example": "DISPONIBLE"},
                                    "imagen": {
                                        "type": "string",
                                        "format": "binary",
                                        "description": "Imagen del servicio"
                                    }
                                },
                                "required": ["nombre", "descripcion", "precio", "ubicacion", "tipos_servicio", "disponibilidad_servicio"]
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Servicio creado exitosamente",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "success"},
                                        "code": {"type": "integer", "example": 201},
                                        "message": {"type": "string", "example": "Recurso creado con éxito"},
                                        "data": {"$ref": "#/components/schemas/Servicio"},
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
                    }
                }
            }
        }
    )
    
    # GET /api/v2.0/servicios/{id_servicio} - Obtener servicio por ID
    spec.path(
        path="/api/v2.0/servicios/{id_servicio}",
        operations={
            "get": {
                "tags": ["Servicios"],
                "summary": "Obtener servicio por ID",
                "description": "Obtiene la información de un servicio específico por su ID",
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
                        "description": "Servicio encontrado",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "success"},
                                        "code": {"type": "integer", "example": 200},
                                        "message": {"type": "string", "example": "Operación exitosa"},
                                        "data": {"$ref": "#/components/schemas/Servicio"},
                                        "error": {"type": "null"}
                                    }
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
                                        "status": {"type": "string", "example": "error"},
                                        "code": {"type": "integer", "example": 404},
                                        "message": {"type": "string", "example": "Servicio no encontrado"}
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "patch": {
                "tags": ["Servicios"],
                "summary": "Actualizar servicio",
                "description": "Actualiza la información de un servicio existente (solo para proveedores y administradores)",
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
                            "schema": {"$ref": "#/components/schemas/Servicio"},
                            "example": {
                                "nombre": "Servicio de Limpieza Actualizado",
                                "descripcion": "Servicio profesional de limpieza residencial mejorado",
                                "precio": 60.00
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Servicio actualizado exitosamente",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "success"},
                                        "code": {"type": "integer", "example": 200},
                                        "message": {"type": "string", "example": "Operación exitosa"},
                                        "data": {"$ref": "#/components/schemas/Servicio"},
                                        "error": {"type": "null"}
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
            },
            "delete": {
                "tags": ["Servicios"],
                "summary": "Eliminar servicio",
                "description": "Elimina un servicio del sistema (solo para proveedores y administradores)",
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
                "responses": {
                    "200": {
                        "description": "Servicio eliminado exitosamente",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "success"},
                                        "code": {"type": "integer", "example": 200},
                                        "message": {"type": "string", "example": "Servicio eliminado exitosamente"}
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
    
    # PUT /api/v2.0/servicios/{id_servicio}/imagen-servicio - Actualizar imagen del servicio
    spec.path(
        path="/api/v2.0/servicios/{id_servicio}/imagen-servicio",
        operations={
            "put": {
                "tags": ["Servicios"],
                "summary": "Actualizar imagen del servicio",
                "description": "Actualiza la imagen de un servicio (solo para proveedores y administradores)",
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
                        "multipart/form-data": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "imagen": {
                                        "type": "string",
                                        "format": "binary",
                                        "description": "Nueva imagen del servicio"
                                    }
                                },
                                "required": ["imagen"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Imagen del servicio actualizada exitosamente",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "success"},
                                        "code": {"type": "integer", "example": 200},
                                        "message": {"type": "string", "example": "Imagen actualizada exitosamente"}
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