from flask import jsonify

from api.app import db
from api.app.models.users.roles import Roles
from api.app.models.users.users import Users
from api.app.models.users.users_has_roles import UsersHasRoles
from api.app.models.users.users_type import UserTypes


class UsersController:

    def __init__(self):
        pass

    def create_user(self, data):
        try:
            # Verify if email or phone had been registered
            existing_user_by_email = Users.query.filter_by(email=data['email']).first()
            existing_user_by_phone = Users.query.filter_by(phone=data['phone']).first()

            if existing_user_by_email or existing_user_by_phone:
                return jsonify({'message': 'The email or phone already registered'}), 400

            # Get user type
            user_type = UserTypes.query.filter_by(type=data['user_types_id']).first()
            print(user_type.id_user_types)
            if not user_type:
                return jsonify({'message': 'Invalid User type'}), 400

            new_user = Users(
                name=data['name'],
                password=data['password'],
                email=data['email'],
                phone=data['phone'],
                user_types_id=user_type.id_user_types
            )
            db.session.add(new_user)

            # Get role's user
            roles = data.get('roles_id', [])

            if not isinstance(roles, list):
                roles = [roles]

            for role in roles:
                role = Roles.query.filter_by(type=role).first()
                print(role)

                if not role:
                    return jsonify({'message': f'Invalid Role:'}), 400

                # Asignar rol al usuario
                user_role = UsersHasRoles(users_id=new_user.id_users, roles_id=role.id_roles)
                db.session.add(user_role)

            db.session.commit()

            return jsonify({
                'status': 'success',
                'message': 'User create successfully'
                # 'user': new_user.to_dict(),
                # 'user_type': user_type.to_dict(),
                # 'role': role.to_dict()
            }), 201


        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400

        finally:
            db.session.close()

    @staticmethod
    def get_user_by_email(email):
        try:

            user = Users.query.filter_by(email=email).first()

            if user:
                return user
            else:
                return None

        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400

    @staticmethod
    def get_user_info(current_user):
        try:
            user = Users.query.filter_by(email=current_user['email']).first()
            return jsonify({
                'username': user.name
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400