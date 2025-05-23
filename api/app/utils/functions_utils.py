from werkzeug.utils import secure_filename
import cloudinary.uploader

from api.app.servicios.models.servicios_model import Servicios
from api.app.usuarios.models.roles_model import Roles, TipoRoles
from api.app.usuarios.models.usuarios_model import Usuarios
from api.app.usuarios.models.usuarios_tiene_roles_model import UsuariosTieneRoles
from api.app.utils.responses import APIResponse

class FunctionsUtils:
    @staticmethod
    def get_roles_user(id_usuario):
        try:
            roles_user = []
            user_role_relations = UsuariosTieneRoles.query.filter_by(usuarios_id=id_usuario).all()

            for relation in user_role_relations:
                role = Roles.query.get(relation.roles_id)
                if role:
                    role_str = str(role.tipo).replace('TipoRoles.', '')
                    roles_user.append(role_str)
            return roles_user
        except Exception as e:
            return APIResponse.error(error=str(e))
    # @staticmethod
    # def get_usertype(id_usuario):
    #     try:
    #         type_user = TiposUsuario.query.filter_by(id_tipos_usuario=id_usuario.tipos_usuario_id).first()
    #         return str(type_user.tipo).replace('Tipo.', '')
    #     except Exception as e:
    #         return APIResponse.error(None, str(e))
    @staticmethod
    def obtener_usuario_por_correo(correo):
            usuario = Usuarios.query.filter_by(correo=correo).first()

            if usuario:
                return usuario
            else:
                return None

    @staticmethod
    def subir_imagen_cloudinary(imagen, id_usuario_token, modelo):
        try:

            if not imagen:
                return None

            imagen_filename = secure_filename(imagen.filename)
            carpeta_principal = f'app_reservas/{modelo}'
            carpeta_usuario = f"id_{id_usuario_token}"
            carpeta_completa = f"{carpeta_principal}/{carpeta_usuario}"

            upload_result = cloudinary.uploader.upload(
                imagen,
                folder=carpeta_completa,
                public_id=imagen_filename
            )
            return upload_result['secure_url']

        except Exception as e:
            return APIResponse.error(None, error=str(e), code=500, message='Error al subir la imagen a Cloudinary')


    @staticmethod
    def existe_registro(id_registro, modelo):
        registro = modelo.query.get(id_registro)
        if registro is None:
            raise ValueError(f"{modelo.__name__}")
        return registro

    @staticmethod
    def verificar_permisos(objeto, id_usuario_token):
        """
        Verifica si un usuario tiene permiso para acceder o modificar un objeto determinado.

        Parámetros:
        - objeto: instancia de un modelo (por ejemplo, Usuarios o Servicios).
        - id_usuario_token: ID del usuario autenticado (extraído del token JWT).

        Excepciones:
        - Lanza PermissionError si el usuario no tiene permisos sobre el objeto y no es administrador.
        """
        roles = FunctionsUtils.get_roles_user(id_usuario_token)

        if isinstance(objeto, Usuarios):
            id_nombre = Usuarios.id_usuarios.key

        elif isinstance(objeto, Servicios):
            id_nombre = Servicios.usuarios_proveedores_id.key

        else:
            raise ValueError("Tipo de objeto no soportado")

        # Verificación de permisos
        if getattr(objeto, id_nombre) != id_usuario_token and (not roles or TipoRoles.ADMIN.value not in roles):
            raise PermissionError("No tienes permisos para realizar esta acción")

    @staticmethod
    def verificar_permisos_reserva(servicio, reserva, id_usuario_token):
        """Verifica permisos para una reserva de un servicio"""
        # Primero verificar permisos sobre el servicio
        FunctionsUtils.verificar_permisos(servicio, id_usuario_token)

        # Luego verificar que la reserva pertenezca al servicio
        if reserva.servicios_id != servicio.id_servicios:
            raise PermissionError("La reserva no pertenece a este servicio")

    @staticmethod
    def verificar_permisos_pago(servicio, reserva, pago, id_usuario_token):
        """Verifica permisos para un pago de una reserva de un servicio"""
        # Verificar la cadena completa de relaciones
        FunctionsUtils.verificar_permisos_reserva(servicio, reserva, id_usuario_token)

        # Verificar que el pago pertenezca a la reserva
        if pago.reservas_id != reserva.id_reservas:
            raise PermissionError("El pago no pertenece a esta reserva")

    @staticmethod
    def obtener_ids_de_enums(modelo, campo_enum, valores_enum, id_campo):
        """
        Convierte una lista de valores de un Enum en sus respectivos IDs en la base de datos.

        :param modelo: Modelo de SQLAlchemy (ej. Roles).
        :param campo_enum: Campo del modelo que contiene el Enum (ej. Roles.tipo).
        :param valores_enum: Lista de valores del Enum a buscar en la base de datos.
        :param id_campo: Nombre del campo de ID en la base de datos (ej. "id_roles").
        :return: Lista de IDs correspondientes a los valores encontrados.
        """

        # Si valores_enum es un string, lo convertimos en lista
        if isinstance(valores_enum, str):
            valores_enum = [valores_enum]

        registros = modelo.query.filter(campo_enum.in_(valores_enum)).all()
        return [getattr(registro, id_campo) for registro in registros]

    @staticmethod
    def renombrar_campo(data, campo_original, nuevo_nombre):
        if campo_original in data:
            data[nuevo_nombre] = data.pop(campo_original)
        return data

    @staticmethod
    def pasar_ids(data, campo, ids):
        """
        Convierte un valor string en un ID utilizando una lista de IDs proporcionada.

        :param data: Diccionario con los datos a modificar.
        :param campo: Nombre del campo que se pasará los ids.
        :param ids: lista de IDs.
        :return: Diccionario con el ids asignados.
        """
        if campo in data:
            if campo == 'tipo_roles':
                data[campo] = ids
            else:
                data[campo] = ids[0]
        return data
