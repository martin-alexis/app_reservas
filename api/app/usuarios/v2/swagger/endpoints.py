from api.app.swagger.apispec_config import spec

def document_usuario_endpoints():
    """Documenta endpoints específicos de usuarios v2"""
    
    # POST /api/v2.0/usuarios - Crear usuario
    spec.path(
        path="/api/v2.0/usuarios",
        operations={
            "post": {
                "tags": ["Usuarios"],
                "summary": "Crear un nuevo usuario",
                "description": "Crea un nuevo usuario en el sistema con los datos proporcionados",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Usuario"},
                            "example": {
                                "nombre": "Juan Pérez",
                                "correo": "juan@ejemplo.com",
                                "telefono": "1234567890",
                                "contrasena": "Password123",
                                "tipos_usuario": "PARTICULAR",
                                "tipo_roles": ["CLIENTE"]
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Usuario creado exitosamente",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "success"},
                                        "code": {"type": "integer", "example": 201},
                                        "message": {"type": "string", "example": "Recurso creado con éxito"},
                                        "data": {"type": "object"},
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
                    }
                }
            }
        }
    )
    
    # GET /api/v2.0/usuarios/{id_usuario} - Obtener usuario
    spec.path(
        path="/api/v2.0/usuarios/{id_usuario}",
        operations={
            "get": {
                "tags": ["Usuarios"],
                "summary": "Obtener usuario por ID",
                "description": "Obtiene la información de un usuario específico por su ID",
                "parameters": [
                    {
                        "name": "id_usuario",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID del usuario"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Usuario encontrado",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "success"},
                                        "code": {"type": "integer", "example": 200},
                                        "message": {"type": "string", "example": "Operación exitosa"},
                                        "data": {"$ref": "#/components/schemas/Usuario"},
                                        "error": {"type": "null"}
                                    }
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Usuario no encontrado",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "error"},
                                        "code": {"type": "integer", "example": 404},
                                        "message": {"type": "string", "example": "Usuario no encontrado"}
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "patch": {
                "tags": ["Usuarios"],
                "summary": "Actualizar usuario",
                "description": "Actualiza la información de un usuario existente",
                "parameters": [
                    {
                        "name": "id_usuario",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID del usuario"
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
                            "schema": {"$ref": "#/components/schemas/Usuario"},
                            "example": {
                                "nombre": "Juan Pérez Actualizado",
                                "correo": "juan.nuevo@ejemplo.com"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Usuario actualizado exitosamente",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "success"},
                                        "code": {"type": "integer", "example": 200},
                                        "message": {"type": "string", "example": "Operación exitosa"},
                                        "data": {"$ref": "#/components/schemas/Usuario"},
                                        "error": {"type": "null"}
                                    }
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "No autorizado",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "error"},
                                        "code": {"type": "integer", "example": 401},
                                        "message": {"type": "string", "example": "Acceso inautorizado"}
                                    }
                                }
                            }
                        }
                    },
                    "403": {
                        "description": "Prohibido",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "error"},
                                        "code": {"type": "integer", "example": 403},
                                        "message": {"type": "string", "example": "No tienes permisos para realizar esta acción"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    )
    
    # PUT /api/v2.0/usuarios/{id_usuario}/foto-perfil - Actualizar foto de perfil
    spec.path(
        path="/api/v2.0/usuarios/{id_usuario}/foto-perfil",
        operations={
            "put": {
                "tags": ["Usuarios"],
                "summary": "Actualizar foto de perfil",
                "description": "Actualiza la foto de perfil de un usuario",
                "parameters": [
                    {
                        "name": "id_usuario",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID del usuario"
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
                                        "description": "Archivo de imagen"
                                    }
                                },
                                "required": ["imagen"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Foto de perfil actualizada exitosamente",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "success"},
                                        "code": {"type": "integer", "example": 200},
                                        "message": {"type": "string", "example": "Operación exitosa"}
                                    }
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "No autorizado"
                    },
                    "403": {
                        "description": "Prohibido"
                    }
                }
            }
        }
    ) 