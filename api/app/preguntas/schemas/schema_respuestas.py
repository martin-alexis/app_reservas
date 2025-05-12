from marshmallow import fields

from api.app import ma
from api.app.preguntas.models.preguntas_model import Preguntas
from api.app.usuarios.schemas.schema_usuarios import UsuariosSchema


class RespuestaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Preguntas

    respuesta = ma.auto_field(required=True)
    fecha_respuesta = ma.auto_field(dump_only=True)
    usuarios_respuesta_id = ma.auto_field(required=True)

    # Relaciones
    usuario_respuesta = fields.Nested(UsuariosSchema, dump_only=True)

# Instancias
respuesta_partial_schema = RespuestaSchema(partial=True)
respuestas_schema = RespuestaSchema(many=True)
respuesta_schema = RespuestaSchema()
