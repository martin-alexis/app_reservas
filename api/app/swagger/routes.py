from flask import Blueprint, jsonify
from api.app.swagger.apispec_config import spec

swagger_bp = Blueprint("swagger", __name__)

@swagger_bp.route("/swagger.json")
def swagger_json():
    """Endpoint para obtener la documentación OpenAPI en formato JSON"""
    return jsonify(spec.to_dict())

@swagger_bp.route("/docs")
def swagger_ui():
    """Endpoint para servir Swagger UI"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Booking API - Swagger UI</title>
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui.css" />
        <style>
            html { box-sizing: border-box; overflow: -moz-scrollbars-vertical; overflow-y: scroll; }
            *, *:before, *:after { box-sizing: inherit; }
            body { margin:0; background: #fafafa; }
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-bundle.js"></script>
        <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-standalone-preset.js"></script>
        <script>
            window.onload = function() {
                const ui = SwaggerUIBundle({
                    url: '/swagger.json',
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIStandalonePreset
                    ],
                    plugins: [
                        SwaggerUIBundle.plugins.DownloadUrl
                    ],
                    layout: "BaseLayout",
                    validatorUrl: null
                });
            }
        </script>
    </body>
    </html>
    """ 