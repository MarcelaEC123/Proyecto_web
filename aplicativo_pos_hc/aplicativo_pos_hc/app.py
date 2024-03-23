# Importamos el módulo redirect
from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__, template_folder="C:\\Users\\lenovo\\OneDrive\\Desktop\\UNIAGUSTINIANA\\Proyecto\\Proyecto_web\\aplicativo_pos_hc\\aplicativo_pos_hc\\templates")

# Conexión a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="SQLMARCE2022.",
    database="Aplicativo_POS_final"
)

# Verifica si la conexión a la base de datos fue exitosa
if db.is_connected():
    print("Conexión exitosa a la base de datos")

cursor = db.cursor()

# Ruta para la página de inicio
@app.route("/")
def index():
    return render_template("home.html")

# Ruta para el inicio de sesión
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Consulta SQL para verificar las credenciales de inicio de sesión
    query = "SELECT * FROM usuarios WHERE Usuario = %s AND Contrasenia = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    # Verifica si se encontró un usuario con las credenciales proporcionadas
    if user:
        # Redirigir al usuario a la página principal si el inicio de sesión es exitoso
        return redirect(url_for("principal"))
    else:
        # Si las credenciales son incorrectas, renderiza la plantilla de mensaje de error
        return render_template("mensaje.html", message="Credenciales incorrectas")

# Ruta para la página principal
@app.route("/principal")
def principal():
    return render_template("principal.html")

# Ruta para cerrar sesión
@app.route("/logout")
def logout():
    # Realiza cualquier limpieza necesaria para cerrar sesión
    # Luego redirecciona al usuario a la página de inicio
    return redirect(url_for("index"))  # Cambiado "home" a "index"

if __name__ == "__main__":
    app.run(debug=True)
