from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash
)

from flask_login import (
    login_required
)

from models import db

from models.cita import Cita
from models.medico import Medico
from models.paciente import Paciente

cita_bp = Blueprint(
    'cita_bp',
    __name__
)

# =========================
# LISTAR
# =========================

@cita_bp.route('/citas')
@login_required
def listar_citas():

    citas = Cita.query.all()

    return render_template(

        'citas/listar.html',

        citas=citas

    )

# =========================
# CREAR
# =========================

@cita_bp.route(
    '/citas/crear',
    methods=['GET', 'POST']
)
@login_required
def crear_cita():

    pacientes = Paciente.query.all()

    medicos = Medico.query.all()

    if request.method == 'POST':

        nueva_cita = Cita(

            fecha=request.form['fecha'],

            hora=request.form['hora'],

            motivo=request.form['motivo'],

            estado=request.form['estado'],

            id_paciente=request.form['id_paciente'],

            id_medico=request.form['id_medico']

        )

        db.session.add(nueva_cita)

        db.session.commit()

        flash(
            'Cita registrada correctamente',
            'success'
        )

        return redirect('/citas')

    return render_template(

        'citas/crear.html',

        pacientes=pacientes,

        medicos=medicos

    )

# =========================
# EDITAR
# =========================

@cita_bp.route('/citas/editar/<int:id>')
@login_required
def editar_cita(id):

    cita = Cita.query.get_or_404(id)

    pacientes = Paciente.query.all()

    medicos = Medico.query.all()

    return render_template(

        'citas/editar.html',

        cita=cita,

        pacientes=pacientes,

        medicos=medicos

    )

# =========================
# UPDATE
# =========================

@cita_bp.route(
    '/citas/update/<int:id>',
    methods=['POST']
)
@login_required
def update_cita(id):

    cita = Cita.query.get_or_404(id)

    cita.fecha = request.form['fecha']

    cita.hora = request.form['hora']

    cita.motivo = request.form['motivo']

    cita.estado = request.form['estado']

    cita.id_paciente = request.form['id_paciente']

    cita.id_medico = request.form['id_medico']

    db.session.commit()

    flash(
        'Cita actualizada correctamente',
        'warning'
    )

    return redirect('/citas')

# =========================
# ELIMINAR
# =========================

@cita_bp.route('/citas/delete/<int:id>')
@login_required
def delete_cita(id):

    cita = Cita.query.get_or_404(id)

    db.session.delete(cita)

    db.session.commit()

    flash(
        'Cita eliminada correctamente',
        'danger'
    )

    return redirect('/citas')