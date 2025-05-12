from marshmallow import validates_schema, ValidationError, fields, validate
from datetime import datetime

from api.app import ma
from api.app.reservas.models.estados_reserva_model import EstadoReserva
from api.app.reservas.schemas.schema_estados_reserva import EstadosReservaSchema
from api.app.reservas.models.reservas_model import Reservas


class ReservasSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Reservas

    id_reservas = ma.auto_field()
    fecha_creacion_reserva = ma.auto_field()
    fecha_inicio_reserva = ma.auto_field(required=True)
    fecha_fin_reserva = ma.auto_field(required=True)
    servicios_id = ma.auto_field(dump_only=True)
    estados_reserva = fields.String(
        required=True,
        load_only=True,
        validate=validate.OneOf([estado.value for estado in EstadoReserva])
    )

    estado_reserva = fields.Nested(EstadosReservaSchema, dump_only=True)

    @validates_schema
    def validar_fechas(self, data, **kwargs):
        inicio = data.get("fecha_inicio_reserva")
        fin = data.get("fecha_fin_reserva")

        if inicio and fin:
            if fin < inicio:
                raise ValidationError("La fecha de fin debe ser posterior a la de inicio", field_name="fecha_fin_reserva")
            if inicio < datetime.now():
                raise ValidationError("La fecha de inicio no puede estar en el pasado", field_name="fecha_inicio_reserva")


# Instancias del esquema para serialización
reserva_partial_schema = ReservasSchema(partial=True)
reserva_schema = ReservasSchema()
reservas_schema = ReservasSchema(many=True)