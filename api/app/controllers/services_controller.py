from flask import jsonify, request

from api.app import db
from api.app.models.services.services_availability_model import ServiceAvailability
from api.app.models.services.services_model import Services
from api.app.models.services.services_type_model import ServiceTypes
from api.app.models.users.users import Users


class ServicesController:

    def __init__(self):
        pass

    @staticmethod
    def create_service(data, email):
        try:
            user_provider = Users.query.filter_by(email=email).first()

            service_type = ServiceTypes.query.filter_by(type=data['service_types_id']).first()
            print(service_type)
            service_availability = ServiceAvailability.query.filter_by(status=data['service_availability_id']).first()

            if not service_availability:
                return jsonify({'message': 'Invalid status service'}), 400

            new_service = Services(
                name=data['name'],
                description=data['description'],
                price=data['price'],
                location=data['location'],
                service_availability_id= service_availability.id_service_availability,
                service_types_id=service_type.id_service_types,
                users_providers_id=user_provider.id_users
            )
            db.session.add(new_service)
            db.session.commit()

            return jsonify({
                'status': 'success',
                'message': 'Service create successfully'
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400

        finally:
            db.session.close()

    def get_services(self):
        try:
            services = Services.query.all()

            if services:
                return jsonify([service.to_dict() for service in services]), 200
            else:
                return jsonify({'message': 'No hay productos regitrados.'}), 200

        except Exception as e:
            return jsonify({'error': 'Ocurrió un error al obtener los productos.', 'message': str(e)}), 500

    @staticmethod
    def update_services(id_service):
        try:
            service = Services.query.get(id_service)

            if not service:
                return jsonify({"error": "Servicio no encontrado"}), 404

            data = request.json

            service_type = ServiceTypes.query.filter_by(type=data['service_types_id']).first()

            service_availability = ServiceAvailability.query.filter_by(status=data['service_availability_id']).first()

            if not service_availability:
                return jsonify({'message': 'Invalid status service'}), 400

            if 'name' in data:
                service.name = data['name']
            if 'description' in data:
                service.description = data['description']
            if 'price' in data:
                service.price = data['price']
            if 'location' in data:
                service.location = data['location']
            if 'service_availability_id' in data:
                service.service_availability_id = service_availability.id_service_availability
            if 'service_types_id' in data:
                service.available = service_type.id_service_types

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar el registro: {e}")
            return jsonify({"error": "Error al actualizar el registro"}), 500

        finally:
            db.session.close()

        return jsonify({"message": "Servicio actualizado exitosamente"}), 200
