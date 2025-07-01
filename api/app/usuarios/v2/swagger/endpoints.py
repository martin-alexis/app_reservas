from api.app.swagger.apispec_config import spec
from api.app.usuarios.models.tipos_usuarios_model import Tipo
from api.app.usuarios.models.roles_model import TipoRoles

def document_usuario_endpoints():
    """Documenta todos los endpoints del módulo de usuarios v2"""
    
    # POST /api/v2.0/usuarios
    tipos_usuario_validos = [tipo.value for tipo in Tipo]
    tipo_roles_validos = [rol.value for rol in TipoRoles]
    spec.path(
        path="/api/v2.0/usuarios",
        operations={
            "post": {
                "tags": ["Usuarios"],
                "summary": "Crear un nuevo usuario",
                "description": (
                    "Crea un nuevo usuario en el sistema.\n\n"
                    "Validaciones por campo:\n"
                    "- nombre: requerido, string.\n"
                    "- correo: requerido, string, formato email válido, único.\n"
                    "- telefono: requerido, string, solo dígitos, longitud 7-15, único.\n"
                    "- contrasena: requerido, string, 8-32 caracteres, al menos una letra y un número.\n"
                    f"- tipos_usuario: requerido, string, Enum válido ({', '.join(tipos_usuario_validos)}).\n"
                    f"- tipo_roles: requerido, lista de strings, al menos uno, Enum válido ({', '.join(tipo_roles_validos)}).\n"
                    "- imagen: string (opcional, si no se envía se asigna una por defecto).\n"
                ),
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Usuario"},
                            "example": {
                                "nombre": "Juan Pérez",
                                "correo": "juan.perez@email.com",
                                "telefono": "1234567890",
                                "contrasena": "Password123",
                                "tipos_usuario": tipos_usuario_validos[0],
                                "tipo_roles": [tipo_roles_validos[0]]
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Usuario creado exitosamente",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 201,
                                    "message": "Recurso creado con éxito",
                                    "data": None,
                                    "error": None
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Error de validación",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 422,
                                    "message": "Validation error",
                                    "error": {
                                        "correo": [
                                            "El correo ya está registrado.",
                                            "Correo invalido. Ingresa un correo válido en formato 'usuario@dominio.com'."
                                        ],
                                        "telefono": [
                                            "Telefono invalido. El teléfono solo puede contener entre 7 y 15 dígitos numéricos.",
                                            "El teléfono ya está registrado."
                                        ],
                                        "contrasena": [
                                            "La contraseña debe tener entre 8 y 32 caracteres.",
                                            "La contraseña debe contener al menos una letra y un número."
                                        ],
                                        "tipos_usuario": [
                                            f"Tipo de usuario inválido. Debe ser uno de: {', '.join(tipos_usuario_validos)}."
                                        ],
                                        "tipo_roles": [
                                            "Se requiere al menos un rol.",
                                            f"Rol inválido. Debe ser uno de: {', '.join(tipo_roles_validos)}."
                                        ]
                                    },
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
    
    # GET /api/v2.0/usuarios/{id_usuario} - Obtener usuario
    spec.path(
        path="/api/v2.0/usuarios/{id_usuario}",
        operations={
            "get": {
                "tags": ["Usuarios"],
                "summary": "Obtener usuario por ID",
                "description": (
                    "Obtiene la información de un usuario específico por su ID.\n\n"
                    "**Notas:**\n"
                    "- No requiere autenticación.\n"
                    "- Devuelve todos los campos del usuario, incluyendo roles y tipo de usuario.\n"
                ),
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
                                "example": {
                                    "status": "success",
                                    "code": 200,
                                    "message": "Operación exitosa",
                                    "data": {
                                        "id_usuarios": 1,
                                        "nombre": "Juan Pérez",
                                        "correo": "juan.perez@email.com",
                                        "telefono": "1234567890",
                                        "imagen": "https://res.cloudinary.com/dfnjifn4w/image/upload/v1740232796/525e350a-f2e9-4b04-9cf8-93d54bffc2ec.png",
                                        "tipos_usuario": "PARTICULAR",
                                        "tipo_usuario": {
                                            "id_tipos_usuario": 1,
                                            "tipo": "PARTICULAR"
                                        },
                                        "roles": [
                                            {
                                                "id_usuarios_tiene_roles": 1,
                                                "usuarios_id": 1,
                                                "roles_id": 2,
                                                "rol": {
                                                    "id_roles": 2,
                                                    "tipo": "CLIENTE"
                                                }
                                            }
                                        ]
                                    },
                                    "error": None
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
            },
            "patch": {
                "tags": ["Usuarios"],
                "summary": "Actualizar usuario",
                "description": (
                    "Actualiza los datos de un usuario existente.\n\n"
                    "**Requiere autenticación JWT y uno de los siguientes roles:** ADMIN, CLIENTE o PROVEEDOR.\n"
                    "**Validaciones:**\n"
                    "- Solo los campos enviados serán actualizados.\n"
                    "- Correo y teléfono deben ser únicos.\n"
                    "- Formato de email válido.\n"
                    "- Teléfono: solo dígitos, 7-15 caracteres.\n"
                    "- Contraseña: 8-32 caracteres, al menos una letra y un número.\n"
                    "- tipos_usuario: Enum válido ('PARTICULAR', 'EMPRESA').\n"
                    "- tipo_roles: Al menos uno, Enum válido ('ADMIN', 'CLIENTE', 'PROVEEDOR').\n"
                    "- Si se eliminan roles de proveedor, el usuario no debe tener servicios activos.\n"
                    "- Solo el usuario dueño o un ADMIN pueden modificar el usuario.\n"
                ),
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {"name": "id_usuario", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del usuario a actualizar"},
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Usuario"},
                            "example": {
                                "nombre": "Juan Pérez Actualizado",
                                "correo": "juan.nuevo@email.com",
                                "telefono": "1234567890",
                                "tipos_usuario": "EMPRESA",
                                "tipo_roles": ["CLIENTE"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Usuario actualizado exitosamente",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 200,
                                    "message": "Operación exitosa",
                                    "data": {
                                        "id_usuarios": 1,
                                        "nombre": "Juan Pérez Actualizado",
                                        "correo": "juan.nuevo@email.com",
                                        "telefono": "1234567890",
                                        "imagen": "https://res.cloudinary.com/dfnjifn4w/image/upload/v1740232796/525e350a-f2e9-4b04-9cf8-93d54bffc2ec.png",
                                        "tipos_usuario": "EMPRESA",
                                        "tipo_usuario": {
                                            "id_tipos_usuario": 2,
                                            "tipo": "EMPRESA"
                                        },
                                        "roles": [
                                            {
                                                "id_usuarios_tiene_roles": 2,
                                                "usuarios_id": 1,
                                                "roles_id": 3,
                                                "rol": {
                                                    "id_roles": 3,
                                                    "tipo": "CLIENTE"
                                                }
                                            }
                                        ]
                                    },
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
    
    # PUT /api/v2.0/usuarios/{id_usuario}/foto-perfil - Actualizar foto de perfil
    spec.path(
        path="/api/v2.0/usuarios/{id_usuario}/foto-perfil",
        operations={
            "put": {
                "tags": ["Usuarios"],
                "summary": "Actualizar foto de perfil del usuario",
                "description": (
                    "Actualiza la foto de perfil de un usuario.\n\n"
                    "**Requiere autenticación JWT y uno de los siguientes roles:** ADMIN, CLIENTE o PROVEEDOR.\n"
                    "**Validaciones:**\n"
                    "- El campo 'imagen' es obligatorio y debe ser un archivo válido (jpg, png, etc.).\n"
                    "- Solo el usuario autenticado o un ADMIN pueden actualizar la foto de perfil.\n"
                    "- Si el usuario no existe, retorna 404.\n"
                    "- Si no se envía imagen, retorna 400.\n"
                    "- Si el token es inválido o falta, retorna 401.\n"
                    "- Si el usuario autenticado no tiene permisos, retorna 403.\n"
                ),
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {"name": "id_usuario", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del usuario a actualizar"},
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "multipart/form-data": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "imagen": {"type": "string", "format": "binary", "description": "Archivo de imagen (jpg, png, etc.)"}
                                },
                                "required": ["imagen"]
                            },
                            "example": {
                                "imagen": "(archivo de imagen)"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Foto de perfil actualizada exitosamente",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 200,
                                    "message": "Operación exitosa",
                                    "data": {
                                        "id_usuarios": 1,
                                        "nombre": "Juan Pérez",
                                        "correo": "juan.perez@email.com",
                                        "telefono": "1234567890",
                                        "imagen": "https://res.cloudinary.com/dfnjifn4w/image/upload/v1740232796/imagen_actualizada.png",
                                        "tipos_usuario": "PARTICULAR",
                                        "tipo_usuario": {
                                            "id_tipos_usuario": 1,
                                            "tipo": "PARTICULAR"
                                        },
                                        "roles": [
                                            {
                                                "id_usuarios_tiene_roles": 1,
                                                "usuarios_id": 1,
                                                "roles_id": 2,
                                                "rol": {
                                                    "id_roles": 2,
                                                    "tipo": "CLIENTE"
                                                }
                                            }
                                        ]
                                    },
                                    "error": None
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Error de validación o falta de imagen",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 400,
                                    "message": "Ha ocurrido un error",
                                    "error": "La imagen no ha sido proporcionada.",
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
    
    # POST /api/v2.0/login - Login de usuario
    spec.path(
        path="/api/v2.0/login",
        operations={
            "post": {
                "tags": ["Auth"],
                "summary": "Login de usuario (JWT)",
                "description": (
                    "Autentica a un usuario y retorna un JWT válido para acceder a los endpoints protegidos.\n\n"
                    "**Validaciones:**\n"
                    "- El correo debe ser válido y estar registrado.\n"
                    "- La contraseña debe ser correcta.\n"
                    "- Ambos campos son obligatorios.\n"
                ),
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "correo": {"type": "string", "format": "email", "description": "Correo electrónico registrado"},
                                    "contrasena": {"type": "string", "description": "Contraseña del usuario"}
                                },
                                "required": ["correo", "contrasena"]
                            },
                            "example": {
                                "correo": "usuario@email.com",
                                "contrasena": "Password123"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Login exitoso. Devuelve el JWT.",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 200,
                                    "message": "Operación exitosa",
                                    "data": {
                                        "jwt_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZW1haWwiOiJ1c2VyQGVtYWlsLmNvbSIsInJvbGVzIjpbIkNMSUVOVEUiXSwiaWF0IjoxNjg1NjYwMDAwLCJleHAiOjE2ODU3NDY0MDB9.abc123..."
                                    },
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
                                    "error": {
                                        "correo": ["El correo es obligatorio."],
                                        "contrasena": ["La contraseña es obligatoria."]
                                    },
                                    "data": None
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Credenciales incorrectas",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 401,
                                    "message": "Correo o contraseña incorrectos",
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