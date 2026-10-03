from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Configuración de PostgreSQL (Asegúrate de que la clave '123' sea la correcta en esta PC)
USUARIO = "postgres"
PASSWORD = "123"
HOST = "localhost"
PUERTO = "5432"
BD = "adivina"

DATABASE_URL = f'postgresql+psycopg2://{USUARIO}:{PASSWORD}@{HOST}:{PUERTO}/{BD}'


# --- MODELOS ---
class Jugador(db.Model):
    __tablename__ = 'jugadores'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    puntuacion = db.Column(db.Integer, default=0)

    partidas = db.relationship('Partida', backref='jugador', lazy=True)


class Partida(db.Model):
    __tablename__ = 'partidas'

    id = db.Column(db.Integer, primary_key=True)
    jugador_id = db.Column(db.Integer, db.ForeignKey('jugadores.id'), nullable=False)
    intentos = db.Column(db.Integer, nullable=False)
    numero_secreto = db.Column(db.Integer, nullable=False)


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()  # Crea las tablas automáticamente en PostgreSQL