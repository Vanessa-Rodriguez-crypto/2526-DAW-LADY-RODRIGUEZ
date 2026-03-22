from flask import Flask, render_template, request, redirect
from models import db, Paciente, Usuario
from conexion.conexion import conectar
import json
import csv
import os

# LOGIN
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

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
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
    user = cursor.fetchone()

    conn.close()

    if user:
        return Usuario(user[0], user[1], user[2], user[3])
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

    with open("data/pacientes.txt", "a") as f:
        f.write(f"{nombre},{telefono},{motivo}\n")

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

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[3], password):
            usuario = Usuario(user[0], user[1], user[2], user[3])
            login_user(usuario)
            return redirect('/panel')

        return "Correo o contraseña incorrectos"

    return render_template('login.html')


# ------------------------
# REGISTRO
# ------------------------
@app.route('/registro', methods=['GET', 'POST'])
def registro():

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = conectar()
        cursor = conn.cursor()

        sql = "INSERT INTO usuarios (nombre, email, password) VALUES (%s,%s,%s)"
        valores = (nombre, email, password)

        cursor.execute(sql, valores)
        conn.commit()
        conn.close()

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
# PACIENTES (PROTEGIDO)
# ------------------------
@app.route("/pacientes")
@login_required
def pacientes():
    pacientes = Paciente.query.all()
    return render_template("pacientes.html", pacientes=pacientes)


# ------------------------
# CITA (PROTEGIDO)
# ------------------------
@app.route('/cita', methods=["GET", "POST"])
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
# AGREGAR PACIENTE
# ------------------------
@app.route("/agregar", methods=["GET","POST"])
@login_required
def agregar_paciente():

    if request.method == "POST":
        print("ENTRANDO POST")  # prueba

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

        conn = conectar()
        cursor = conn.cursor()

        sql = "INSERT INTO pacientes (nombre, telefono, motivo) VALUES (%s,%s,%s)"
        valores = (nombre, telefono, motivo)

        cursor.execute(sql, valores)
        conn.commit()
        conn.close()

        return redirect("/pacientes")

  
    print("ENTRANDO GET")
    return render_template("agregar_paciente.html")


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
# MOSTRAR DATOS
# ------------------------
@app.route("/datos")
@login_required
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
        with open("data/pacientes.json", "r") as archivo:
            datos_json = json.load(archivo)
    except:
        pass

    # -------- CSV --------
    datos_csv = []
    try:
        with open("data/pacientes.csv", "r") as archivo:
            lector = csv.reader(archivo)
            next(lector, None)  # 👈 saltar cabecera
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

# ------------------------
# TEST MYSQL
# ------------------------
@app.route("/test_mysql")
def test_mysql():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SHOW TABLES")
    tablas = cursor.fetchall()

    conn.close()

    return str(tablas)


# ------------------------
# RUN
# ------------------------
if __name__ == "__main__":
    app.run(debug=True)