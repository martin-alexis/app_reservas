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
            if key not in response:  # Evita sobrescribir los campos básicos
                response[key] = value
        return response, code

    @staticmethod
    def success(message="", data=None, code=200, **kwargs):
        return APIResponse._build_response("success", code, message, data, **kwargs)

    @staticmethod
    def error(message="", code=400, data=None, **kwargs):
        return APIResponse._build_response("error", code, message, data, **kwargs)

    @staticmethod
    def validation_error(errors, message="Validation error", code=422):
        return APIResponse._build_response("error", code, message, None, errors=errors)

    @staticmethod
    def not_found(resource="Resource", code=404):
        message = f"{resource} not found"
        return APIResponse._build_response("error", code, message, None)

    @staticmethod
    def unauthorized(message="Unauthorized access", code=401):
        return APIResponse._build_response("error", code, message, None)

    @staticmethod
    def forbidden(message="Access forbidden", code=403):
        return APIResponse._build_response("error", code, message, None)

    @staticmethod
    def pagination(data, page, per_page, total, message=""):
        pagination_info = {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page
        }
        return APIResponse._build_response("success", 200, message, data, pagination=pagination_info)