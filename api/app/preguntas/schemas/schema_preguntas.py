from marshmallow import fields

from api.app import ma
from api.app.preguntas.models.preguntas_model import Preguntas
from api.app.servicios.schemas.schema_servicios import ServiciosSchema
from api.app.usuarios.schemas.schema_usuarios import UsuariosSchema


class PreguntaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Preguntas

    id_preguntas = ma.auto_field(dump_only=True)
    pregunta = ma.auto_field(required=True)
    fecha_pregunta = ma.auto_field(dump_only=True)
    servicios_id = ma.auto_field(dump_only=True)
    usuarios_pregunta_id = ma.auto_field(dump_only=True)

    # Relaciones (solo para mostrar, no para enviar)
    servicio = fields.Nested(ServiciosSchema, dump_only=True)
    usuario_pregunta = fields.Nested(UsuariosSchema, dump_only=True)

pregunta_partial_schema = PreguntaSchema(partial=True)
preguntas_schema = PreguntaSchema(many=True)
pregunta_schema = PreguntaSchema()
