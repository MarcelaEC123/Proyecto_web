from flask import Flask, request, render_template, redirect, url_for
from database import conectar_bd

app = Flask(__name__)

# Ruta para mostrar la página de proveedores
@app.route("/proveedores")
def proveedores():
    db_connection, cursor = conectar_bd()

    # Obtener el próximo valor autoincremental de id_proveedor
    cursor.execute("SHOW TABLE STATUS LIKE 'proveedor'")
    table_status = cursor.fetchone()
    next_id = table_status[10]  # El índice 10 corresponde a la columna Auto_increment

    # Contar la cantidad de registros
    cursor.execute("SELECT COUNT(*) FROM proveedor")
    count = cursor.fetchone()[0]
    if count == 0:
        next_id = 1  # Si no hay registros, comenzar desde 1
    else:
        # Obtener el último ID y ajustar para el siguiente ID
        cursor.execute("SELECT MAX(id_proveedor) FROM proveedor")
        last_id = cursor.fetchone()[0]
        next_id = last_id + 1

    # Obtener los proveedores existentes
    cursor.execute("SELECT * FROM proveedor")
    proveedores = [dict(zip(cursor.column_names, row)) for row in cursor.fetchall()]

    cursor.close()
    db_connection.close()
    return render_template("proveedores.html", proveedores=proveedores, next_id=next_id)

# Ruta para guardar un nuevo proveedor
@app.route('/guardarProveedores', methods=['POST'])
def guardar_proveedor():
    datos_proveedor = request.form

    if validar_datos_proveedor(datos_proveedor):
        try:
            db_connection, cursor = conectar_bd()
            sql = "INSERT INTO proveedor (id_proveedor, tipo_identificacion, numero_identificacion, nombre_proveedor, email, direccion, telefono, dia_de_visita, dia_de_entrega) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (datos_proveedor['id_proveedor'], datos_proveedor['tipo_identificacion'], datos_proveedor['numero_identificacion'], datos_proveedor['nombre_proveedor'], datos_proveedor['email'], datos_proveedor['direccion'], datos_proveedor['telefono'], datos_proveedor['dia_de_visita'], datos_proveedor['dia_de_entrega']))
            db_connection.commit()
            cursor.close()
            db_connection.close()
            return redirect(url_for('proveedores'))
        except Exception as e:
            mensaje_error = f"Error al guardar el proveedor: {str(e)}"
            return render_template("mensaje.html", message=mensaje_error)
    else:
        mensaje_error = "Por favor, complete todos los campos obligatorios."
        return render_template("mensaje.html", message=mensaje_error)

# Ruta para eliminar un proveedor
@app.route('/deleteProveedor/<string:id_proveedor>')
def eliminar_proveedor(id_proveedor):
    try:
        db_connection, cursor = conectar_bd()
        sql = "DELETE FROM proveedor WHERE id_proveedor = %s"
        cursor.execute(sql, (id_proveedor,))
        db_connection.commit()
        cursor.close()
        db_connection.close()
        return redirect(url_for('proveedores'))
    except Exception as e:
        mensaje_error = f"Error al eliminar el proveedor: {str(e)}"
        return render_template("mensaje.html", message=mensaje_error)

# Ruta para editar un proveedor
@app.route('/editarProveedor', methods=['POST'])
def editar_proveedor():
    datos_proveedor = request.form

    if validar_datos_proveedor(datos_proveedor):
        try:
            db_connection, cursor = conectar_bd()
            sql = "UPDATE proveedor SET tipo_identificacion = %s, numero_identificacion = %s, nombre_proveedor = %s, email = %s, direccion = %s, telefono = %s, dia_de_visita = %s, dia_de_entrega = %s WHERE id_proveedor = %s"
            cursor.execute(sql, (datos_proveedor['tipo_identificacion'], datos_proveedor['numero_identificacion'], datos_proveedor['nombre_proveedor'], datos_proveedor['email'], datos_proveedor['direccion'], datos_proveedor['telefono'], datos_proveedor['dia_de_visita'], datos_proveedor['dia_de_entrega'], datos_proveedor['id_proveedor']))
            db_connection.commit()
            cursor.close()
            db_connection.close()
            return redirect(url_for('proveedores'))
        except Exception as e:
            mensaje_error = f"Error al editar el proveedor: {str(e)}"
            return render_template("mensaje.html", message=mensaje_error)
    else:
        mensaje_error = "Por favor, complete todos los campos obligatorios."
        return render_template("mensaje.html", message=mensaje_error)

# Función para validar los datos del formulario de proveedor
def validar_datos_proveedor(datos_proveedor):
    campos_obligatorios = ['id_proveedor', 'tipo_identificacion', 'numero_identificacion', 'nombre_proveedor', 'email', 'direccion', 'telefono', 'dia_de_visita', 'dia_de_entrega']
    for campo in campos_obligatorios:
        if not datos_proveedor.get(campo):
            return False
    return True

if __name__ == "__main__":
    app.run(debug=True)
