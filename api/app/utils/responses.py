class APIResponse:
    @staticmethod
    def _build_response(status, code, message, data, **kwargs):
        response = {
            "status": status,
            "code": code,
            "message": message if message is not None else "",
            "data": data
        }
        # Añadir campos adicionales si existen (pero no sobrescribir los 4 básicos)
        for key, value in kwargs.items():
            if key not in response:
                response[key] = value
        return response, code

    @staticmethod
    def success(data=None, message="", code=200, **kwargs):
        return APIResponse._build_response("success", code, message, data, **kwargs)

    @staticmethod
    def error(data=None, message="Ha ocurrido un error", code=400, **kwargs):
        return APIResponse._build_response("error", code, message, data, **kwargs)

    @staticmethod
    def validation_error(data=None, errors=None, message="Validation error", code=422, **kwargs):
        return APIResponse._build_response("error", code, message, data, errors=errors, **kwargs)

    @staticmethod
    def not_found(data=None, resource="Resource", message=None, code=404, **kwargs):
        if message is None:
            message = f"{resource} no encontrado"
        return APIResponse._build_response("error", code, message, data, **kwargs)

    @staticmethod
    def unauthorized(data=None, message="Acceso inautorizado", code=401, **kwargs):
        return APIResponse._build_response("error", code, message, data, **kwargs)

    @staticmethod
    def forbidden(data=None, message="Acceso prohibido", code=403, **kwargs):
        return APIResponse._build_response("error", code, message, data, **kwargs)

    @staticmethod
    def pagination(data=None, page=1, per_page=10, total=0, message="", code=200, **kwargs):
        pagination_info = {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page
        }
        return APIResponse._build_response("success", code, message, data, pagination=pagination_info, **kwargs)
