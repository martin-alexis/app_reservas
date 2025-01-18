from flask import Blueprint, render_template, redirect, url_for, request

from api.app.models.users.roles import RolesType
from api.app.models.users.users_type import UserType

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():

    return render_template('base.html')


@main_bp.route('/signup')
def signup():
    # Filtrar para excluir ADMIN
    visible_roles = [role for role in RolesType if role != RolesType.ADMIN]
    return render_template('signup.html', roles_types=visible_roles, user_types=UserType)



@main_bp.route('/dashboard/')
def dashboard():

    return render_template('dashboard.html')




