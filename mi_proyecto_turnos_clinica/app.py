from flask import Flask, render_template, request, redirect
from models import db, Paciente

import json
import csv
import os

app = Flask(__name__)

# CONFIGURACIÓN SQLITE
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clinica.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Crear base de datos
with app.app_context():
    db.create_all()


# -------------------------
# GUARDAR DATOS EN ARCHIVOS
# -------------------------
def guardar_archivos(nombre, telefono, motivo):

    os.makedirs("data", exist_ok=True)

    # TXT
    with open("data/pacientes.txt", "a") as f:
        f.write(f"{nombre},{telefono},{motivo}\n")

    # JSON
    try:
        with open("data/pacientes.json", "r") as f:
            datos = json.load(f)
    except:
        datos = []

    datos.append({
        "nombre": nombre,
        "telefono": telefono,
        "motivo": motivo
    })

    with open("data/pacientes.json", "w") as f:
        json.dump(datos, f, indent=4)

    # CSV
    archivo_csv = "data/pacientes.csv"

    existe = os.path.isfile(archivo_csv)

    with open(archivo_csv, "a", newline="") as f:
        writer = csv.writer(f)

        if not existe:
            writer.writerow(["nombre", "telefono", "motivo"])

        writer.writerow([nombre, telefono, motivo])


# -------------------
# PAGINA PRINCIPAL
# -------------------
@app.route('/')
def inicio():
    return render_template("index.html")


# -------------------
# ACERCA DE
# -------------------
@app.route('/about')
def about():
    return render_template("about.html")


# -------------------
# LISTAR PACIENTES
# -------------------
@app.route("/pacientes")
def pacientes():
    pacientes = Paciente.query.all()
    return render_template("pacientes.html", pacientes=pacientes)


# -------------------
# SOLICITAR CITA
# -------------------
@app.route('/cita', methods=["GET", "POST"])
def cita():

    if request.method == "POST":

        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        motivo = request.form["motivo"]

        # guardar en archivos
        guardar_archivos(nombre, telefono, motivo)

        # guardar en SQLite con SQLAlchemy
        nuevo = Paciente(
            nombre=nombre,
            telefono=telefono,
            motivo=motivo
        )

        db.session.add(nuevo)
        db.session.commit()

        return redirect("/pacientes")

    return render_template("cita.html")


# -------------------
# AGREGAR PACIENTE
# -------------------
@app.route("/agregar", methods=["GET","POST"])
def agregar_paciente():

    if request.method == "POST":

        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        motivo = request.form["motivo"]

        guardar_archivos(nombre, telefono, motivo)

        nuevo = Paciente(
            nombre=nombre,
            telefono=telefono,
            motivo=motivo
        )

        db.session.add(nuevo)
        db.session.commit()

        return redirect("/pacientes")

    return render_template("agregar_paciente.html")


# -------------------
# ELIMINAR PACIENTE
# -------------------
@app.route("/eliminar/<int:id>")
def eliminar(id):

    paciente = Paciente.query.get(id)

    db.session.delete(paciente)
    db.session.commit()

    return redirect("/pacientes")


# -------------------
# EDITAR PACIENTE
# -------------------
@app.route("/editar/<int:id>", methods=["GET","POST"])
def editar(id):

    paciente = Paciente.query.get(id)

    if request.method == "POST":

        paciente.nombre = request.form["nombre"]
        paciente.telefono = request.form["telefono"]
        paciente.motivo = request.form["motivo"]

        db.session.commit()

        return redirect("/pacientes")

    return render_template("editar_paciente.html", paciente=paciente)


# -------------------
# MOSTRAR DATOS TXT JSON CSV
# -------------------
@app.route("/datos")
def ver_datos():

    # -------- TXT --------
    datos_txt = []
    try:
        with open("data/pacientes.txt", "r") as archivo:
            for linea in archivo:
                datos_txt.append(linea.strip().split(","))
    except:
        pass


    # -------- JSON --------
    datos_json = []
    try:
        import json
        with open("data/pacientes.json", "r") as archivo:
            datos_json = json.load(archivo)
    except:
        pass


    # -------- CSV --------
    datos_csv = []
    try:
        import csv
        with open("data/pacientes.csv", "r") as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                datos_csv.append(fila)
    except:
        pass


    return render_template(
        "datos.html",
        txt=datos_txt,
        json=datos_json,
        csv=datos_csv
    )


# -------------------
# EJECUTAR APP
# -------------------
if __name__ == "__main__":
    app.run(debug=True)