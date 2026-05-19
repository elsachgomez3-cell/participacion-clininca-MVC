from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required
)

from models import db

from models.usuario import Usuario


auth_bp = Blueprint(
    'auth_bp',
    __name__
)


# LOGIN

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        usuario = Usuario.query.filter_by(
            username=username
        ).first()

        if usuario and usuario.check_password(password):

            login_user(usuario)

            flash(
                'Bienvenido al sistema',
                'success'
            )

            return redirect('/')

        else:

            flash(
                'Usuario o contraseña incorrectos',
                'danger'
            )

    return render_template('login.html')


# REGISTER

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        existe = Usuario.query.filter_by(
            username=username
        ).first()

        if existe:

            flash(
                'El usuario ya existe',
                'warning'
            )

            return redirect('/register')

        nuevo_usuario = Usuario(
            username=username
        )

        nuevo_usuario.set_password(password)

        db.session.add(nuevo_usuario)

        db.session.commit()

        flash(
            'Usuario registrado correctamente',
            'success'
        )

        return redirect('/login')

    return render_template('register.html')


# LOGOUT

@auth_bp.route('/logout')
@login_required
def logout():

    logout_user()

    flash(
        'Sesión cerrada',
        'info'
    )

    return redirect('/login')