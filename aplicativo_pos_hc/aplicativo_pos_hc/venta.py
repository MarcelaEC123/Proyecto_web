def obtener_detalles_de_venta(id_venta):
    try:
        from database import conectar_bd  # Importar dentro de la función
        db_connection, cursor = conectar_bd()
        cursor.execute("SELECT * FROM venta WHERE id_venta = %s", (id_venta,))
        venta = cursor.fetchone()
        cursor.close()
        db_connection.close()
        return venta
    except Exception as e:
        print(f"Error al obtener los detalles de la venta desde la base de datos: {str(e)}")
        return None
