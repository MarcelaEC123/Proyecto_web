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

def actualizar_proveedor(id_proveedor, tipo_identificacion, numero_identificacion, nombre_proveedor, email, direccion, telefono, dia_de_visita, dia_de_entrega):
    try:
        db_connection, cursor = conectar_bd()
        sql = "UPDATE proveedor SET tipo_identificacion = %s, numero_identificacion = %s, nombre_proveedor = %s, email = %s, direccion = %s, telefono = %s, dia_de_visita = %s, dia_de_entrega = %s WHERE id_proveedor = %s"
        data = (tipo_identificacion, numero_identificacion, nombre_proveedor, email, direccion, telefono, dia_de_visita, dia_de_entrega, id_proveedor)  # Agrega el ID del proveedor al final
        cursor.execute(sql, data)
        db_connection.commit()
        cursor.close()
        db_connection.close()
        return True
    except Exception as e:
        print("Error al actualizar proveedor:", e)
        return False


def actualizar_producto(id_producto, codigo, descripcion, categoria,id_proveedor, nombre_proveedor, valor_unitario, unidad_medida, stock):
    try:
        db_connection, cursor = conectar_bd()
        if db_connection is None or cursor is None:
            return False
        sql = "UPDATE producto SET codigo = %s, descripcion = %s,categoria = %s,id_proveedor = %s, nombre_proveedor = %s, valor_unitario = %s, unidad_medida = %s, stock = %s WHERE id_producto = %s"
        data = (codigo, descripcion, categoria,id_proveedor, nombre_proveedor, valor_unitario, unidad_medida, stock, id_producto)
        cursor.execute(sql, data)
        db_connection.commit()
        cursor.close()
        db_connection.close()
        return True
    except Exception as e:
        print("Error al actualizar proveedor:", e)
        return False