from models import db


class Cita(db.Model):

    __tablename__ = 'citas'

    id_cita = db.Column(
        db.Integer,
        primary_key=True
    )

    fecha = db.Column(
        db.String(50),
        nullable=False
    )

    hora = db.Column(
        db.String(20),
        nullable=False
    )

    motivo = db.Column(
        db.String(255),
        nullable=False
    )

    estado = db.Column(
        db.String(50),
        default='Pendiente'
    )

    id_paciente = db.Column(
        db.Integer,
        db.ForeignKey(
            'pacientes.id_paciente'
        ),
        nullable=False
    )

    id_medico = db.Column(
        db.Integer,
        db.ForeignKey(
            'medicos.id_medico'
        ),
        nullable=False
    )