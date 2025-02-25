from datetime import datetime

from flask import jsonify, request

from api.app import db
from api.app.controllers.usuarios_controller import ControladorUsuarios
from api.app.models.reservas.estados_reserva_model import EstadosReserva
from api.app.models.reservas.reservas_model import Reservas
from api.app.models.services.servicios_model import Servicios
from api.app.models.users.roles_model import TipoRoles
from api.app.models.users.usuarios_model import Usuarios


class ControladorReservas:

    def __init__(self):
        pass


    def crear_reservas(self, id_servicio, id_usuario_token, roles):
        try:
            servicio = Servicios.query.get(id_servicio)

            usuario = Usuarios.query.get(id_usuario_token)

            if not usuario:
                return jsonify({"error": "Usuario no encontrado"}), 404

            if not servicio:
                return jsonify({"error": "Servicio no encontrado"}), 404

            if usuario.id_usuarios != servicio.usuarios_proveedores_id and (not roles or TipoRoles.ADMIN.value not in roles):
                return jsonify({"error": "No tienes permiso para crear la reserva."}), 403

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

    def obtener_reservas_por_servicio(self, id_servicio):
        try:
            servicio = Servicios.query.get(id_servicio)
            if not servicio:
                return jsonify({"error": "Servicio no encontrado"}), 404

            reservas = Reservas.query.filter_by(servicios_id=id_servicio).all()

            if reservas:
                return jsonify([reserva.to_json() for reserva in reservas]), 200
            else:
                return jsonify({'message': 'No hay reservas registradas para este servicio.'}), 200

        except Exception as e:
            return jsonify({"error": f"Error al localizar el registro: {str(e)}"}), 500

    def actualizar_reservas_por_servicio(self, id_servicio, id_reserva, id_usuario_token, roles):
        try:
            usuario = Usuarios.query.get(id_usuario_token)

            servicio = Servicios.query.get(id_servicio)

            if not usuario:
                return jsonify({"error": "Usuario no encontrado"}), 404

            if not servicio:
                return jsonify({"error": "Servicio no encontrado"}), 404

            if usuario.id_usuarios != servicio.usuarios_proveedores_id and (not roles or TipoRoles.ADMIN.value not in roles):
                return jsonify({"error": "No tienes permiso para actualizar la reserva."}), 403

            reserva = Reservas.query.get(id_reserva)

            if not reserva:
                return jsonify({"error": "Reserva no encontrada"}), 404

            data = request.json

            estado_reserva = True
            if 'fecha_inicio_reserva' in data:
                reserva.fecha_inicio_reserva = datetime.strptime(data['fecha_inicio_reserva'], "%d/%m/%Y %H:%M:%S")
            if 'fecha_fin_reserva' in data:
                reserva.fecha_fin_reserva = datetime.strptime(data['fecha_fin_reserva'], "%d/%m/%Y %H:%M:%S")
            if 'monto_total' in data:
                reserva.monto_total = data['monto_total']
            if 'estados_reserva_id' in data:
                estado_reserva = EstadosReserva.query.filter_by(estado=data['estados_reserva_id']).first()
                reserva.estados_reserva_id = estado_reserva.id_estados_reserva
            elif not estado_reserva :
                return jsonify({"error": "Estado de la reserva no es valido."}), 400


            db.session.commit()

            return jsonify({"message": "Reserva actualizado exitosamente"}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Error al actualizar el registro: {str(e)}"}), 500

        finally:
            db.session.close()



    def eliminar_reservas_por_servicio(self, id_servicio, id_reserva, email):
        try:
            usuario = ControladorUsuarios.obtener_usuario_por_correo(email)
            if not usuario:
                return jsonify({"error": "Usuario no encontrado"}), 404

            usuario_es_valido = Servicios.query.filter_by(usuarios_proveedores_id=usuario.id_usuarios).first()
            if not usuario_es_valido:
                return jsonify({"error": "El usuario no ha creado este servicio"}), 403

            servicio = Servicios.query.get(id_servicio)

            if not servicio:
                return jsonify({"error": "Servicio no encontrado"}), 404

            reserva = Reservas.query.get(id_reserva)

            if reserva:
                db.session.delete(reserva)
                db.session.commit()
                return jsonify({'message': 'Reserva eliminado correctamente.'}), 200
            else:
                return jsonify({'message': 'No se encontró la reserva.'}), 404

        except Exception as e:
            return jsonify({'error': 'Ocurrió un error al eliminar la reserva.', 'message': str(e)}), 500