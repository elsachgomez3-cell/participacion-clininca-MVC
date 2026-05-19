from models import db


class Medico(db.Model):

    __tablename__ = 'medicos'

    id_medico = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    especialidad = db.Column(
        db.String(100),
        nullable=False
    )

    telefono = db.Column(
        db.String(20)
    )

    correo = db.Column(
        db.String(100)
    )

    horario = db.Column(
        db.String(100)
    )

    # RELACIONES

    consultas = db.relationship(
        'Consulta',
        backref='medico',
        lazy=True,
        cascade='all, delete'
    )

    citas = db.relationship(
        'Cita',
        backref='medico',
        lazy=True,
        cascade='all, delete'
    )