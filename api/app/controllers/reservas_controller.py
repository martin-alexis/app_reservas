from datetime import datetime

from flask import jsonify, request

from api.app import db
from api.app.models.reservas.estados_reserva_model import EstadosReserva
from api.app.models.reservas.reservas_model import Reservas
from api.app.models.services.disponibilidad_servicios_model import DisponibilidadServicio
from api.app.models.services.servicios_model import Servicios
from api.app.models.services.tipos_servicios_model import TiposServicio
from api.app.models.users.usuarios_model import Usuarios


class ControladorReservas:

    def __init__(self):
        pass


    def crear_reservas(self, id_servicio):
        try:
            servicio = Servicios.query.get(id_servicio)

            if not servicio:
                return jsonify({"error": "Servicio no encontrado"}), 404

            data = request.json

            estado_reserva = EstadosReserva.query.filter_by(estado=data['estados_reserva_id']).first()

            if not estado_reserva:
                return jsonify({"error": "Estado de la reserva no es valido."}), 400


            nueva_reserva = Reservas(
                fecha_inicio_reserva=datetime.strptime(data['fecha_inicio_reserva'], "%d/%m/%Y %H:%M:%S"),
                fecha_fin_reserva=datetime.strptime(data['fecha_fin_reserva'], "%d/%m/%Y %H:%M:%S"),
                monto_total=data['monto_total'],
                servicios_id=id_servicio,
                estados_reserva_id=estado_reserva.id_estados_reserva
            )

            db.session.add(nueva_reserva)
            db.session.commit()

            return jsonify({
                'status': 'success',
                'message': 'Reserva creada exitosamente'
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400

        finally:
            db.session.close()

    # def obtener_servicios_usuario(self, email):
    #     try:
    #         usuario = Usuarios.query.filter_by(correo=email).first()
    #         servicios = Servicios.query.filter_by(usuarios_proveedores_id=usuario.id_usuarios).all()
    #
    #         if servicios:
    #             return jsonify([servicio.to_json() for servicio in servicios]), 200
    #         else:
    #             return jsonify({'message': 'No hay servicios registrados.'}), 200
    #
    #     except Exception as e:
    #         return jsonify({'error': 'Ocurrió un error al obtener los servicios.', 'message': str(e)}), 500
    #
    # @staticmethod
    # def actualizar_servicio(id_servicio):
    #     try:
    #         servicio = Servicios.query.get(id_servicio)
    #
    #         if not servicio:
    #             return jsonify({"error": "Servicio no encontrado"}), 404
    #
    #         data = request.json
    #
    #         tipo_servicio = TiposServicio.query.filter_by(tipo=data['tipos_servicio_id']).first()
    #
    #         disponibilidad_servicio = DisponibilidadServicio.query.filter_by(estado=data['disponibilidad_servicio_id']).first()
    #
    #         if not disponibilidad_servicio:
    #             return jsonify({'message': 'Estado del servicio inválido'}), 400
    #
    #         if 'nombre' in data:
    #             servicio.nombre = data['nombre']
    #         if 'descripcion' in data:
    #             servicio.descripcion = data['descripcion']
    #         if 'precio' in data:
    #             servicio.precio = data['precio']
    #         if 'ubicacion' in data:
    #             servicio.ubicacion = data['ubicacion']
    #         if 'disponibilidad_servicio_id' in data:
    #             servicio.disponibilidad_servicio_id = disponibilidad_servicio.id_disponibilidad_servicio
    #         if 'tipos_servicio_id' in data:
    #             servicio.tipos_servicio_id = tipo_servicio.id_tipos_servicio
    #
    #         db.session.commit()
    #
    #     except Exception as e:
    #         db.session.rollback()
    #         print(f"Error al actualizar el registro: {e}")
    #         return jsonify({"error": "Error al actualizar el registro"}), 500
    #
    #     finally:
    #         db.session.close()
    #
    #     return jsonify({"message": "Servicio actualizado exitosamente"}), 200
    #
    #
    # def eliminar_servicios_usuario(self, id_servicios, email):
    #     try:
    #         # usuario = Usuarios.query.filter_by(correo=email).first()
    #         servicio = Servicios.query.get(id_servicios)
    #
    #         if servicio:
    #             db.session.delete(servicio)
    #             db.session.commit()
    #             return jsonify({'message': 'Servicio eliminado correctamente.'}), 200
    #         else:
    #             return jsonify({'message': 'No se encontró el servicio.'}), 404
    #
    #     except Exception as e:
    #         return jsonify({'error': 'Ocurrió un error al eliminar el servicio.', 'message': str(e)}), 500