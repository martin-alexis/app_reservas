from flask import jsonify, request

from api.app import db
from api.app.models.services.disponibilidad_servicios_model import DisponibilidadServicio
from api.app.models.services.servicios_model import Servicios
from api.app.models.services.tipos_servicios_model import TiposServicio
from api.app.models.users.usuarios_model import Usuarios


class ControladorServicios:

    def __init__(self):
        pass

    @staticmethod
    def crear_servicio(data, correo):
        try:
            usuario_proveedor = Usuarios.query.filter_by(correo=correo).first()

            tipo_servicio = TiposServicio.query.filter_by(tipo=data['tipos_servicio_id']).first()
            print(tipo_servicio)
            disponibilidad_servicio = DisponibilidadServicio.query.filter_by(status=data['disponibilidad_servicio_id']).first()

            if not disponibilidad_servicio:
                return jsonify({'message': 'Estado del servicio inválido'}), 400

            nuevo_servicio = Servicios(
                nombre=data['nombre'],
                descripcion=data['descripcion'],
                precio=data['precio'],
                ubicacion=data['ubicacion'],
                disponibilidad_servicio_id=disponibilidad_servicio.id_disponibilidad_servicio,
                tipos_servicio_id=tipo_servicio.id_tipos_servicio,
                usuarios_proveedores_id=usuario_proveedor.id_usuarios
            )
            db.session.add(nuevo_servicio)
            db.session.commit()

            return jsonify({
                'status': 'success',
                'message': 'Servicio creado exitosamente'
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400

        finally:
            db.session.close()

    def obtener_servicios(self):
        try:
            servicios = Servicios.query.all()

            if servicios:
                return jsonify([servicio.to_dict() for servicio in servicios]), 200
            else:
                return jsonify({'message': 'No hay productos registrados.'}), 200

        except Exception as e:
            return jsonify({'error': 'Ocurrió un error al obtener los productos.', 'message': str(e)}), 500

    @staticmethod
    def actualizar_servicio(id_servicio):
        try:
            servicio = Servicios.query.get(id_servicio)

            if not servicio:
                return jsonify({"error": "Servicio no encontrado"}), 404

            data = request.json

            tipo_servicio = TiposServicio.query.filter_by(type=data['tipos_servicio_id']).first()

            disponibilidad_servicio = DisponibilidadServicio.query.filter_by(status=data['disponibilidad_servicio_id']).first()

            if not disponibilidad_servicio:
                return jsonify({'message': 'Estado del servicio inválido'}), 400

            if 'nombre' in data:
                servicio.nombre = data['nombre']
            if 'descripcion' in data:
                servicio.descripcion = data['descripcion']
            if 'precio' in data:
                servicio.precio = data['precio']
            if 'ubicacion' in data:
                servicio.ubicacion = data['ubicacion']
            if 'disponibilidad_servicio_id' in data:
                servicio.disponibilidad_servicio_id = disponibilidad_servicio.id_disponibilidad_servicio
            if 'tipos_servicio_id' in data:
                servicio.tipos_servicio_id = tipo_servicio.id_service_types

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar el registro: {e}")
            return jsonify({"error": "Error al actualizar el registro"}), 500

        finally:
            db.session.close()

        return jsonify({"message": "Servicio actualizado exitosamente"}), 200
