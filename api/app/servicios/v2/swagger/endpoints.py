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
                "description": (
                    "Obtiene la lista de todos los servicios disponibles en el sistema.\n\n"
                    "**Parámetros de consulta (query):**\n"
                    "- page: número de página (requerido)\n"
                    "- per_page: cantidad por página (opcional, default 10)\n"
                    "- precio_min, precio_max: filtrar por rango de precio\n"
                    "- categoria: filtrar por tipo de servicio\n"
                    "- disponibilidad: filtrar por estado (DISPONIBLE, AGOTADO, PROXIMAMENTE)\n"
                    "- busqueda: búsqueda por nombre o descripción\n"
                ),
                "parameters": [
                    {"name": "page", "in": "query", "required": True, "schema": {"type": "integer"}},
                    {"name": "per_page", "in": "query", "required": False, "schema": {"type": "integer", "default": 10}},
                    {"name": "precio_min", "in": "query", "required": False, "schema": {"type": "number"}},
                    {"name": "precio_max", "in": "query", "required": False, "schema": {"type": "number"}},
                    {"name": "categoria", "in": "query", "required": False, "schema": {"type": "string", "enum": ["GIMNASIOS Y ENTRENAMIENTOS", "ALQUILER DE VEHICULOS", "HOTELES Y HOSPEDAJES", "SALONES DE EVENTOS", "CINES Y TEATROS", "SPA Y MASAJES", "RESTAURANTES Y BARES", "OTROS"]}},
                    {"name": "disponibilidad", "in": "query", "required": False, "schema": {"type": "string", "enum": ["DISPONIBLE", "AGOTADO", "PROXIMAMENTE"]}},
                    {"name": "busqueda", "in": "query", "required": False, "schema": {"type": "string"}}
                ],
                "responses": {
                    "200": {
                        "description": "Lista de servicios obtenida exitosamente",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 200,
                                    "message": "Operación exitosa",
                                    "data": [
                                        {
                                            "id_servicios": 1,
                                            "nombre": "Hotel Central",
                                            "descripcion": "Hotel céntrico con desayuno incluido",
                                            "precio": 120.0,
                                            "ubicacion": "Madrid, España",
                                            "imagen": "https://.../hotel.png",
                                            "tipos_servicio": "HOTELES Y HOSPEDAJES",
                                            "tipo_servicio": {"id_tipos_servicio": 3, "tipo": "HOTELES Y HOSPEDAJES"},
                                            "disponibilidad": {"id_disponibilidad_servicio": 1, "estado": "DISPONIBLE"},
                                            "usuarios_proveedores_id": 5
                                        }
                                    ],
                                    "error": None
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Error de validación de parámetros",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "error",
                                    "code": 422,
                                    "message": "Validation error",
                                    "error": {"page": ["El campo es obligatorio."]},
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
            "post": {
                "tags": ["Servicios"],
                "summary": "Crear un nuevo servicio",
                "description": (
                    "Crea un nuevo servicio en el sistema.\n\n"
                    "**Requiere autenticación JWT y uno de los siguientes roles:** PROVEEDOR o ADMIN.\n"
                    "**Validaciones:**\n"
                    "- Todos los campos son obligatorios salvo imagen.\n"
                    "- El campo 'imagen' es obligatorio y debe ser un archivo válido (jpg, png, etc.).\n"
                    "- 'tipos_servicio' debe ser uno de los valores válidos.\n"
                    "- 'disponibilidad_servicio' debe ser uno de los valores válidos.\n"
                ),
                "security": [{"bearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "multipart/form-data": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "nombre": {"type": "string", "example": "Hotel Central"},
                                    "descripcion": {"type": "string", "example": "Hotel céntrico con desayuno incluido"},
                                    "precio": {"type": "number", "example": 120.0},
                                    "ubicacion": {"type": "string", "example": "Madrid, España"},
                                    "tipos_servicio": {"type": "string", "example": "HOTELES Y HOSPEDAJES"},
                                    "disponibilidad_servicio": {"type": "string", "example": "DISPONIBLE"},
                                    "imagen": {"type": "string", "format": "binary", "description": "Archivo de imagen (jpg, png, etc.)"}
                                },
                                "required": ["nombre", "descripcion", "precio", "ubicacion", "tipos_servicio", "disponibilidad_servicio", "imagen"]
                            },
                            "example": {
                                "nombre": "Hotel Central",
                                "descripcion": "Hotel céntrico con desayuno incluido",
                                "precio": 120.0,
                                "ubicacion": "Madrid, España",
                                "tipos_servicio": "HOTELES Y HOSPEDAJES",
                                "disponibilidad_servicio": "DISPONIBLE",
                                "imagen": "(archivo de imagen)"
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Servicio creado exitosamente",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 201,
                                    "message": "Recurso creado con éxito",
                                    "data": {
                                        "id_servicios": 10,
                                        "nombre": "Hotel Central",
                                        "descripcion": "Hotel céntrico con desayuno incluido",
                                        "precio": 120.0,
                                        "ubicacion": "Madrid, España",
                                        "imagen": "https://.../hotel.png",
                                        "tipos_servicio": "HOTELES Y HOSPEDAJES",
                                        "tipo_servicio": {"id_tipos_servicio": 3, "tipo": "HOTELES Y HOSPEDAJES"},
                                        "disponibilidad": {"id_disponibilidad_servicio": 1, "estado": "DISPONIBLE"},
                                        "usuarios_proveedores_id": 5
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
                                        "nombre": ["El nombre es obligatorio."],
                                        "precio": ["El precio debe ser un número positivo."]
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
    
    # GET /api/v2.0/servicios/{id_servicio} - Obtener servicio por ID
    spec.path(
        path="/api/v2.0/servicios/{id_servicio}",
        operations={
            "get": {
                "tags": ["Servicios"],
                "summary": "Obtener servicio por ID",
                "description": (
                    "Obtiene la información de un servicio específico por su ID.\n\n"
                    "No requiere autenticación.\n"
                ),
                "parameters": [
                    {"name": "id_servicio", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del servicio"}
                ],
                "responses": {
                    "200": {
                        "description": "Servicio encontrado",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 200,
                                    "message": "Operación exitosa",
                                    "data": {
                                        "id_servicios": 1,
                                        "nombre": "Hotel Central",
                                        "descripcion": "Hotel céntrico con desayuno incluido",
                                        "precio": 120.0,
                                        "ubicacion": "Madrid, España",
                                        "imagen": "https://.../hotel.png",
                                        "tipos_servicio": "HOTELES Y HOSPEDAJES",
                                        "tipo_servicio": {"id_tipos_servicio": 3, "tipo": "HOTELES Y HOSPEDAJES"},
                                        "disponibilidad": {"id_disponibilidad_servicio": 1, "estado": "DISPONIBLE"},
                                        "usuarios_proveedores_id": 5
                                    },
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
            },
            "patch": {
                "tags": ["Servicios"],
                "summary": "Actualizar servicio",
                "description": (
                    "Actualiza la información de un servicio existente.\n\n"
                    "**Requiere autenticación JWT y uno de los siguientes roles:** PROVEEDOR o ADMIN.\n"
                    "**Validaciones:**\n"
                    "- Solo los campos enviados serán actualizados.\n"
                    "- Permisos: solo el proveedor dueño o un ADMIN pueden modificar el servicio.\n"
                ),
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {"name": "id_servicio", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del servicio a actualizar"}
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Servicio"},
                            "example": {
                                "nombre": "Hotel Central Actualizado",
                                "precio": 150.0
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Servicio actualizado exitosamente",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 200,
                                    "message": "Operación exitosa",
                                    "data": {
                                        "id_servicios": 1,
                                        "nombre": "Hotel Central Actualizado",
                                        "descripcion": "Hotel céntrico con desayuno incluido",
                                        "precio": 150.0,
                                        "ubicacion": "Madrid, España",
                                        "imagen": "https://.../hotel.png",
                                        "tipos_servicio": "HOTELES Y HOSPEDAJES",
                                        "tipo_servicio": {"id_tipos_servicio": 3, "tipo": "HOTELES Y HOSPEDAJES"},
                                        "disponibilidad": {"id_disponibilidad_servicio": 1, "estado": "DISPONIBLE"},
                                        "usuarios_proveedores_id": 5
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
                                        "precio": ["El precio debe ser un número positivo."]
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
            },
            "delete": {
                "tags": ["Servicios"],
                "summary": "Eliminar servicio",
                "description": (
                    "Elimina un servicio existente.\n\n"
                    "**Requiere autenticación JWT y uno de los siguientes roles:** PROVEEDOR o ADMIN.\n"
                    "**Permisos:** Solo el proveedor dueño o un ADMIN pueden eliminar el servicio.\n"
                ),
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {"name": "id_servicio", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del servicio a eliminar"}
                ],
                "responses": {
                    "200": {
                        "description": "Servicio eliminado exitosamente",
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
    
    # PUT /api/v2.0/servicios/{id_servicio}/imagen-servicio - Actualizar imagen del servicio
    spec.path(
        path="/api/v2.0/servicios/{id_servicio}/imagen-servicio",
        operations={
            "put": {
                "tags": ["Servicios"],
                "summary": "Actualizar imagen del servicio",
                "description": (
                    "Actualiza la imagen de un servicio existente.\n\n"
                    "**Requiere autenticación JWT y uno de los siguientes roles:** PROVEEDOR o ADMIN.\n"
                    "**Permisos:** Solo el proveedor dueño o un ADMIN pueden modificar la imagen.\n"
                    "**Validaciones:**\n"
                    "- El campo 'imagen' es obligatorio y debe ser un archivo válido (jpg, png, etc.).\n"
                ),
                "security": [{"bearerAuth": []}],
                "parameters": [
                    {"name": "id_servicio", "in": "path", "required": True, "schema": {"type": "integer"}, "description": "ID del servicio a actualizar"}
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
                        "description": "Imagen actualizada exitosamente",
                        "content": {
                            "application/json": {
                                "example": {
                                    "status": "success",
                                    "code": 200,
                                    "message": "Operación exitosa",
                                    "data": {
                                        "id_servicios": 1,
                                        "nombre": "Hotel Central",
                                        "imagen": "https://.../hotel_actualizado.png"
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
                                    "error": "No se envió ninguna imagen",
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