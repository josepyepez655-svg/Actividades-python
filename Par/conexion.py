import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)


def obtener_conexion():
    return psycopg2.connect(
        host="localhost", database="par", user="postgres", password="123"
    )

# Asegurarnos de que la tabla exista
try:
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS historial (
            id SERIAL PRIMARY KEY,
            numero INT NOT NULL,
            resultado VARCHAR(10) NOT NULL
        )
    """
    )
    conn.commit()
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error al verificar la tabla: {e}")


@app.route("/", methods=["GET", "POST"])
def inicio():
    resultado = None
    numero = None
    usuario = "Elkin"

    # 1. SI EL USUARIO ENVÍA UN NÚMERO (POST)
    if request.method == "POST":
        valor_recibido = request.form.get("definir")

        if valor_recibido:
            numero = int(valor_recibido)
            resultado = "PAR" if numero % 2 == 0 else "IMPAR"

            # Insertar en PostgreSQL
            conn = obtener_conexion()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO historial (numero, resultado) VALUES (%s, %s)",
                (numero, resultado),
            )
            conn.commit()  # Confirmar cambios en la base de datos
            cur.close()
            conn.close()

    # 2. CONSULTAR TODOS LOS REGISTROS PARA MOSTRARLOS
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("SELECT numero, resultado FROM historial ORDER BY id DESC")
    historial_guardado = cur.fetchall()
    cur.close()
    conn.close()

    return render_template(
        "index.html",
        usuario_actual=usuario,
        resultado=resultado,
        numero=numero,
        historial=historial_guardado,
    )


if __name__ == "__main__":
    app.run(debug=True)