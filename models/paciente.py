from models import db


class Paciente(db.Model):

    __tablename__ = 'pacientes'

    id_paciente = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(150),
        nullable=False
    )

    edad = db.Column(
        db.Integer,
        nullable=False
    )

    direccion = db.Column(
        db.String(255),
        nullable=False
    )

    telefono = db.Column(
        db.String(30),
        nullable=False
    )

    genero = db.Column(
        db.String(30),
        nullable=False
    )

    fecha_registro = db.Column(
        db.String(50)
    )

    # RELACIONES

    consultas = db.relationship(
        'Consulta',
        backref='paciente',
        lazy=True,
        cascade='all, delete'
    )

    citas = db.relationship(
        'Cita',
        backref='paciente',
        lazy=True,
        cascade='all, delete'
    )