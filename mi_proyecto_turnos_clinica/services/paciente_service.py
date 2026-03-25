from conexion.conexion import conectar

# INSERTAR
def insertar_paciente(nombre, telefono, motivo):

    conn = conectar()
    cursor = conn.cursor()

    sql = "INSERT INTO pacientes (nombre, telefono, motivo) VALUES (%s,%s,%s)"
    cursor.execute(sql, (nombre, telefono, motivo))

    conn.commit()
    conn.close()


# LISTAR
def obtener_pacientes():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pacientes")
    datos = cursor.fetchall()

    conn.close()
    return datos


# ELIMINAR
def eliminar_paciente_mysql(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM pacientes WHERE id = %s", (id,))
    conn.commit()

    conn.close()