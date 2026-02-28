import sqlite3

def conectar():
    return sqlite3.connect("clinica.db")

def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            motivo TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()