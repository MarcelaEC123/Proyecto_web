from flask import Blueprint, render_template, request, redirect, url_for, session
from database import db  # Importa la instancia de la base de datos desde database.py

auth_bp = Blueprint('auth', __name__)

# Ruta para el inicio de sesión
@auth_bp.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    try:
        # Consulta SQL para verificar las credenciales de inicio de sesión
        query = "SELECT * FROM usuario WHERE Usuario = %s AND Contrasenia = %s"
        with db.connect() as conn:  # Utiliza la conexión a la base de datos
            result = conn.execute(query, (username, password))
            user = result.fetchone()

        if user:
            # Guardar el usuario en la sesión
            session['user'] = user
            return redirect(url_for("principal"))
        else:
            error_message = "Credenciales incorrectas"
            return render_template("mensaje.html", message=error_message)

    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir durante la ejecución de la consulta
        error_message = "Error al procesar la solicitud: {}".format(str(e))
        return render_template("mensaje.html", message=error_message)

# Ruta para la página principal
@auth_bp.route("/principal")
def principal():
    user = session.get('user')
    if user:
        # Renderizar la plantilla principal con los datos del usuario
        return render_template("principal.html", user=user)
    else:
        return redirect(url_for("auth.login"))  # Redirigir al inicio de sesión si no hay usuario en la sesión

# Ruta para cerrar sesión
@auth_bp.route("/logout")
def logout():
    session.pop('user', None)  # Eliminar el usuario de la sesión
    return redirect(url_for("auth.login"))

# Otras rutas y funciones de autenticación...
