import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def obtener_conexion():
    return psycopg2.connect(
        host="localhost", database="par", user="postgres", password="123"
    )


# Verificar e inicializar la tabla al arrancar
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

    if request.method == "POST":
        # 1. SI SE ENVÍA UN NÚMERO
        valor_recibido = request.form.get("definir")
        if valor_recibido:
            try:
                numero = int(valor_recibido)
                resultado = "PAR" if numero % 2 == 0 else "IMPAR"

                # Guardar en PostgreSQL
                conn = obtener_conexion()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO historial (numero, resultado) VALUES (%s, %s)",
                    (numero, resultado),
                )
                conn.commit()
                cur.close()
                conn.close()
            except ValueError:
                pass

        # 2. SI SE PRESIONA EL BOTÓN DE BORRAR DATOS
        if "Borrar" in request.form:
            conn = obtener_conexion()
            cur = conn.cursor()
            cur.execute("DELETE FROM historial")
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for("inicio"))

    # 3. CONSULTAR HISTORIAL ACTUALIZADO
    historial_guardado = []
    try:
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("SELECT numero, resultado FROM historial ORDER BY id DESC")
        historial_guardado = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error al consultar historial: {e}")

    return render_template(
        "index.html",
        usuario_actual=usuario,
        resultado=resultado,
        numero=numero,
        historial=historial_guardado,
    )


if __name__ == "__main__":
    app.run(debug=True)