import cloudinary.uploader
from werkzeug.utils import secure_filename
from flask import jsonify, request, abort

from api.app import db
from api.app.models.services.disponibilidad_servicios_model import DisponibilidadServicio
from api.app.models.services.servicios_model import Servicios
from api.app.models.services.tipos_servicios_model import TiposServicio
from api.app.models.users.roles_model import TipoRoles
from api.app.models.users.usuarios_model import Usuarios


class ControladorServicios:

    def __init__(self):
        pass


    @staticmethod
    def subir_imagen_cloudinary(imagen, correo, modelo):
        try:

            if not imagen:
                return None

            imagen_filename = secure_filename(imagen.filename)
            carpeta_principal = f'app_reservas/{modelo}'
            carpeta_usuario = correo.replace('@', '_').replace('.', '_')
            carpeta_completa = f"{carpeta_principal}/{carpeta_usuario}"

            upload_result = cloudinary.uploader.upload(
                imagen,
                folder=carpeta_completa,
                public_id=imagen_filename
            )
            return upload_result['secure_url']

        except Exception as e:
            abort(500, description=f"Error al subir la imagen a Cloudinary: {str(e)}")

    def crear_servicio(self, data, correo):
        try:
            # Recuperar el usuario proveedor
            usuario_proveedor = Usuarios.query.filter_by(correo=correo).first()
            if not usuario_proveedor:
                return jsonify({"error": "Usuario no encontrado"}), 404

            # Recuperar el tipo de servicio
            tipo_servicio = TiposServicio.query.filter_by(tipo=data['tipos_servicio_id']).first()
            if not tipo_servicio:
                return jsonify({"error": "Tipo de servicio inválido"}), 404

            # Recuperar la disponibilidad del servicio
            disponibilidad_servicio = DisponibilidadServicio.query.filter_by(
                estado=data['disponibilidad_servicio_id']).first()
            if not disponibilidad_servicio:
                return jsonify({'message': 'Estado del servicio inválido'}), 400
            imagen = request.files['imagen']

            imagen_url = self.subir_imagen_cloudinary(imagen, correo, 'servicios')

            # Crear el nuevo servicio
            nuevo_servicio = Servicios(
                nombre=data['nombre'],
                descripcion=data['descripcion'],
                precio=data['precio'],
                ubicacion=data['ubicacion'],
                disponibilidad_servicio_id=disponibilidad_servicio.id_disponibilidad_servicio,
                tipos_servicio_id=tipo_servicio.id_tipos_servicio,
                usuarios_proveedores_id=usuario_proveedor.id_usuarios,
                imagen=imagen_url
            )

            db.session.add(nuevo_servicio)
            db.session.commit()

            return jsonify({
                'status': 'success',
                'message': 'Servicio creado exitosamente',
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400

        finally:
            db.session.close()

    def obtener_servicios_usuario(self, id_usuario):
        try:
            usuario = Usuarios.query.get(id_usuario)
            if not usuario:
                return jsonify({"error": "Usuario no encontrado"}), 404

            servicios = Servicios.query.filter_by(usuarios_proveedores_id=usuario.id_usuarios).all()

            if servicios:
                return jsonify([servicio.to_json() for servicio in servicios]), 200
            else:
                return jsonify({'message': 'No hay servicios registrados.'}), 200

        except Exception as e:
            return jsonify({'error': 'Ocurrió un error al obtener los servicios.', 'message': str(e)}), 500


    def obtener_todos_servicios(self, email):
        try:
            usuario = Usuarios.query.filter_by(correo=email).first()
            if not usuario:
                return jsonify({"error": "Usuario no encontrado"}), 404

            # Obtener los filtros desde la URL
            tipos_servicios = request.args.get('categoria')
            disponibilidad = request.args.get('disponibilidad')
            precio_min = request.args.get('precio_min')
            precio_max = request.args.get('precio_max')

            query = Servicios.query

            if tipos_servicios:
                tipos_validos = ControladorServicios.validar_tipos_servicios("Tipos de servicios", tipos_servicios,
                                                                             "tipo", TiposServicio)
                if "error" in tipos_validos:
                    return jsonify(tipos_validos), 400

                query = query.join(TiposServicio).filter(TiposServicio.tipo.in_(tipos_validos))

            if disponibilidad:
                estados_validos = ControladorServicios.validar_tipos_servicios("Disponibilidad", disponibilidad,
                                                                               "estado", DisponibilidadServicio)
                if "error" in estados_validos:
                    return jsonify(estados_validos), 400

                query = query.join(DisponibilidadServicio).filter(DisponibilidadServicio.estado.in_(estados_validos))

            resultado = ControladorServicios.verificar_filtros_precio(precio_min, precio_max)

            # Si se ha retornado un diccionario de error, respondemos con el error
            if isinstance(resultado, dict) and "error" in resultado:
                return jsonify(resultado), 400

            query = ControladorServicios.aplicar_filtros_precio(query, precio_min, precio_max)

            query = ControladorServicios.aplicar_filtros_precio(query, precio_min, precio_max)

            servicios = query.all()

            if not servicios:
                return jsonify({'message': 'No se encontraron servicios.'}), 200

            return jsonify([servicio.to_json() for servicio in servicios]), 200


        except Exception as e:
            return jsonify({'error': 'Ocurrió un error al obtener los servicios.', 'message': str(e)}), 500


    def actualizar_servicio(self, id_servicio, correo, roles):
        try:
            servicio = Servicios.query.get(id_servicio)

            usuario = Usuarios.query.filter_by(correo=correo).first()

            if not usuario:
                return jsonify({"error": "Usuario no encontrado"}), 404

            if not servicio:
                return jsonify({"error": "Servicio no encontrado"}), 404

            if usuario.id_usuarios != servicio.usuarios_proveedores_id and (not roles or TipoRoles.ADMIN.value not in roles):
                return jsonify({"error": "No tienes permiso para actualizar los datos"}), 403

            data = request.json


            if 'disponibilidad_servicio_id' in data:
                disponibilidad_servicio = DisponibilidadServicio.query.filter_by(
                    estado=data['disponibilidad_servicio_id']).first()

                if not disponibilidad_servicio:
                    return jsonify({'message': 'Estado del servicio inválido'}), 400

                servicio.disponibilidad_servicio_id = disponibilidad_servicio.id_disponibilidad_servicio

            if 'tipos_servicio_id' in data:
                tipo_servicio = TiposServicio.query.filter_by(tipo=data['tipos_servicio_id']).first()
                if not tipo_servicio:
                    return jsonify({'message': 'Tipo del servicio inválido'}), 400

                servicio.tipos_servicio_id = tipo_servicio.id_tipos_servicio
            if 'nombre' in data:
                servicio.nombre = data['nombre']
            if 'descripcion' in data:
                servicio.descripcion = data['descripcion']
            if 'precio' in data:
                servicio.precio = data['precio']
            if 'ubicacion' in data:
                servicio.ubicacion = data['ubicacion']


            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar el registro: {e}")
            return jsonify({"error": "Error al actualizar el registro"}), 500

        finally:
            db.session.close()

        return jsonify({"message": "Servicio actualizado exitosamente"}), 200

    def eliminar_servicios_usuario(self, id_usuario, id_servicio, correo, roles):
        try:
            servicio = Servicios.query.get(id_servicio)
            usuario = Usuarios.query.get(id_usuario)
            mismo_usuario = Usuarios.query.filter_by(correo=correo).first()

            if not usuario:
                return jsonify({"error": "Usuario no encontrado"}), 404
            if not servicio:
                return jsonify({"error": "Servicio no encontrado"}), 404

            if TipoRoles.ADMIN.value in roles:
                # El ADMIN puede eliminar cualquier servicio, no es necesario verificar si es propietario
                pass
            else:
                # El usuario no es ADMIN, entonces verificamos que el usuario sea el dueño del servicio
                if usuario.id_usuarios != servicio.usuarios_proveedores_id:
                    return jsonify({"error": "Este servicio no pertenece al usuario"}), 403

                # Verificar que el usuario en el token sea el mismo que el id_usuario
                if usuario.id_usuarios != mismo_usuario.id_usuarios:
                    return jsonify({"error": "No tienes permiso para eliminar el servicio"}), 403

            db.session.delete(servicio)
            db.session.commit()
            return jsonify({'message': 'Servicio eliminado correctamente.'}), 200

        except Exception as e:
            print(f"Error al eliminar servicio: {e}")
            return jsonify({'error': 'Ocurrió un error al eliminar el servicio.', 'message': str(e)}), 500

    @staticmethod
    def validar_tipos_servicios(atributo, nombres_atributos, campo, modelo):
        if not nombres_atributos:
            return []

        nombres_atributos = [atributo.upper() for atributo in nombres_atributos.split(",")]
        atributos_validos = modelo.query.with_entities(getattr(modelo, campo)).filter(getattr(modelo, campo).in_(nombres_atributos)).all()

        atributos_validos = [atributo[0].value for atributo in atributos_validos]  # Extraer los valores válidos

        atributos_invalidos = set(nombres_atributos) - set(atributos_validos)  # Buscar valores que no existen
        if atributos_invalidos:
            return {"error": f"{atributo.capitalize()} no encontradas: {', '.join(atributos_invalidos)}"}

        return atributos_validos

    @staticmethod
    def verificar_filtros_precio(precio_min, precio_max):
        if precio_min:
            try:
                precio_min = float(precio_min)
            except ValueError:
                return {"error": "El precio mínimo debe ser un número válido."}

        if precio_max:
            try:
                precio_max = float(precio_max)
            except ValueError:
                return {"error": "El precio máximo debe ser un número válido."}

        return precio_min, precio_max


    @staticmethod
    def aplicar_filtros_precio(query, precio_min, precio_max):
        if precio_min and precio_max:
            query = query.filter(Servicios.precio >= float(precio_min), Servicios.precio <= float(precio_max))
        elif precio_min:
            query = query.filter(Servicios.precio >= float(precio_min))
        elif precio_max:
            query = query.filter(Servicios.precio <= float(precio_max))
        return query



