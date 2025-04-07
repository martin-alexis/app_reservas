class APIResponse:
    @staticmethod
    def _build_response(status, code, message, data, error, **kwargs):
        response = {
            "status": status,
            "code": code,
            "message": message if message is not None else "",
            "error": error,
            "data": data
        }
        # Añadir campos adicionales si existen (pero no sobrescribir los 5 básicos)
        for key, value in kwargs.items():
            if key not in response:
                response[key] = value
        return response, code

    @staticmethod
    def created(data=None, message="Recurso creado con éxito", error=None, code=201, **kwargs):
        return APIResponse._build_response("success", code, message, data, error, **kwargs)

    @staticmethod
    def success(data=None, message="Operación exitosa", code=200, error=None, **kwargs):
        return APIResponse._build_response("success", code, message, data, error, **kwargs)

    @staticmethod
    def error(data=None, message="Ha ocurrido un error", code=400, error=None, **kwargs):
        return APIResponse._build_response("error", code, message, data, error, **kwargs)

    @staticmethod
    def validation_error(data=None, errors=None, message="Validation error", code=422, **kwargs):
        return APIResponse._build_response("error", code, message, data, error=errors, **kwargs)

    @staticmethod
    def not_found(data=None, resource="Recurso", message=None, code=404, error=None, **kwargs):
        if message is None:
            message = f"{resource} no encontrado"
        return APIResponse._build_response("error", code, message, data, error, **kwargs)

    @staticmethod
    def unauthorized(data=None, message="Acceso inautorizado", code=401, error=None, **kwargs):
        return APIResponse._build_response("error", code, message, data, error, **kwargs)

    @staticmethod
    def forbidden(data=None, message="Acceso prohibido", code=403, error=None, **kwargs):
        return APIResponse._build_response("error", code, message, data, error, **kwargs)

    @staticmethod
    def pagination(data=None, page=0, per_page=0, total=0, pages=0, message="Operación Exitosa", code=200, error=None,
                   **kwargs):
        pagination_info = {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": pages
        }

        # Insertar paginación al principio dentro de data
        data_with_pagination = {
            "pagination": pagination_info,
            "results": data if data is not None else []
        }

        return APIResponse._build_response("success", code, message, data_with_pagination, error, **kwargs)
