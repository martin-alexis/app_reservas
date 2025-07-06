from werkzeug.utils import secure_filename
import cloudinary.uploader

from api.app.servicios.models.servicios_model import Servicios
from api.app.usuarios.models.roles_model import Roles, TipoRoles
from api.app.usuarios.models.usuarios_model import Usuarios
from api.app.usuarios.models.usuarios_tiene_roles_model import UsuariosTieneRoles
from api.app.preguntas.models.preguntas_model import Preguntas
from api.app.utils.responses import APIResponse
from api.app.reservas.models.estados_reserva_model import EstadosReserva, EstadoReserva
from api.app import db

class FunctionsUtils:
    @staticmethod
    def get_roles_user(id_usuario):
        """
        Obtiene la lista de roles (como strings) asociados a un usuario dado su ID.
        
        :param id_usuario: ID del usuario
        :return: Lista de roles (strings) o APIResponse de error
        """
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
        """
        Busca un usuario por su correo electrónico.
        
        :param correo: Correo electrónico a buscar
        :return: Instancia de Usuarios o None si no existe
        """
        usuario = Usuarios.query.filter_by(correo=correo).first()
        if usuario:
            return usuario
        else:
            return None

    @staticmethod
    def subir_imagen_cloudinary(imagen, id_usuario_token, modelo):
        """
        Sube una imagen a Cloudinary en una carpeta específica del usuario y modelo.
        
        :param imagen: Archivo de imagen
        :param id_usuario_token: ID del usuario autenticado
        :param modelo: Nombre del modelo (string)
        :return: URL segura de la imagen subida o APIResponse de error
        """
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
        """
        Verifica si existe un registro en la base de datos para un modelo y ID dados.
        
        :param id_registro: ID del registro
        :param modelo: Modelo de SQLAlchemy
        :return: Instancia del modelo si existe, si no lanza ValueError
        """
        registro = modelo.query.get(id_registro)
        if registro is None:
            raise ValueError(f"{modelo.__name__}")
        return registro

    @staticmethod
    def verificar_permisos(objeto, id_usuario_token):
        """
        Verifica si un usuario tiene permiso para acceder o modificar un objeto determinado.
        
        :param objeto: Instancia de un modelo (Usuarios o Servicios)
        :param id_usuario_token: ID del usuario autenticado
        :raises PermissionError: Si el usuario no tiene permisos
        """
        roles = FunctionsUtils.get_roles_user(id_usuario_token)

        if isinstance(objeto, Usuarios):
            id_nombre = Usuarios.id_usuarios.key
        elif isinstance(objeto, Servicios):
            id_nombre = Servicios.usuarios_proveedores_id.key
        else:
            raise ValueError("Tipo de objeto no soportado")

        if getattr(objeto, id_nombre) != id_usuario_token and (not roles or TipoRoles.ADMIN.value not in roles):
            raise PermissionError("No tienes permisos para realizar esta acción")

    @staticmethod
    def verificar_permisos_reserva(servicio, reserva, id_usuario_token):
        """
        Verifica permisos para una reserva de un servicio.
        
        :param servicio: Instancia de Servicios
        :param reserva: Instancia de Reserva
        :param id_usuario_token: ID del usuario autenticado
        :raises PermissionError: Si no tiene permisos
        """
        FunctionsUtils.verificar_permisos(servicio, id_usuario_token)
        if reserva.servicios_id != servicio.id_servicios:
            raise PermissionError("La reserva no pertenece a este servicio")
    
    @staticmethod
    def verificar_permisos_respuesta(servicio, pregunta, id_usuario_token):
        """
        Verifica permisos para una respuesta de una pregunta de un servicio.
        
        :param servicio: Instancia de Servicios
        :param pregunta: Instancia de Pregunta
        :param id_usuario_token: ID del usuario autenticado
        :raises PermissionError: Si no tiene permisos
        """
        FunctionsUtils.verificar_permisos(servicio, id_usuario_token)
        if pregunta.servicios_id != servicio.id_servicios:
            raise PermissionError("La pregunta no pertenece a este servicio")
    
    @staticmethod
    def reserva_pertece_servicio(servicio, reserva):
        """
        Verifica que la reserva pertenezca al servicio.
        
        :param servicio: Instancia de Servicios
        :param reserva: Instancia de Reserva
        :raises PermissionError: Si la reserva no pertenece al servicio
        """
        if reserva.servicios_id != servicio.id_servicios:
            raise PermissionError("La reserva no pertenece a este servicio")

    @staticmethod
    def verificar_permisos_pago(servicio, reserva, pago, id_usuario_token):
        """
        Verifica permisos para un pago de una reserva de un servicio.
        
        :param servicio: Instancia de Servicios
        :param reserva: Instancia de Reserva
        :param pago: Instancia de Pago
        :param id_usuario_token: ID del usuario autenticado
        :raises PermissionError: Si no tiene permisos
        """
        FunctionsUtils.verificar_permisos_reserva(servicio, reserva, id_usuario_token)
        if pago.reservas_id != reserva.id_reservas:
            raise PermissionError("El pago no pertenece a esta reserva")
    
    @staticmethod
    def pregunta_pertenece_servicio(servicio, pregunta):
        """
        Verifica si la pregunta pertenece al servicio.
        
        :param servicio: Instancia de Servicios
        :param pregunta: Instancia de Pregunta
        :raises PermissionError: Si la pregunta no pertenece al servicio
        """
        if pregunta.servicios_id != servicio.id_servicios:
            raise PermissionError("La pregunta no pertenece a este servicio")    

    @staticmethod
    def verificar_permisos_eliminar_pregunta(servicio, pregunta, id_usuario_token):
        """
        Verifica permisos para eliminar una pregunta.
        Solo el proveedor del servicio o el autor de la pregunta pueden eliminarla.
        
        :param servicio: Instancia de Servicios
        :param pregunta: Instancia de Pregunta
        :param id_usuario_token: ID del usuario autenticado
        :raises PermissionError: Si no tiene permisos
        """
        es_proveedor = servicio.usuarios_proveedores_id == id_usuario_token
        es_autor_pregunta = pregunta.usuarios_pregunta_id == id_usuario_token
        if not (es_proveedor or es_autor_pregunta):
            raise PermissionError("No tienes permisos para eliminar esta pregunta")
    
    @staticmethod
    def verificar_usuario_pregunta(servicio, id_usuario_token):
        """
        Si el usuario es dueño del servicio no puede preguntar, a menos que sea admin.
        
        :param servicio: Instancia de Servicios
        :param id_usuario_token: ID del usuario autenticado
        :raises PermissionError: Si el usuario es dueño y no es admin
        """
        roles = FunctionsUtils.get_roles_user(id_usuario_token)
        if servicio.usuarios_proveedores_id == id_usuario_token and (not roles or TipoRoles.ADMIN.value not in roles):
            raise PermissionError("Los dueños del servicio no pueden preguntar")

    @staticmethod
    def obtener_ids_de_enums(modelo, campo_enum, valores_enum, id_campo):
        """
        Convierte una lista de valores de un Enum en sus respectivos IDs en la base de datos.
        
        :param modelo: Modelo de SQLAlchemy (ej. Roles)
        :param campo_enum: Campo del modelo que contiene el Enum
        :param valores_enum: Lista de valores del Enum
        :param id_campo: Nombre del campo de ID en la base de datos
        :return: Lista de IDs correspondientes
        """
        if isinstance(valores_enum, str):
            valores_enum = [valores_enum]
        registros = modelo.query.filter(campo_enum.in_(valores_enum)).all()
        return [getattr(registro, id_campo) for registro in registros]

    @staticmethod
    def renombrar_campo(data, campo_original, nuevo_nombre):
        """
        Renombra un campo en un diccionario de datos.
        
        :param data: Diccionario de datos
        :param campo_original: Nombre actual del campo
        :param nuevo_nombre: Nuevo nombre para el campo
        :return: Diccionario actualizado
        """
        if campo_original in data:
            data[nuevo_nombre] = data.pop(campo_original)
        return data

    @staticmethod
    def pasar_ids(data, campo, ids):
        """
        Asigna uno o varios IDs a un campo de un diccionario de datos, adaptando el formato según el tipo de campo.

        - Si el campo es 'tipo_roles', asigna la lista completa de IDs (permite múltiples roles).
        - Para otros campos, asigna solo el primer ID de la lista (caso típico de relaciones uno a uno).

        Parámetros:
        - data (dict): Diccionario de datos a modificar.
        - campo (str): Nombre del campo a actualizar.
        - ids (list): Lista de IDs a asignar.

        Retorna:
        - dict: El diccionario de datos actualizado con el campo modificado.

        Ejemplo:
        >>> data = {'tipo_roles': None}
        >>> FunctionsUtils.pasar_ids(data, 'tipo_roles', [1,2,3])
        {'tipo_roles': [1, 2, 3]}
        >>> data = {'tipos_usuario': None}
        >>> FunctionsUtils.pasar_ids(data, 'tipos_usuario', [5])
        {'tipos_usuario': 5}
        """
        if campo in data:
            if campo == 'tipo_roles':
                data[campo] = ids
            else:
                data[campo] = ids[0]
        return data

    @staticmethod
    def verificar_reserva_ya_reservada(reserva):
        """
        Verifica si una reserva ya está en estado RESERVADA.
        
        :param reserva: Instancia de Reserva
        :raises PermissionError: Si la reserva ya está reservada
        """
        estado_actual = EstadosReserva.query.get(reserva.estados_reserva_id)
        if estado_actual and estado_actual.estado.value == EstadoReserva.RESERVADA.value:
            raise PermissionError("Esta reserva ya está reservada.")

    @staticmethod
    def verificar_pago_monto_exactitud(servicio, monto):
        """
        Verifica que el monto de pago sea exactamente igual al precio del servicio.
        
        :param servicio: Instancia de Servicios
        :param monto: Monto a verificar
        :raises ValueError: Si el monto no es exacto
        """
        if monto != servicio.precio:
            raise ValueError("El pago del servicio tiene que ser exacto.")

    @staticmethod
    def poner_reserva_en_estado_reservada(reserva):
        """
        Cambia el estado de una reserva a RESERVADA.
        
        :param reserva: Instancia de Reserva
        :raises ValueError: Si no se encuentra el estado RESERVADA
        """
        estado_reservada = EstadosReserva.query.filter_by(estado=EstadoReserva.RESERVADA.value).first()
        if not estado_reservada:
            raise ValueError("No se encontró el estado RESERVADA.")
        reserva.estados_reserva_id = estado_reservada.id_estados_reserva

    @staticmethod
    def verificar_usuario_no_es_proveedor(servicio, usuario):
        """
        Lanza PermissionError si el usuario es el proveedor del servicio.
        
        :param servicio: Instancia de Servicios
        :param usuario: Instancia de Usuarios
        :raises PermissionError: Si el usuario es el proveedor
        """
        if servicio.usuarios_proveedores_id == usuario.id_usuarios:
            raise PermissionError("El proveedor del servicio no puede efectuar el pago de su propio servicio.")

    @staticmethod
    def verificar_permisos_eliminar_pago(pago, id_usuario_token):
        """
        Permite eliminar solo si el usuario es dueño del pago o es admin.
        
        :param pago: Instancia de Pago
        :param id_usuario_token: ID del usuario autenticado
        :raises PermissionError: Si no tiene permisos
        """
        roles = FunctionsUtils.get_roles_user(id_usuario_token)
        es_duenio = pago.usuarios_id == id_usuario_token
        es_admin = roles and TipoRoles.ADMIN.value in roles
        if not (es_duenio or es_admin):
            raise PermissionError("No tienes permisos para eliminar este pago")

    @staticmethod
    def verificar_pago_pertenece_reserva_servicio(servicio, reserva, pago):
        """
        Verifica que la reserva pertenezca al servicio y el pago a la reserva.
        
        :param servicio: Instancia de Servicios
        :param reserva: Instancia de Reserva
        :param pago: Instancia de Pago
        :raises PermissionError: Si no se cumple la relación
        """
        if reserva.servicios_id != servicio.id_servicios:
            raise PermissionError("La reserva no pertenece a este servicio")
        if pago.reservas_id != reserva.id_reservas:
            raise PermissionError("El pago no pertenece a esta reserva")

    @staticmethod
    def poner_reserva_en_estado_disponible(reserva):
        """
        Cambia el estado de una reserva a DISPONIBLE.
        
        :param reserva: Instancia de Reserva
        :raises ValueError: Si no se encuentra el estado DISPONIBLE
        """
        estado_disponible = EstadosReserva.query.filter_by(estado=EstadoReserva.DISPONIBLE.value).first()
        if not estado_disponible:
            raise ValueError("No se encontró el estado DISPONIBLE.")
        reserva.estados_reserva_id = estado_disponible.id_estados_reserva
