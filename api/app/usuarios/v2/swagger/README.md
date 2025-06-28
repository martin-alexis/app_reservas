# Documentación Swagger - Módulo Usuarios v2

Este directorio contiene la documentación Swagger específica para el módulo de usuarios v2.

## Estructura

```
swagger/
├── __init__.py          # Módulo Python
├── schemas.py           # Registro de esquemas Marshmallow
├── endpoints.py         # Documentación de endpoints
├── initializer.py       # Coordinador de inicialización
└── README.md           # Este archivo
```

## Archivos

### `schemas.py`
Registra los esquemas Marshmallow específicos de usuarios en apispec:
- `Usuario` - Esquema principal de usuarios
- `UsuarioRol` - Esquema de relación usuario-rol
- `TipoUsuario` - Esquema de tipos de usuario
- `Rol` - Esquema de roles

### `endpoints.py`
Documenta todos los endpoints específicos de usuarios:
- `POST /api/v2.0/usuarios` - Crear usuario
- `GET /api/v2.0/usuarios/{id}` - Obtener usuario
- `PATCH /api/v2.0/usuarios/{id}` - Actualizar usuario
- `PUT /api/v2.0/usuarios/{id}/foto-perfil` - Actualizar foto

### `initializer.py`
Coordina la inicialización de toda la documentación del módulo:
1. Registra esquemas
2. Documenta endpoints
3. Proporciona feedback de inicialización

## Uso

La documentación se inicializa automáticamente al arrancar la aplicación a través de:
```python
from api.app.usuarios.v2.swagger.initializer import initialize_usuario_documentation
initialize_usuario_documentation()
```

## Ventajas de esta estructura

1. **Modularidad**: Cada módulo maneja su propia documentación
2. **Mantenibilidad**: Fácil de mantener y actualizar
3. **Escalabilidad**: Fácil agregar nuevos módulos
4. **Separación de responsabilidades**: Esquemas y endpoints separados
5. **Reutilización**: Esquemas pueden ser reutilizados en otros módulos 