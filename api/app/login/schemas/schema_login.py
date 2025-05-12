from marshmallow import Schema, fields, validate

class LoginSchema(Schema):
    correo = fields.Email(
        required=True,
        validate=validate.Email(error="Correo inválido. Ingresa un correo válido en formato 'usuario@dominio.com'."),
        error_messages={"required": "El correo es obligatorio."}
    )

    contrasena = fields.Str(
        required=True,
        load_only=True,
        # validate=[
        #     validate.Length(min=8, max=32, error="La contraseña debe tener entre 8 y 32 caracteres."),
        #     validate.Regexp(
        #         regex=r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]+$",
        #         error="La contraseña debe contener al menos una letra y un número."
        #     )
        # ],
        error_messages={"required": "La contraseña es obligatoria."}
    )

login_schema = LoginSchema()
