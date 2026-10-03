from flask import Flask, render_template, request, session, redirect, url_for
import random
from conexion import db, init_db, Jugador, Partida


app = Flask(__name__, template_folder='.', static_folder='static')
app.secret_key = "clave_secreta_futurista"

# Conectar e inicializar tablas en PostgreSQL
init_db(app)


class JuegoAdivinanza:
    def __init__(self, limite_inferior=1, limite_superior=100):
        self.limite_inferior = limite_inferior
        self.limite_superior = limite_superior

    def nuevo_numero(self):
        return random.randint(self.limite_inferior, self.limite_superior)


juego = JuegoAdivinanza(1, 100)


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'numero_secreto' not in session:
        session['numero_secreto'] = juego.nuevo_numero()
        session['intentos'] = 0
        session['mensaje'] = "SISTEMA INICIALIZADO. Ingresa un número del 1 al 100."
        session['ganado'] = False

    if request.method == 'POST':
        if 'reiniciar' in request.form:
            session.clear()
            return redirect(url_for('index'))

        try:
            intento = int(request.form.get('numero'))
            session['intentos'] += 1

            if intento < session['numero_secreto']:
                session['mensaje'] = f"ACCESO DENEGADO: El número secreto es MAYOR que {intento}."
            elif intento > session['numero_secreto']:
                session['mensaje'] = f"ACCESO DENEGADO: El número secreto es MENOR que {intento}."
            else:
                session['mensaje'] = f"¡ACCESO CONCEDIDO! Adivinaste el número en {session['intentos']} intentos."
                session['ganado'] = True

                # Guardar el intento exitoso en PostgreSQL
                nuevo_jugador = Jugador(nombre="Jugador 1", puntuacion=session['intentos'])
                db.session.add(nuevo_jugador)
                db.session.commit()

                nueva_partida = Partida(
                    jugador_id=nuevo_jugador.id,
                    intentos=session['intentos'],
                    numero_secreto=session['numero_secreto']
                )
                db.session.add(nueva_partida)
                db.session.commit()

        except (ValueError, TypeError):
            session['mensaje'] = "ERROR DE ENTRADA: Ingrese un número válido."

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)