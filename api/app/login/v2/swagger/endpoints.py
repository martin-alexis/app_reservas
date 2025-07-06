from api.app.swagger.apispec_config import spec

def document_login_endpoints():
    """Documenta todos los endpoints del módulo de login v2"""
    
    # Endpoint: Login JWT
    spec.path(
        path="/api/v2.0/login",
        operations={
            "post": {
                "tags": ["Autenticación"],
                "summary": "Iniciar sesión con JWT",
                "description": "Autentica un usuario usando correo y contraseña, retornando un token JWT para futuras peticiones.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["correo", "contrasena"],
                                "properties": {
                                    "correo": {
                                        "type": "string",
                                        "format": "email",
                                        "description": "Correo electrónico del usuario",
                                        "example": "usuario@ejemplo.com"
                                    },
                                    "contrasena": {
                                        "type": "string",
                                        "description": "Contraseña del usuario",
                                        "example": "miContraseña123"
                                    }
                                }
                            },
                            "examples": {
                                "Login válido": {
                                    "summary": "Credenciales válidas",
                                    "value": {
                                        "correo": "usuario@ejemplo.com",
                                        "contrasena": "miContraseña123"
                                    }
                                },
                                "Login inválido": {
                                    "summary": "Credenciales incorrectas",
                                    "value": {
                                        "correo": "usuario@ejemplo.com",
                                        "contrasena": "contraseñaIncorrecta"
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Login exitoso. Retorna token JWT.",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 200,
                                    "message": "Operación exitosa",
                                    "error": None,
                                    "data": {
                                        "jwt_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZFVzdWFyaW8iOjEsImVtYWlsIjoiandhbi5wZXJlekBnbWFpbC5jb20iLCJyb2xlcyI6WyJDTElFTlRFIl0sImV4cCI6MTcwMDAwMDAwMCwiaWF0IjoxNzAwMDAwMDAwfQ.example"
                                    }
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
                    "422": {
                        "description": "Error de validación en los datos de entrada",
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
                    "500": {
                        "description": "Error interno del servidor",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 500,
                                    "message": "Ha ocurrido un error",
                                    "error": "Error interno del servidor",
                                    "data": None
                                }
                            }
                        }
                    }
                }
            }
        }
    )
    
    # Endpoint: Login Google (inicio del flujo OAuth)
    spec.path(
        path="/api/v2.0/google/login",
        operations={
            "get": {
                "tags": ["Autenticación Google"],
                "summary": "Iniciar flujo de autenticación con Google",
                "description": "Inicia el flujo de autenticación OAuth 2.0 con Google. Redirige al usuario a la página de autorización de Google.",
                "responses": {
                    "302": {
                        "description": "Redirección a Google OAuth",
                        "headers": {
                            "Location": {
                                "description": "URL de autorización de Google",
                                "schema": {
                                    "type": "string",
                                    "example": "https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=..."
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
                                    "message": "Error iniciando autenticación con Google",
                                    "error": "Error interno del servidor",
                                    "data": None
                                }
                            }
                        }
                    }
                }
            }
        }
    )
    
    # Endpoint: Callback de Google OAuth
    spec.path(
        path="/api/v2.0/google/callback",
        operations={
            "get": {
                "tags": ["Autenticación Google"],
                "summary": "Callback de autenticación Google",
                "description": "Endpoint de callback que Google llama después de la autorización exitosa. Procesa el código de autorización y retorna un token JWT o información del usuario nuevo.",
                "parameters": [
                    {
                        "name": "code",
                        "in": "query",
                        "required": True,
                        "description": "Código de autorización proporcionado por Google",
                        "schema": {
                            "type": "string"
                        },
                        "example": "4/0AfJohXn..."
                    },
                    {
                        "name": "state",
                        "in": "query",
                        "required": True,
                        "description": "Estado CSRF para prevenir ataques",
                        "schema": {
                            "type": "string"
                        },
                        "example": "abc123def456..."
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Autenticación exitosa",
                        "content": {
                            "application/json": {
                                "examples": {
                                    "Usuario existente": {
                                        "summary": "Usuario ya registrado en el sistema",
                                        "value": {
                                            "status": "success",
                                            "code": 200,
                                            "message": "Operación exitosa",
                                            "error": None,
                                            "data": {
                                                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZFVzdWFyaW8iOjEsImVtYWlsIjoiandhbi5wZXJlekBnbWFpbC5jb20iLCJyb2xlcyI6WyJDTElFTlRFIl0sImV4cCI6MTcwMDAwMDAwMCwiaWF0IjoxNzAwMDAwMDAwfQ.example"
                                            }
                                        }
                                    },
                                    "Usuario nuevo": {
                                        "summary": "Usuario nuevo que necesita registro",
                                        "value": {
                                            "status": "success",
                                            "code": 200,
                                            "message": "Operación exitosa",
                                            "error": None,
                                            "data": {
                                                "usuario_nuevo": True,
                                                "google_user": {
                                                    "nombre": "Juan Pérez",
                                                    "correo": "juan.perez@gmail.com",
                                                    "picture": "https://lh3.googleusercontent.com/a/ACg8ocJ..."
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Estado CSRF inválido",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 400,
                                    "message": "Estado inválido",
                                    "error": None,
                                    "data": None
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Error obteniendo datos del usuario de Google",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 401,
                                    "message": "Error obteniendo datos del usuario",
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
                                    "message": "Error en autenticación",
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
    
    # Endpoint: Logout Google
    spec.path(
        path="/api/v2.0/google/logout",
        operations={
            "post": {
                "tags": ["Autenticación Google"],
                "summary": "Cerrar sesión",
                "description": "Invalida el token JWT actual, cerrando la sesión del usuario.",
                "security": [
                    {
                        "bearerAuth": []
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Sesión cerrada exitosamente",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 200,
                                    "message": "Sesión cerrada exitosamente",
                                    "error": None,
                                    "data": None
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Token no proporcionado o inválido",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 401,
                                    "message": "Token no proporcionado",
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
                                    "message": "Error al cerrar sesión",
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