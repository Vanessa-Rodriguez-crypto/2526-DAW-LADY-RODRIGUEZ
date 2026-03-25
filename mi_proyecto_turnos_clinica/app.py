from flask import Flask, render_template, request, redirect, send_file
from models import db, Paciente, Usuario, Cita
from services.paciente_service import insertar_paciente
from conexion.conexion import conectar
import json
import csv
import os

# LOGIN
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

# PDF
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = "clave_secreta_clinica"

# ------------------------
# CONFIG LOGIN
# ------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM usuarios WHERE id_usuario = %s",
            (user_id,)
        )
        user = cursor.fetchone()

        conn.close()

        if user:
            class UserLogin(Usuario):
                pass

            usuario = UserLogin()
            usuario.id_usuario = user["id_usuario"]
            usuario.nombre = user["nombre"]
            usuario.email = user["email"]
            usuario.password = user["password"]

            return usuario

    except Exception as e:
        print("Error load_user:", e)

    return None

# ------------------------
# SQLITE
# ------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clinica.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# ------------------------
# GUARDAR ARCHIVOS
# ------------------------
def guardar_archivos(nombre, telefono, motivo):

    os.makedirs("data", exist_ok=True)

    # -------- TXT --------
    with open("data/pacientes.txt", "a") as f:
        f.write(f"{nombre},{telefono},{motivo}\n")

    # -------- JSON --------
    try:
        with open("data/pacientes.json", "r") as f:
            datos = json.load(f)
    except:
        datos = []

    nuevo = {
        "nombre": nombre,
        "telefono": telefono,
        "motivo": motivo
    }

    # SOLO AGREGA SI NO EXISTE
    if nuevo not in datos:
        datos.append(nuevo)

    with open("data/pacientes.json", "w") as f:
        json.dump(datos, f, indent=4)

    # -------- CSV --------
    archivo_csv = "data/pacientes.csv"
    existe = os.path.isfile(archivo_csv)

    with open(archivo_csv, "a", newline="") as f:
        writer = csv.writer(f)

        if not existe:
            writer.writerow(["nombre", "telefono", "motivo"])

        writer.writerow([nombre, telefono, motivo])


# ------------------------
# LOGIN 
# ------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            conn = conectar()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = cursor.fetchone()

            conn.close()

        except Exception as e:
            print("Error login:", e)
            user = None

        if user:
            print("Usuario encontrado:", user)

            if check_password_hash(user["password"], password):

                # crear objeto manual compatible con Flask-Login
                class UserLogin(Usuario):
                    pass

                usuario = UserLogin()
                usuario.id_usuario = user["id_usuario"]
                usuario.nombre = user["nombre"]
                usuario.email = user["email"]
                usuario.password = user["password"]

                login_user(usuario)
                return redirect('/panel')

        return "Correo o contraseña incorrectos"

    return render_template('login.html')

#-----------------------
#solicitar cita 
#-----------------------
@app.route('/cita', methods=['GET','POST'])
@login_required
def cita():

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

    return render_template("cita.html")


# ------------------------
# REGISTRO
# ------------------------
@app.route('/registro', methods=['GET', 'POST'])
def registro():

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        try:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO usuarios (nombre, email, password) VALUES (%s,%s,%s)",
                (nombre, email, password)
            )

            conn.commit()
            conn.close()
        except Exception as e:
             print("ERROR MYSQL:", e)

        return redirect('/login')

    return render_template('registro.html')


# ------------------------
# LOGOUT
# ------------------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


# ------------------------
# PANEL
# ------------------------
@app.route('/panel')
@login_required
def panel():
    return render_template("panel.html")


# ------------------------
# PAGINAS
# ------------------------
@app.route('/')
def inicio():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")


# ------------------------
# LISTAR PACIENTES
# ------------------------
@app.route("/pacientes")
@login_required
def pacientes():
    pacientes = Paciente.query.all()
    return render_template("pacientes.html", pacientes=pacientes)


# ------------------------
# AGREGAR PACIENTE
# ------------------------
@app.route("/agregar", methods=["GET","POST"])
@login_required
def agregar_paciente():

    if request.method == "POST":

        from forms.paciente_form import PacienteForm
        form = PacienteForm(request.form)

        if not form.validar():
            return "Datos incompletos"

        nombre = form.nombre
        telefono = form.telefono
        motivo = form.motivo

        # Guardar en archivos (txt, json, csv)
        guardar_archivos(nombre, telefono, motivo)

        # GUARDAR EN BASE DE DATOS (SQLITE - SQLAlchemy)
        nuevo = Paciente(
            nombre=nombre,
            telefono=telefono,
            motivo=motivo
        )

        db.session.add(nuevo)
        db.session.commit()

        return redirect("/pacientes")

    return render_template("agregar_paciente.html")

# ------------------------
# EDITAR
# ------------------------
@app.route("/editar/<int:id>", methods=["GET","POST"])
@login_required
def editar(id):

    paciente = Paciente.query.get(id)

    if request.method == "POST":
        paciente.nombre = request.form["nombre"]
        paciente.telefono = request.form["telefono"]
        paciente.motivo = request.form["motivo"]

        db.session.commit()
        return redirect("/pacientes")

    return render_template("editar_paciente.html", paciente=paciente)


# ------------------------
# ELIMINAR
# ------------------------
@app.route("/eliminar/<int:id>")
@login_required
def eliminar(id):
    paciente = Paciente.query.get(id)
    db.session.delete(paciente)
    db.session.commit()
    return redirect("/pacientes")


# ------------------------
# DATOS ARCHIVOS
# ------------------------
@app.route("/datos")
@login_required
def ver_datos():

    datos_txt = []
    try:
        with open("data/pacientes.txt", "r") as archivo:
            for linea in archivo:
                datos_txt.append(linea.strip().split(","))
    except:
        pass

    datos_json = []
    try:
        with open("data/pacientes.json", "r") as archivo:
            datos_json = json.load(archivo)
    except:
        pass

    datos_csv = []
    try:
        with open("data/pacientes.csv", "r") as archivo:
            lector = csv.reader(archivo)
            next(lector, None)
            for fila in lector:
                datos_csv.append(fila)
    except:
        pass

    return render_template("datos.html", txt=datos_txt, json=datos_json, csv=datos_csv)


# ------------------------
# REPORTE PDF
# ------------------------
@app.route('/reporte')
@login_required
def reporte():

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pacientes")
        datos = cursor.fetchall()
        conn.close()
    except:
        datos = []

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt="Reporte de Pacientes", ln=True, align='C')

    pdf.set_font("Arial", size=10)

    for p in datos:
        pdf.cell(200, 10, txt=f"{p[1]} - {p[2]} - {p[3]}", ln=True)

    pdf.output("reporte.pdf")

    return send_file("reporte.pdf", as_attachment=True)


# ------------------------
# TEST MYSQL
# ------------------------
@app.route("/test_mysql")
def test_mysql():

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tablas = cursor.fetchall()
        conn.close()
        return str(tablas)
    except:
        return "Error MySQL"


# ------------------------
# RUN
# ------------------------
if __name__ == "__main__":
    app.run(debug=True)