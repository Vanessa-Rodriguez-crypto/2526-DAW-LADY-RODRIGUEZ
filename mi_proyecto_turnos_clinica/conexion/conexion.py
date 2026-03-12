import mysql.connector

def conectar():

    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="clinica"
    )

    return conexion