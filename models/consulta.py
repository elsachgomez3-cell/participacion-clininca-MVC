from models import db


class Consulta(db.Model):

    __tablename__ = 'consultas'

    id_consulta = db.Column(
        db.Integer,
        primary_key=True
    )

    fecha = db.Column(
        db.String(50),
        nullable=False
    )

    diagnostico = db.Column(
        db.Text,
        nullable=False
    )

    tratamiento = db.Column(
        db.Text,
        nullable=False
    )

    observaciones = db.Column(
        db.Text
    )

    id_paciente = db.Column(
        db.Integer,
        db.ForeignKey('pacientes.id_paciente'),
        nullable=False
    )

    id_medico = db.Column(
        db.Integer,
        db.ForeignKey('medicos.id_medico'),
        nullable=False
    )