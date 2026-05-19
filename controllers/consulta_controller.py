from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    make_response
)

from flask_login import login_required

from models import db

from models.consulta import Consulta
from models.paciente import Paciente
from models.medico import Medico

from reportlab.pdfgen import canvas

import io


consulta_bp = Blueprint(
    'consulta_bp',
    __name__
)


# LISTAR CONSULTAS

@consulta_bp.route('/consultas')
@login_required
def listar_consultas():

    fecha = request.args.get('fecha')

    if fecha:

        consultas = Consulta.query.filter_by(
            fecha=fecha
        ).all()

    else:

        consultas = Consulta.query.all()

    return render_template(
        'consultas/listar.html',
        consultas=consultas
    )


# CREAR CONSULTA

@consulta_bp.route(
    '/consultas/crear',
    methods=['GET', 'POST']
)
@login_required
def crear_consulta():

    pacientes = Paciente.query.all()

    medicos = Medico.query.all()

    if request.method == 'POST':

        consulta = Consulta(

            fecha=request.form['fecha'],

            diagnostico=request.form[
                'diagnostico'
            ],

            tratamiento=request.form[
                'tratamiento'
            ],

            observaciones=request.form[
                'observaciones'
            ],

            id_paciente=request.form[
                'id_paciente'
            ],

            id_medico=request.form[
                'id_medico'
            ]

        )

        db.session.add(consulta)

        db.session.commit()

        flash(
            'Consulta registrada correctamente',
            'success'
        )

        return redirect('/consultas')

    return render_template(

        'consultas/crear.html',

        pacientes=pacientes,

        medicos=medicos

    )


# EDITAR

@consulta_bp.route(
    '/consultas/editar/<int:id>'
)
@login_required
def editar_consulta(id):

    consulta = Consulta.query.get_or_404(id)

    pacientes = Paciente.query.all()

    medicos = Medico.query.all()

    return render_template(

        'consultas/editar.html',

        consulta=consulta,

        pacientes=pacientes,

        medicos=medicos

    )


# UPDATE

@consulta_bp.route(
    '/consultas/update/<int:id>',
    methods=['POST']
)
@login_required
def update_consulta(id):

    consulta = Consulta.query.get_or_404(id)

    consulta.fecha = request.form['fecha']

    consulta.diagnostico = request.form[
        'diagnostico'
    ]

    consulta.tratamiento = request.form[
        'tratamiento'
    ]

    consulta.observaciones = request.form[
        'observaciones'
    ]

    consulta.id_paciente = request.form[
        'id_paciente'
    ]

    consulta.id_medico = request.form[
        'id_medico'
    ]

    db.session.commit()

    flash(
        'Consulta actualizada correctamente',
        'warning'
    )

    return redirect('/consultas')


# ELIMINAR

@consulta_bp.route(
    '/consultas/delete/<int:id>'
)
@login_required
def delete_consulta(id):

    consulta = Consulta.query.get_or_404(id)

    db.session.delete(consulta)

    db.session.commit()

    flash(
        'Consulta eliminada correctamente',
        'danger'
    )

    return redirect('/consultas')


# EXPORTAR PDF

@consulta_bp.route(
    '/consultas/reporte/pdf'
)
@login_required
def reporte_pdf():

    consultas = Consulta.query.all()

    buffer = io.BytesIO()

    p = canvas.Canvas(buffer)

    p.setFont(
        'Helvetica-Bold',
        18
    )

    p.drawString(
        180,
        800,
        'REPORTE DE CONSULTAS'
    )

    y = 760

    p.setFont(
        'Helvetica',
        12
    )

    for consulta in consultas:

        texto = (

            f'Fecha: {consulta.fecha} | '

            f'Paciente: {consulta.paciente.nombre} | '

            f'Médico: {consulta.medico.nombre}'

        )

        p.drawString(
            40,
            y,
            texto
        )

        y -= 30

    p.save()

    buffer.seek(0)

    response = make_response(
        buffer.getvalue()
    )
    response.headers['Content-Type'] = (
        'application/pdf'
    )

    response.headers[
        'Content-Disposition'
    ] = (

        'inline; filename=consultas.pdf'

    )

    return response