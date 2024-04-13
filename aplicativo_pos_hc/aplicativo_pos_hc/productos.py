from flask import Flask, request, render_template, redirect, url_for
from database import conectar_bd

app = Flask(__name__)

# Ruta para mostrar la página de productos
@app.route("/productos")
def productos():
    db_connection, cursor = conectar_bd()

    # Obtener el próximo valor autoincremental de id_producto
    cursor.execute("SHOW TABLE STATUS LIKE 'producto'")
    table_status = cursor.fetchone()
    next_id = table_status[10]  # El índice 10 corresponde a la columna Auto_increment

    # Contar la cantidad de registros
    cursor.execute("SELECT COUNT(*) FROM producto")
    count = cursor.fetchone()[0]
    if count == 0:
        next_id = 1  # Si no hay registros, comenzar desde 1
    else:
        # Obtener el último ID y ajustar para el siguiente ID
        cursor.execute("SELECT MAX(id_producto) FROM producto")
        last_id = cursor.fetchone()[0]
        next_id = last_id + 1

    # Generar el nuevo código
    cursor.execute("SELECT MAX(codigo) FROM producto")
    last_code = cursor.fetchone()[0]
    new_code = str(int(last_code) + 1).zfill(4) if last_code else "0001"

    # Obtener los productos existentes
    cursor.execute("SELECT * FROM producto")
    productos = [dict(zip(cursor.column_names, row)) for row in cursor.fetchall()]

    cursor.close()
    db_connection.close()
    return render_template("productos.html", productos=productos, next_id=next_id, new_code=new_code)

# Ruta para guardar un nuevo producto
@app.route('/guardar', methods=['POST'])
def guardar_producto():
    datos_producto = request.form

    if validar_datos_producto(datos_producto):
        try:
            db_connection, cursor = conectar_bd()
            sql = "INSERT INTO producto (codigo, descripcion, categoria, id_proveedor, stock, valor_unitario, unidad_medida) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (datos_producto['codigo'], datos_producto['descripcion'], datos_producto['categoria'], datos_producto['id_proveedor'], datos_producto['stock'], datos_producto['valor_unitario'], datos_producto['unidad_medida']))
            db_connection.commit()
            cursor.close()
            db_connection.close()
            return redirect(url_for('productos'))
        except Exception as e:
            mensaje_error = f"Error al guardar el producto: {str(e)}"
            return render_template("mensaje.html", message=mensaje_error)
    else:
        mensaje_error = "Por favor, complete todos los campos obligatorios."
        return render_template("mensaje.html", message=mensaje_error)

# Ruta para agregar stock a un producto
@app.route('/addStock', methods=['POST'])
def add_stock():
    id_producto = request.form['id_producto']
    cantidad = request.form['cantidad']

    if id_producto and cantidad:
        try:
            db_connection, cursor = conectar_bd()
            # Obtener el stock actual del producto
            cursor.execute("SELECT stock FROM producto WHERE id_producto = %s", (id_producto,))
            stock_actual = cursor.fetchone()[0]

            # Sumar la cantidad proporcionada al stock actual
            nuevo_stock = stock_actual + int(cantidad)

            # Actualizar el stock en la base de datos
            cursor.execute("UPDATE producto SET stock = %s WHERE id_producto = %s", (nuevo_stock, id_producto))
            db_connection.commit()
            cursor.close()
            db_connection.close()
            return redirect(url_for('productos'))
        except Exception as e:
            mensaje_error = f"Error al agregar stock al producto: {str(e)}"
            return render_template("mensaje.html", message=mensaje_error)
    else:
        mensaje_error = "Por favor, complete todos los campos obligatorios."
        return render_template("mensaje.html", message=mensaje_error)

# Ruta para eliminar un producto
@app.route('/deleteProducto/<string:id_producto>')
def eliminar_producto(id_producto):
    try:
        db_connection, cursor = conectar_bd()
        sql = "DELETE FROM producto WHERE id_producto = %s"
        cursor.execute(sql, (id_producto,))
        db_connection.commit()
        cursor.close()
        db_connection.close()
        return redirect(url_for('productos'))
    except Exception as e:
        mensaje_error = f"Error al eliminar el producto: {str(e)}"
        return render_template("mensaje.html", message=mensaje_error)

# Ruta para editar un producto
@app.route('/editar_producto', methods=['POST'])
def editar_producto():
    datos_producto = request.form

    if validar_datos_producto(datos_producto):
        try:
            db_connection, cursor = conectar_bd()
            sql = "UPDATE producto SET codigo = %s, descripcion = %s, categoria = %s, id_proveedor = %s, stock = %s, valor_unitario = %s, unidad_medida = %s WHERE id_producto = %s"
            cursor.execute(sql, (datos_producto['codigo'], datos_producto['descripcion'], datos_producto['categoria'], datos_producto['id_proveedor'], datos_producto['stock'], datos_producto['valor_unitario'], datos_producto['unidad_medida'], datos_producto['id_producto']))
            db_connection.commit()
            cursor.close()
            db_connection.close()
            return redirect(url_for('productos'))
        except Exception as e:
            mensaje_error = f"Error al editar el producto: {str(e)}"
            return render_template("mensaje.html", message=mensaje_error)
    else:
        mensaje_error = "Por favor, complete todos los campos obligatorios."
        return render_template("mensaje.html", message=mensaje_error)

# Función para validar los datos del formulario de producto
def validar_datos_producto(datos_producto):
    campos_obligatorios = ['codigo', 'descripcion', 'categoria', 'id_proveedor', 'stock', 'valor_unitario', 'unidad_medida']
    for campo in campos_obligatorios:
        if not datos_producto.get(campo):
            return False
    return True

if __name__ == "__main__":
    app.run(debug=True)
