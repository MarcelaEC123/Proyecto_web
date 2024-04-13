from flask import Flask, request, render_template, redirect, url_for
from database import conectar_bd

app = Flask(__name__)

# Función para validar los datos del formulario
def validar_datos_cliente(formulario):
    campos_obligatorios = ['id_cliente', 'tipo_identificacion', 'numero_identificacion', 'nombre_completo', 'email', 'direccion', 'telefono']
    for campo in campos_obligatorios:
        if not formulario.get(campo):
            return False
    return True

# Ruta para mostrar la página de clientes
@app.route("/clientes")
def mostrar_clientes():
    db_connection, cursor = conectar_bd()
    cursor.execute("SELECT * FROM cliente")
    clientes = [dict(zip(cursor.column_names, row)) for row in cursor.fetchall()]
    cursor.close()
    db_connection.close()
    return render_template("clientes.html", clientes=clientes)

# Ruta para guardar un nuevo cliente
@app.route('/guardarClientes', methods=['POST'])
def guardar_cliente():
    datos_cliente = request.form

    if validar_datos_cliente(datos_cliente):
        try:
            db_connection, cursor = conectar_bd()
            sql = "INSERT INTO cliente (id_cliente, tipo_identificacion, numero_identificacion, nombre_completo, email, direccion, telefono) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (datos_cliente['id_cliente'], datos_cliente['tipo_identificacion'], datos_cliente['numero_identificacion'], datos_cliente['nombre_completo'], datos_cliente['email'], datos_cliente['direccion'], datos_cliente['telefono']))
            db_connection.commit()
            cursor.close()
            db_connection.close()
            return redirect(url_for('mostrar_clientes'))
        except Exception as e:
            mensaje_error = f"Error al guardar el cliente: {str(e)}"
            return render_template("mensaje.html", message=mensaje_error)
    else:
        mensaje_error = "Por favor, complete todos los campos obligatorios."
        return render_template("mensaje.html", message=mensaje_error)

# Ruta para eliminar un cliente
@app.route('/deleteCliente/<string:id_cliente>')
def eliminar_cliente(id_cliente):
    try:
        db_connection, cursor = conectar_bd()
        sql = "DELETE FROM cliente WHERE id_cliente = %s"
        cursor.execute(sql, (id_cliente,))
        db_connection.commit()
        cursor.close()
        db_connection.close()
        return redirect(url_for('mostrar_clientes'))
    except Exception as e:
        mensaje_error = f"Error al eliminar el cliente: {str(e)}"
        return render_template("mensaje.html", message=mensaje_error)

if __name__ == "__main__":
    app.run(debug=True)
