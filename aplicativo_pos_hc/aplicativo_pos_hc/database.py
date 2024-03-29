import mysql.connector

# Función para conectar a la base de datos y crear un cursor
def conectar_bd():
    database = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Aplicativo_POS_final"
    )
    cursor = database.cursor()
    return database, cursor

