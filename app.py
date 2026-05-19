from flask import Flask, render_template
import os
from flask_login import (
    LoginManager,
    login_required
)

from config import Config

# APP

app = Flask(__name__)

app.config.from_object(Config)

# DATABASE

from models import db

db.init_app(app)

# LOGIN

login_manager = LoginManager()

login_manager.login_view = 'auth_bp.login'

login_manager.init_app(app)

# =========================
# IMPORTAR MODELOS
# =========================

from models.usuario import Usuario
from models.medico import Medico
from models.paciente import Paciente
from models.consulta import Consulta
from models.cita import Cita

# =========================
# USER LOADER
# =========================

@login_manager.user_loader
def load_user(user_id):

    return Usuario.query.get(int(user_id))

# =========================
# IMPORTAR CONTROLLERS
# =========================

from controllers.auth_controller import auth_bp
from controllers.medico_controller import medico_bp
from controllers.paciente_controller import paciente_bp
from controllers.consulta_controller import consulta_bp
from controllers.cita_controller import cita_bp

# =========================
# REGISTRAR BLUEPRINTS
# =========================

app.register_blueprint(auth_bp)

app.register_blueprint(medico_bp)

app.register_blueprint(paciente_bp)

app.register_blueprint(consulta_bp)

app.register_blueprint(cita_bp)

# =========================
# DASHBOARD
# =========================

@app.route('/')
@login_required
def home():

    total_pacientes = Paciente.query.count()

    total_medicos = Medico.query.count()

    total_consultas = Consulta.query.count()

    total_citas = Cita.query.count()

    return render_template(

        'dashboard.html',

        total_pacientes=total_pacientes,

        total_medicos=total_medicos,

        total_consultas=total_consultas,

        total_citas=total_citas

    )

# =========================
# CREAR TABLAS
# =========================

with app.app_context():

    db.create_all()

# =========================
# RUN
# =========================

if __name__ == '__main__':
    # Render usa la variable de entorno PORT, si no existe usa el 5000 por defecto
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)