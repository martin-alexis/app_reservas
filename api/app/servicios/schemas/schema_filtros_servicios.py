from marshmallow import Schema, fields, ValidationError, validates_schema, validate

from api.app.servicios.models.disponibilidad_servicios_model import Estado
from api.app.servicios.models.tipos_servicios_model import Tipo


class FiltroServiciosSchema(Schema):
    page = fields.Int(required=True)
    per_page = fields.Int(load_default=10)
    precio_min = fields.Float(required=False)
    precio_max = fields.Float(required=False)
    categoria = fields.String(required=False, load_only=True, validate=validate.OneOf([tipo.value for tipo in Tipo]))
    disponibilidad = fields.String(required=False, load_only=True, validate=validate.OneOf([estado.value for estado in Estado]))

    busqueda = fields.Str(required=False)

    @validates_schema
    def validar_rango_precios(self, data, **kwargs):
        if 'precio_min' in data and 'precio_max' in data:
            if data['precio_min'] > data['precio_max']:
                raise ValidationError("El precio mínimo no puede ser mayor que el máximo.")

filtros_servicios_schema = FiltroServiciosSchema()