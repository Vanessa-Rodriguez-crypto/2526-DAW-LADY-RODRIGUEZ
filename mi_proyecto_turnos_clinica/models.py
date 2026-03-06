from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    motivo = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Paciente {self.nombre}>'