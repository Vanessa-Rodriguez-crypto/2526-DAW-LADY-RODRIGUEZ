class Paciente:
    def __init__(self, id, nombre, telefono, motivo):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.motivo = motivo

    def obtener_datos(self):
        return (self.id, self.nombre, self.telefono, self.motivo)