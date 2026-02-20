from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# RUTA DINÁMICA DEL NEGOCIO (CLÍNICA)
@app.route('/cita/<paciente>')
def cita(paciente):
    return f'Bienvenido {paciente}. Tu cita médica ha sido registrada correctamente.'

if __name__ == '__main__':
    app.run(debug=True)