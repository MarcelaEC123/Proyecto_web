from flask import Flask, request, render_template, redirect, url_for
import database as db

app = Flask(__name__, template_folder="C:\\Users\\lenovo\\OneDrive\\Desktop\\UNIAGUSTINIANA\\Proyecto\\Proyecto_web\\aplicativo_pos_hc\\aplicativo_pos_hc\\templates")

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
# Ruta para caja
@app.route("/caja")
def caja():
     db_connection, cursor = db.conectar_bd()
     cursor.execute("SELECT * FROM venta")
     myresult = cursor.fetchall()
     #convertir datos a diccionary 
     insertObjec = []
     columnNames = [column[0] for column in cursor.description]
     for record in myresult:
            insertObjec.append(dict(zip(columnNames, record)))
     cursor.close()   
     return render_template("caja.html", data=insertObjec)
 
#Ruta para guardar VENTAS
@app.route('/guardarVenta', methods=['POST'])
def addGuardarVenta():    
     id_venta = request.form['id_venta']
     codigo = request.form['codigo']
     descripcion = request.form['descripcion']
     valor_unitario = request.form['valor_unitario']
     medio_pago = request.form['medio_pago']
     descuento = request.form['descuento']
     id_cliente = request.form['id_cliente']
     cantidad = request.form['cantidad']
     iva = request.form['iva']
     total_a_pagar = request.form['total_a_pagar']
     fecha_registro = request.form['fecha_registro']
     observaciones = request.form['observaciones']
     

     if id_venta and codigo and descripcion and valor_unitario and medio_pago and descuento and id_cliente and cantidad and iva and total_a_pagar and fecha_registro and observaciones:
        db_connection, cursor = db.conectar_bd()
        sql = "INSERT INTO venta (id_venta,codigo,descripcion,valor_unitario,medio_pago,descuento,id_cliente,cantidad,iva,total_a_pagar,fecha_registro,observaciones) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        data = (id_venta,codigo,descripcion,valor_unitario,medio_pago,descuento,id_cliente,cantidad,iva,total_a_pagar,fecha_registro,observaciones,)
        cursor.execute(sql, data)
        db_connection.commit()
        cursor.close()
        db_connection.close()
     return redirect(url_for('caja'))

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
  
#Ruta para guardar productos
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

@app.route("/editar_producto/<int:id_producto>", methods=["GET", "POST"])
def editar_producto(id_producto):
    if request.method == "POST":
        # Obtener los datos del formulario de edición
        print("Datos del formulario:", request.form)
        codigo = request.form['codigo']
        descripcion = request.form['descripcion']
        categoria = request.form['categoria']
        proveedor = request.form['proveedor']
        valorUnitario = request.form['valor_unitario']
        unidadMedida = request.form['unidad_medida']
        
        # Imprimir los datos obtenidos del formulario para depurar
        print("Datos del formulario recibidos:", codigo, descripcion, categoria, proveedor, valorUnitario, unidadMedida)
        
        # Actualizar los detalles del producto en la base de datos
        db_connection, cursor = db.conectar_bd()
        sql = """UPDATE producto SET codigo = %s, descripcion = %s, categoria = %s, proveedor = %s, 
                 valor_unitario = %s, unidad_medida = %s WHERE id_producto = %s"""
        data = (codigo, descripcion, categoria, proveedor, valorUnitario, unidadMedida, id_producto)
        cursor.execute(sql, data)
        db_connection.commit()
        cursor.close()
        db_connection.close()
        
        return redirect(url_for('productos'))
    else:
        # Obtener los detalles del producto a editar
        db_connection, cursor = db.conectar_bd()
        cursor.execute("SELECT * FROM producto WHERE id_producto = %s", (id_producto,))
        producto = cursor.fetchone()
        cursor.close()
        db_connection.close()
        
        # Imprimir los detalles del producto para depurar
        print("Detalles del producto a editar:", producto)
        
        return render_template("editar_producto.html", producto=producto)

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


