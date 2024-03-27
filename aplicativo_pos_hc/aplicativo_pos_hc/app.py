from flask import Flask, request, render_template, redirect, url_for
import database as db

app = Flask(__name__, template_folder="C:\\Users\\lenovo\\OneDrive\\Desktop\\UNIAGUSTINIANA\\Proyecto\\Proyecto_web\\aplicativo_pos_hc\\aplicativo_pos_hc\\templates")

# # Función para conectar a la base de datos y crear un cursor
# def conectar_bd():
#     db = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="SQLMARCE2022.",
#         database="Aplicativo_POS_final"
#     )
#     cursor = db.cursor()
#     return db, cursor

# Ruta para la página de inicio
@app.route("/")
def index():
    return render_template("home.html")

# Ruta para el inicio de sesión
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    try:
        # Conectar a la base de datos y crear un cursor
        db_connection, cursor = db.conectar_bd()

        # Consulta SQL para verificar las credenciales de inicio de sesión
        query = "SELECT * FROM usuarios WHERE Usuario = %s AND Contrasenia = %s"
        cursor.execute(query, (username, password))

        # Leer y procesar los resultados de la consulta
        user = cursor.fetchone()

        # Cerrar el cursor y la conexión
        cursor.close()
        db_connection.close()

        # Procesar los resultados de la consulta
        if user:
            # Redirigir al usuario a la página principal si el inicio de sesión es exitoso
            return redirect(url_for("principal"))
        else:
            # Si las credenciales son incorrectas, renderizar la plantilla de mensaje de error
            error_message = "Credenciales incorrectas"
            return render_template("mensaje.html", message=error_message)

    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir durante la ejecución de la consulta
        error_message = "Error al procesar la solicitud: {}".format(str(e))
        return render_template("mensaje.html", message=error_message)


# Ruta para la página principal
@app.route("/principal")
def principal():
    return render_template("principal.html")

# Ruta para cerrar sesión
@app.route("/logout")
def logout():
    # Realiza cualquier limpieza necesaria para cerrar sesión
    # Luego redirecciona al usuario a la página de inicio
    return redirect(url_for("index"))  # Aquí cambiamos "home" a "index"

# Rutas para otras páginas

@app.route("/caja")
def caja():
    return render_template("caja.html")

@app.route("/clientes")
def clientes():
    return render_template("clientes.html")

@app.route("/proveedores")
def proveedores():
    return render_template("proveedores.html")

@app.route("/productos")
def productos():
     db_connection, cursor = db.conectar_bd()
     cursor.execute("SELECT * FROM producto")
     myresult = cursor.fetchall()
     #convertir datos a diccionary 
     insertObjec = []
     columnNames = [column[0] for column in cursor.description]
     for record in myresult:
            insertObjec.append(dict(zip(columnNames, record)))
     cursor.close()   
     return render_template("productos.html", data=insertObjec)
  
#Ruta para guardar usuarios
@app.route('/guardar', methods=['POST'])
def addGuardar():    
     id_producto = request.form['id_producto']
     codigo = request.form['codigo']
     descripcion = request.form['descripcion']
     categoria = request.form['categoria']
     proveedor = request.form['proveedor']
     valorUnitario = request.form['valor_unitario']
     unidadMedida = request.form['unidad_medida']

     if id_producto and codigo and descripcion and categoria and proveedor and valorUnitario and unidadMedida:
        db_connection, cursor = db.conectar_bd()
        sql = "INSERT INTO producto (id_producto,codigo,descripcion,categoria,proveedor,valor_unitario,unidad_medida) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        data = (id_producto,codigo,descripcion,categoria,proveedor,valorUnitario,unidadMedida)
        cursor.execute(sql, data)
        db_connection.commit()
        cursor.close()
        db_connection.close()
     return redirect(url_for('productos'))

#Ruta para eliminar
@app.route('/delete/<string:id_producto>')
def delete(id_producto):
        cursor = db.database.cursor()
        sql = "DELETE FROM producto WHERE id_producto = %s)"
        data = (id_producto,)
        cursor.execute(sql, data)
        db.database.commit() 
        return redirect(url_for('productos'))

#Ruta para editor
@app.route('/edit/<string:id_producto>', methods=['POST'])
def edit(id_producto):
     id_producto = request.form['id_producto']
     codigo = request.form['codigo']
     categoria = request.form['categoria']
     proveedor = request.form['proveedor']
     valorUnitario = request.form['valor_unitario']
     unidadMedida = request.form['unidad_medida']
     
     if id_producto and codigo and categoria and proveedor and valorUnitario and unidadMedida:
        cursor = db.database.cursor()
        sql = "UPDATE producto SET codigo = %s, categoria = %s, proveedor = %s,valor_unitario  = %s,unidad_medida = %s WHERE id_producto = %s"
        data = (codigo,categoria,proveedor,valorUnitario,unidadMedida,id_producto)
        cursor.execute(sql, data)
        db.database.commit()
     return redirect(url_for('productos'))


@app.route("/compras")
def compras():
    return render_template("compras.html")

@app.route("/venta_historico")
def venta_historico():
    return render_template("ventaHistorico.html")

@app.route("/registro")
def registro():
    return render_template("registro.html")


if __name__ == "__main__":
    app.run(debug=True)


