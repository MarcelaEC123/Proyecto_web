from flask import Flask, request, render_template, redirect, url_for
from database import conectar_bd

app = Flask(__name__)

# Ruta para mostrar la página de usuarios
@app.route("/usuarios")
def usuarios():
    db_connection, cursor = conectar_bd()

    # Obtener el último ID insertado antes de eliminar registros
    cursor.execute("SELECT MAX(id_usuario) FROM usuario")
    last_id = cursor.fetchone()[0]

    # Calcular el próximo ID
    if last_id is None:
        next_id = 1
    else:
        next_id = last_id + 1

    # Obtener los usuarios existentes
    cursor.execute("SELECT * FROM usuario")
    usuarios = [dict(zip(cursor.column_names, row)) for row in cursor.fetchall()]

    cursor.close()
    db_connection.close()

    return render_template("usuarios.html", usuarios=usuarios, next_id=next_id)

# Ruta para guardar usuarios
@app.route('/guardarUsuario', methods=['POST'])
def guardar_usuario():
    datos_usuario = request.form

    if validar_datos_usuario(datos_usuario):
        try:
            db_connection, cursor = conectar_bd()

            # Obtener el último ID insertado antes de eliminar registros
            cursor.execute("SELECT MAX(id_usuario) FROM usuario")
            last_id = cursor.fetchone()[0]

            # Calcular el próximo ID
            if last_id is None:
                next_id = 1
            else:
                next_id = last_id + 1

            # Insertar el nuevo usuario en la tabla usuarios
            sql = "INSERT INTO usuario (id_usuario, nombre, tipo_Identificacion, numero_identificacion, telefono, email, usuario, contrasenia, tipo_usuario) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (next_id, datos_usuario['nombre'], datos_usuario['tipo_Identificacion'], datos_usuario['numero_identificacion'], datos_usuario['telefono'], datos_usuario['email'], datos_usuario['usuario'], datos_usuario['contrasenia'], datos_usuario['tipo_usuario'])
            cursor.execute(sql, data)
            db_connection.commit()

            cursor.close()
            db_connection.close()

            return redirect(url_for('usuarios'))
        except Exception as e:
            mensaje_error = f"Error al guardar el usuario: {str(e)}"
            return render_template("mensaje.html", message=mensaje_error)
    else:
        mensaje_error = "Por favor, complete todos los campos obligatorios."
        return render_template("mensaje.html", message=mensaje_error)

# Ruta para eliminar un usuario
@app.route('/deleteUsuario/<string:id_usuario>')
def eliminar_usuario(id_usuario):
    try:
        db_connection, cursor = conectar_bd()
        sql = "DELETE FROM usuario WHERE id_usuario = %s"
        cursor.execute(sql, (id_usuario,))
        db_connection.commit()
        cursor.close()
        db_connection.close()
        return redirect(url_for('usuarios'))
    except Exception as e:
        mensaje_error = f"Error al eliminar el usuario: {str(e)}"
        return render_template("mensaje.html", message=mensaje_error)

# Ruta para editar un usuario
@app.route('/editarUsuario', methods=['POST'])
def editar_usuario():
    datos_usuario = request.form

    if validar_datos_usuario(datos_usuario):
        try:
            db_connection, cursor = conectar_bd()
            sql = "UPDATE usuario SET nombre = %s, tipo_Identificacion = %s, numero_identificacion = %s, telefono = %s, email = %s, usuario = %s, contrasenia = %s, tipo_usuario = %s WHERE id_usuario = %s"
            data = (datos_usuario['nombre'], datos_usuario['tipo_Identificacion'], datos_usuario['numero_identificacion'], datos_usuario['telefono'], datos_usuario['email'], datos_usuario['usuario'], datos_usuario['contrasenia'], datos_usuario['tipo_usuario'], datos_usuario['id_usuario'])
            cursor.execute(sql, data)
            db_connection.commit()
            cursor.close()
            db_connection.close()
            return redirect(url_for('usuarios'))
        except Exception as e:
            mensaje_error = f"Error al editar el usuario: {str(e)}"
            return render_template("mensaje.html", message=mensaje_error)
    else:
        mensaje_error = "Por favor, complete todos los campos obligatorios."
        return render_template("mensaje.html", message=mensaje_error)

# Función para validar los datos del formulario de usuario
def validar_datos_usuario(datos_usuario):
    campos_obligatorios = ['nombre', 'tipo_Identificacion', 'numero_identificacion', 'telefono', 'email', 'usuario', 'contrasenia', 'tipo_usuario']
    for campo in campos_obligatorios:
        if not datos_usuario.get(campo):
            return False
    return True

if __name__ == "__main__":
    app.run(debug=True)
