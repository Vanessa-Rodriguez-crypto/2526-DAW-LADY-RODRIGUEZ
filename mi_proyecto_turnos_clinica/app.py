from flask import Flask, render_template

app = Flask(__name__)

# Página principal
@app.route('/')
def inicio():
    return render_template('index.html')

# Ruta dinámica
@app.route('/cita/<paciente>')
def cita(paciente):
    return f'<h2>Bienvenido, {paciente}. Tu cita médica está en proceso.</h2>'

if __name__ == '__main__':
    app.run(debug=True)
