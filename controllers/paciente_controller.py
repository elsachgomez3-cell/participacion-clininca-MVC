from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash
)

from flask_login import login_required

from models import db

from models.paciente import Paciente

from models.consulta import Consulta


paciente_bp = Blueprint(
    'paciente_bp',
    __name__
)


# LISTAR

@paciente_bp.route('/pacientes')
@login_required
def listar_pacientes():

    buscar = request.args.get('buscar')

    if buscar:

        pacientes = Paciente.query.filter(
            Paciente.nombre.like(f'%{buscar}%')
        ).all()

    else:

        pacientes = Paciente.query.all()

    return render_template(
        'pacientes/listar.html',
        pacientes=pacientes
    )


# CREAR

@paciente_bp.route('/pacientes/crear', methods=['GET', 'POST'])
@login_required
def crear_paciente():

    if request.method == 'POST':

        nombre = request.form['nombre']

        edad = request.form['edad']

        direccion = request.form['direccion']

        telefono = request.form['telefono']

        genero = request.form['genero']

        fecha_registro = request.form['fecha_registro']

        # VALIDACIONES

        if not nombre or not edad:

            flash(
                'Complete los campos obligatorios',
                'danger'
            )

            return redirect('/pacientes/crear')

        paciente = Paciente(

            nombre=nombre,

            edad=edad,

            direccion=direccion,

            telefono=telefono,

            genero=genero,

            fecha_registro=fecha_registro

        )

        db.session.add(paciente)

        db.session.commit()

        flash(
            'Paciente registrado correctamente',
            'success'
        )

        return redirect('/pacientes')

    return render_template(
        'pacientes/crear.html'
    )


# EDITAR

@paciente_bp.route('/pacientes/editar/<int:id>')
@login_required
def editar_paciente(id):

    paciente = Paciente.query.get_or_404(id)

    return render_template(
        'pacientes/editar.html',
        paciente=paciente
    )


# UPDATE

@paciente_bp.route(
    '/pacientes/update/<int:id>',
    methods=['POST']
)
@login_required
def update_paciente(id):

    paciente = Paciente.query.get_or_404(id)

    paciente.nombre = request.form['nombre']

    paciente.edad = request.form['edad']

    paciente.direccion = request.form['direccion']

    paciente.telefono = request.form['telefono']

    paciente.genero = request.form['genero']

    paciente.fecha_registro = request.form[
        'fecha_registro'
    ]

    db.session.commit()

    flash(
        'Paciente actualizado correctamente',
        'warning'
    )

    return redirect('/pacientes')


# ELIMINAR

@paciente_bp.route('/pacientes/delete/<int:id>')
@login_required
def delete_paciente(id):

    paciente = Paciente.query.get_or_404(id)

    db.session.delete(paciente)

    db.session.commit()

    flash(
        'Paciente eliminado correctamente',
        'danger'
    )

    return redirect('/pacientes')


# HISTORIAL MEDICO

@paciente_bp.route('/pacientes/historial/<int:id>')
@login_required
def historial_paciente(id):

    paciente = Paciente.query.get_or_404(id)

    consultas = Consulta.query.filter_by(
        id_paciente=id
    ).all()

    return render_template(

        'pacientes/historial.html',

        paciente=paciente,

        consultas=consultas

    )