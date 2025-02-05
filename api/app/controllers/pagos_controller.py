from datetime import datetime

from flask import jsonify, request

from api.app import db
from api.app.controllers.usuarios_controller import ControladorUsuarios
from api.app.models.pagos.estados_pago_model import EstadosPago, TiposEstadoPago
from api.app.models.pagos.pagos_model import Pagos
from api.app.models.reservas.estados_reserva_model import EstadosReserva, EstadoReserva
from api.app.models.reservas.reservas_model import Reservas
from api.app.models.services.disponibilidad_servicios_model import DisponibilidadServicio
from api.app.models.services.servicios_model import Servicios
from api.app.models.services.tipos_servicios_model import TiposServicio
from api.app.models.users.usuarios_model import Usuarios


class ControladorPagos:

    def __init__(self):
        pass


    def efectuar_pago(self, id_servicio, id_reserva):
        try:
            servicio = Servicios.query.get(id_servicio)

            if not servicio:
                return jsonify({"error": "Servicio no encontrado"}), 404

            reserva = Reservas.query.get(id_reserva)

            if not reserva:
                return jsonify({"error": "Reserva no encontrada"}), 404

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

    def obtener_pagos(self, email):
        usuario = ControladorUsuarios.obtener_usuario_por_correo(email)
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404



        reservas = Reservas.query.filter_by(servicios_id=id_servicio).all()

        if reservas:
            return jsonify([reserva.to_json() for reserva in reservas]), 200
        else:
            return jsonify({'message': 'No hay reservas registradas para este servicio.'}), 200

    def actualizar_reservas_por_servicio(self, id_servicio, id_reserva, email):
        try:
            usuario = ControladorUsuarios.obtener_usuario_por_correo(email)

            servicio = Servicios.query.get(id_servicio)

            usuario_es_valido = Servicios.query.filter_by(usuarios_proveedores_id=usuario.id_usuarios).first()
            if not usuario_es_valido:
                return jsonify({"error": "El usuario no ha creado este servicio"}), 403

            if not servicio:
                return jsonify({"error": "Servicio no encontrado"}), 404

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

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Error al actualizar el registro: {str(e)}"}), 500

        finally:
            db.session.close()

        return jsonify({"message": "Reserva actualizado exitosamente"}), 200


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