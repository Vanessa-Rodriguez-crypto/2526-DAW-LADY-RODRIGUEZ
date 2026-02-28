from flask import Flask, render_template, request, redirect
from database import crear_tabla, conectar

app = Flask(__name__)

# Crear tabla al iniciar
crear_tabla()

# -------------------------
# INICIO
# -------------------------
@app.route("/")
def inicio():
    return render_template("index.html")


# -------------------------
# ACERCA DE
# -------------------------
@app.route("/about")
def about():
    return render_template("about.html")


# -------------------------
# SOLICITAR CITA (DINÁMICA)
# -------------------------
@app.route("/cita/<paciente>")
def cita(paciente):
    return render_template("cita.html", paciente=paciente)


# -------------------------
# AGREGAR PACIENTE
# -------------------------
@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        motivo = request.form["motivo"]

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pacientes (nombre, telefono, motivo) VALUES (?, ?, ?)",
            (nombre, telefono, motivo)
        )
        conn.commit()
        conn.close()

        return redirect("/pacientes")

    return render_template("agregar_paciente.html")


# -------------------------
# LISTAR PACIENTES
# -------------------------
@app.route("/pacientes")
def pacientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pacientes")
    datos = cursor.fetchall()
    conn.close()

    return render_template("pacientes.html", pacientes=datos)


# -------------------------
# EDITAR PACIENTE
# -------------------------
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        motivo = request.form["motivo"]

        cursor.execute("""
            UPDATE pacientes
            SET nombre = ?, telefono = ?, motivo = ?
            WHERE id = ?
        """, (nombre, telefono, motivo, id))

        conn.commit()
        conn.close()

        return redirect("/pacientes")

    cursor.execute("SELECT * FROM pacientes WHERE id = ?", (id,))
    paciente = cursor.fetchone()
    conn.close()

    return render_template("editar_paciente.html", paciente=paciente)


# -------------------------
# ELIMINAR PACIENTE
# -------------------------
@app.route("/eliminar/<int:id>")
def eliminar(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pacientes WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/pacientes")


# -------------------------
# SERVIDOR
# -------------------------
import os

if __name__ == "__main__":
    app.run(debug=True)
else:
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)