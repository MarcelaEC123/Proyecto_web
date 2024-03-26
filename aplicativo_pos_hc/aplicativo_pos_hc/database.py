import mysql.connector

# Función para conectar a la base de datos y crear un cursor
# def conectar_bd():
database = mysql.connector.connect(
        host="localhost",
        user="root",
        password="SQLMARCE2022.",
        database="Aplicativo_POS_final"
    )
    # cursor = db.cursor()
    # return db, cursor
 