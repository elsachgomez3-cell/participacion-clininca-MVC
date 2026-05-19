from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash
)

from flask_login import login_required

from models import db

from models.medico import Medico


medico_bp = Blueprint(
    'medico_bp',
    __name__
)


# LISTAR

@medico_bp.route('/medicos')
@login_required
def listar_medicos():

    buscar = request.args.get('buscar')

    if buscar:

        medicos = Medico.query.filter(
            Medico.nombre.like(f'%{buscar}%')
        ).all()

    else:

        medicos = Medico.query.all()

    return render_template(
        'medicos/listar.html',
        medicos=medicos
    )


# CREAR

@medico_bp.route('/medicos/crear', methods=['GET', 'POST'])
@login_required
def crear_medico():

    if request.method == 'POST':

        medico = Medico(

            nombre=request.form['nombre'],

            especialidad=request.form['especialidad'],

            telefono=request.form['telefono'],

            correo=request.form['correo'],

            horario=request.form['horario']

        )

        db.session.add(medico)

        db.session.commit()

        flash(
            'Médico registrado correctamente',
            'success'
        )

        return redirect('/medicos')

    return render_template(
        'medicos/crear.html'
    )


# EDITAR

@medico_bp.route('/medicos/editar/<int:id>')
@login_required
def editar_medico(id):

    medico = Medico.query.get_or_404(id)

    return render_template(
        'medicos/editar.html',
        medico=medico
    )


# UPDATE

@medico_bp.route(
    '/medicos/update/<int:id>',
    methods=['POST']
)
@login_required
def update_medico(id):

    medico = Medico.query.get_or_404(id)

    medico.nombre = request.form['nombre']

    medico.especialidad = request.form[
        'especialidad'
    ]

    medico.telefono = request.form['telefono']

    medico.correo = request.form['correo']

    medico.horario = request.form['horario']

    db.session.commit()

    flash(
        'Médico actualizado correctamente',
        'warning'
    )

    return redirect('/medicos')


# DELETE

@medico_bp.route('/medicos/delete/<int:id>')
@login_required
def delete_medico(id):

    medico = Medico.query.get_or_404(id)

    db.session.delete(medico)

    db.session.commit()

    flash(
        'Médico eliminado correctamente',
        'danger'
    )

    return redirect('/medicos')