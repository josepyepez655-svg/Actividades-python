from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURACIÓN DE POSTGRESQL ---
USUARIO = "postgres"
PASSWORD = "123"  # Cambia por tu contraseña de PostgreSQL
HOST = "localhost"
PUERTO = "5432"
BD = "multiplicacion"

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{USUARIO}:{PASSWORD}@{HOST}:{PUERTO}/{BD}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# --- MODELOS (POO) ---
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), default='Estudiante')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    historial = db.relationship('HistorialTabla', backref='usuario', lazy=True)


class HistorialTabla(db.Model):
    __tablename__ = 'historial_tablas'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    numero = db.Column(db.Integer, nullable=False)
    fecha_consulta = db.Column(db.DateTime, default=datetime.utcnow)


# Crear las tablas automáticamente si no existen
with app.app_context():
    db.create_all()


# --- RUTAS ---
@app.route('/', methods=['GET', 'POST'])
def index():
    tabla = []
    numero = None

    if request.method == 'POST':
        try:
            numero = int(request.form.get('numero1'))

            # Generar la tabla de multiplicar del 1 al 10
            # Formato "8 x 1 = 8" para que encaje con linea.split('=') de tu HTML
            for i in range(1, 11):
                resultado = numero * i
                tabla.append(f"{numero} x {i} = {resultado}")

            # Registrar la consulta en PostgreSQL
            nueva_consulta = HistorialTabla(numero=numero)
            db.session.add(nueva_consulta)
            db.session.commit()

        except (ValueError, TypeError):
            pass

    return render_template('index.html', tabla=tabla, numero=numero)


if __name__ == '__main__':
    app.run(debug=True)