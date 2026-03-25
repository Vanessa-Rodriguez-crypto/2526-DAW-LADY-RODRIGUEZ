class PacienteForm:

    def __init__(self, form):
        self.nombre = form.get("nombre")
        self.telefono = form.get("telefono")
        self.motivo = form.get("motivo")

    def validar(self):
        if not self.nombre or not self.telefono or not self.motivo:
            return False
        return True