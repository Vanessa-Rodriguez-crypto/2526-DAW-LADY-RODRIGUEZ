from flask import Flask, render_template

app = Flask(__name__)

# Ruta principal
@app.route('/')
def inicio():
    return render_template('index.html')

# Ruta dinámica
@app.route('/cita/<paciente>')
def cita(paciente):
    return f'Bienvenido {paciente}, tu cita médica ha sido registrada correctamente.'

# IMPORTANTE PARA RENDER
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
