from flask import jsonify, request

from api.app import db
from api.app.models.pagos.estados_pago_model import EstadosPago, TiposEstadoPago
from api.app.models.pagos.pagos_model import Pagos
from api.app.models.reservas.estados_reserva_model import EstadosReserva, EstadoReserva
from api.app.models.reservas.reservas_model import Reservas
from api.app.models.services.servicios_model import Servicios
from api.app.models.users.roles_model import TipoRoles
from api.app.models.users.usuarios_model import Usuarios


class ControladorPagos:

    def __init__(self):
        pass


    def efectuar_pago(self, id_servicio, id_reserva, id_usuario_token, roles):
        try:
            usuario = Usuarios.query.get(id_usuario_token)
            if not usuario:
                return jsonify({"error": "Usuario no encontrado"}), 404

            servicio = Servicios.query.get(id_servicio)

            if not servicio:
                return jsonify({"error": "Servicio no encontrado"}), 404

            reserva = Reservas.query.get(id_reserva)

            if not reserva:
                return jsonify({"error": "Reserva no encontrada"}), 404


            if TipoRoles.ADMIN.value in roles:
                pass
            else:
                if usuario.id_usuarios != servicio.usuarios_proveedores_id:
                    return jsonify({"error": "Este servicio no pertenece al usuario"}), 403

                if reserva.servicios_id != servicio.id_servicios:
                    return jsonify({"error": "Esta reserva no pertenece al servicio indicado."}), 403

            reserva_esta_disponible = EstadosReserva.query.get(reserva.estados_reserva_id)

            if reserva_esta_disponible and reserva_esta_disponible.estado.value == EstadoReserva.RESERVADA.value:
                return jsonify({"error": "Esta reserva ya está reservada."}), 403

            data = request.json

            if data['monto'] != reserva.monto_total:
                return jsonify({"error": "El pago de la reserva tiene que estar exacto."}), 400

            tipo_pago = EstadosPago.query.filter_by(estado=TiposEstadoPago.CONFIRMADO.value).first()


            nuevo_pago = Pagos(
                monto=data['monto'],
                reservas_id=reserva.id_reservas,
                estados_pago_id=tipo_pago.id_estados_pago,
                usuarios_id=usuario.id_usuarios,
            )

            db.session.add(nuevo_pago)
            estado_reservada = EstadosReserva.query.filter_by(estado=EstadoReserva.RESERVADA.value).first()

            reserva.estados_reserva_id = estado_reservada.id_estados_reserva
            db.session.commit()

            return jsonify({
                'status': 'success',
                'message': 'Pago creado exitosamente'
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400

        finally:
            db.session.close()

    def obtener_pagos_del_usuario(self, id_usuario, id_usuario_token, roles):
        try:
            usuario = Usuarios.query.get(id_usuario)
            if not usuario:
                return jsonify({"error": "Usuario no encontrado"}), 404

            if usuario.id_usuarios != id_usuario_token and (not roles or TipoRoles.ADMIN.value not in roles):
                return jsonify({"error": "No tienes permiso para obtener los pagos."}), 403

            pagos = Pagos.query.filter_by(usuarios_id=usuario.id_usuarios).all()

            if not pagos:
                return jsonify({'message': 'No se encontraron pagos.'}), 200

            return jsonify([pago.to_json() for pago in pagos]), 200

        except Exception as e:
            return jsonify({"error": f"Error: {str(e)}"}), 500