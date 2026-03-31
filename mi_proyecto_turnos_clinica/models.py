from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# ------------------------
# USUARIOS (LOGIN)
# ------------------------
class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(200))

    
    def get_id(self):
        return str(self.id_usuario)
    
# ------------------------
# PACIENTES
# ------------------------
class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    motivo = db.Column(db.String(200), nullable=False)

    #  RELACIÓN
    citas = db.relationship('Cita', backref='paciente')

    def __repr__(self):
        return f'<Paciente {self.nombre}>'

# ------------------------
# CITAS 
# ------------------------
class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('paciente.id'))
    fecha = db.Column(db.String(50))
    motivo = db.Column(db.String(200))