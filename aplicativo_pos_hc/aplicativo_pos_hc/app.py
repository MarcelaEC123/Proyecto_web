from flask import Flask, request, render_template, redirect, url_for
import database as db

app = Flask(__name__, template_folder="C:\\Users\\cindy\\OneDrive\\Escritorio\\Proyecto de GRADO\\Proyecto_web\\aplicativo_pos_hc\\aplicativo_pos_hc\\templates")

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
        db_connection, cursor = db.conectar_bd()
        # Consulta SQL para verificar las credenciales de inicio de sesión
        query = "SELECT * FROM usuarios WHERE Usuario = %s AND Contrasenia = %s"
        cursor.execute(query, (username, password))
        # Leer y procesar los resultados de la consulta
        user = cursor.fetchone()
        # Cerrar el cursor y la conexión
        cursor.close()
        db_connection.close()
        if user:
            return redirect(url_for("principal"))
        else:
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
    return redirect(url_for("index"))

@app.route("/caja")
def caja():
    try:
        db_connection, cursor = db.conectar_bd()
        
        # Obtener el próximo valor autoincremental de id_venta
        cursor.execute("SHOW TABLE STATUS LIKE 'venta'")
        table_status = cursor.fetchone()
        if table_status is not None:
            next_id = table_status[10]  # El índice 10 corresponde a la columna Auto_increment
            
            # Contar la cantidad de registros
            cursor.execute("SELECT COUNT(*) FROM venta")
            count = cursor.fetchone()[0]
            if count == 0:
                next_id = 1  # Si no hay registros, comenzar desde 1
            else:
                # Obtener el último ID y ajustar para el siguiente ID
                cursor.execute("SELECT MAX(id_venta) FROM venta")
                last_id = cursor.fetchone()[0]
                next_id = last_id + 1
                
            # Generar el nuevo código de factura
            cursor.execute("SELECT MAX(id_factura) FROM venta")
            last_code = cursor.fetchone()[0]
            if last_code is not None:
                new_code = str(int(last_code) + 1).zfill(7)  # Incrementar el último código y rellenar con ceros
            else:
                new_code = "0000001"  # Si no hay códigos en la base de datos, iniciar desde "0000001"

            
            # Obtener los productos existentes
            cursor.execute("SELECT * FROM venta")
            myresult = cursor.fetchall()
            
            # Convertir datos a diccionario
            insertObjects = []
            columnNames = [column[0] for column in cursor.description]
            for record in myresult:
                insertObjects.append(dict(zip(columnNames, record)))
                
            cursor.close()
            return render_template("caja.html", data=insertObjects, next_id=next_id, new_code=new_code)
        else:
            return "No se pudo obtener información de la tabla 'venta'"
    except Exception as e:
        # Manejar cualquier excepción que ocurra
        return f"Error: {str(e)}"

#Ruta para guardar VENTAS
@app.route('/guardarVenta', methods=['POST'])
def addGuardarVenta():    
     id_venta = request.form['id_venta']
     id_factura= request.form['id_factura']
     nombre_proveedor = request.form['nombre_proveedor']
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
     
     if id_venta and id_factura and  nombre_proveedor and descripcion and valor_unitario and medio_pago and descuento and id_cliente and cantidad and iva and total_a_pagar and fecha_registro and observaciones:
        db_connection, cursor = db.conectar_bd()
        sql = "INSERT INTO venta (id_venta,id_factura, nombre_proveedor,descripcion,valor_unitario,medio_pago,descuento,id_cliente,cantidad,iva,total_a_pagar,fecha_registro,observaciones) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        data = (id_venta,id_factura,nombre_proveedor,descripcion,valor_unitario,medio_pago,descuento,id_cliente,cantidad,iva,total_a_pagar,fecha_registro,observaciones,)
        cursor.execute(sql, data)
        db_connection.commit()
        cursor.close()
        db_connection.close()
     return redirect(url_for('caja'))

@app.route('/deleteVenta/<string:id_venta>')
def deleteVenta(id_venta):
    try:
        # Conectar a la base de datos y crear un cursor
        db_connection, cursor = db.conectar_bd()

        # Definir la consulta SQL para eliminar la venta por su ID
        sql = "DELETE FROM venta WHERE id_venta = %s"

        # Ejecutar la consulta SQL con los datos proporcionados
        cursor.execute(sql, (id_venta,))

        # Confirmar los cambios en la base de datos
        db_connection.commit()

        # Cerrar el cursor y la conexión
        cursor.close()
        db_connection.close()

        # Redirigir al usuario de vuelta a la página de caja después de eliminar la venta
        return redirect(url_for('caja'))

    except Exception as e:
        # Manejar cualquier excepción que ocurra durante el proceso
        # Imprimir el error para fines de depuración
        print("Error al eliminar la venta:", e)
        # Si hay un error, deshacer cualquier cambio pendiente y cerrar la conexión
        db_connection.rollback()
        cursor.close()
        db_connection.close()
        # Redirigir al usuario a una página de error o volver a cargar la página actual
        # Puedes personalizar esta parte según tu aplicación
        return "Error al eliminar la venta. Por favor, inténtalo de nuevo más tarde."

@app.route("/generar_ticket/<int:id_venta>")
def generar_ticket(id_venta):
    # Conectar a la base de datos y crear un cursor
    db_connection, cursor = db.conectar_bd()

    # Ejecutar la consulta SQL para seleccionar los registros relevantes de la tabla de ventas
    cursor.execute("SELECT cantidad, descripcion, valor_unitario ,id_factura,fecha_registro FROM venta WHERE id_venta = %s", (id_venta,))
    
    # Obtener los resultados de la consulta
    venta_data = cursor.fetchall()

    # Imprimir los datos de la venta para depuración
    print("Datos de la venta:", venta_data)

    # Cerrar el cursor y la conexión
    cursor.close()
    db_connection.close()
    
    # Renderizar la plantilla HTML con los datos recuperados
    return render_template("factura.html", productos=venta_data)

@app.route("/clientes")
def clientes():
    db_connection, cursor = db.conectar_bd()
    
    # Obtener el próximo valor autoincremental de id_producto
    cursor.execute("SHOW TABLE STATUS LIKE 'clientes'")
    table_status = cursor.fetchone()
    next_id = table_status[10]  # El índice 10 corresponde a la columna Auto_increment
    
    # Contar la cantidad de registros
    cursor.execute("SELECT COUNT(*) FROM clientes")
    count = cursor.fetchone()[0]
    if count == 0:
        next_id = 1  # Si no hay registros, comenzar desde 1
    else:
        # Obtener el último ID y ajustar para el siguiente ID
        cursor.execute("SELECT MAX(id_cliente) FROM clientes")
        last_id = cursor.fetchone()[0]
        next_id = last_id + 1
    
    # Obtener los productos existentes
    cursor.execute("SELECT * FROM clientes")
    myresult = cursor.fetchall()
    # Convertir datos a diccionario
    insertObjec = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObjec.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template("clientes.html", data=insertObjec, next_id=next_id)

#Ruta para guardar CLIENTES
@app.route('/guardarClientes', methods=['POST'])
def addGuardarClientes():    
     id_cliente = request.form['id_cliente']
     tipo_identificacion = request.form['tipo_identificacion']
     numero_identificacion = request.form['numero_identificacion']
     nombre_completo = request.form['nombre_completo']
     email = request.form['email']
     direccion = request.form['direccion']
     telefono = request.form['telefono']
    
     if id_cliente and tipo_identificacion and numero_identificacion and nombre_completo and  email and direccion and  telefono :
        db_connection, cursor = db.conectar_bd()
        sql = "INSERT INTO clientes (id_cliente,tipo_identificacion,numero_identificacion,nombre_completo, email,direccion, telefono) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        data = (id_cliente,tipo_identificacion,numero_identificacion,nombre_completo,email,direccion,telefono)
        cursor.execute(sql, data)
        db_connection.commit()
        cursor.close()
        db_connection.close()
     return redirect(url_for('clientes'))

@app.route('/deleteCliente/<string:id_cliente>')
def deleteCliente (id_cliente):
        db_connection, cursor = db.conectar_bd()
        sql = "DELETE FROM clientes WHERE id_cliente=%s"
        data = (id_cliente,)
        cursor.execute(sql, data)
        db_connection.commit()
        cursor.close()
        db_connection.close()
        return redirect(url_for('clientes'))

@app.route("/proveedores")
def proveedores():
    db_connection, cursor = db.conectar_bd()
    
        # Obtener el próximo valor autoincremental de id_producto
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
    
    # Obtener los productos existentes
    cursor.execute("SELECT * FROM proveedor")
    myresult = cursor.fetchall()
    # Convertir datos a diccionario
    insertObjec = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObjec.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template("proveedores.html", data=insertObjec, next_id=next_id)

#Ruta para guardar PROVEEDORES
@app.route('/guardarProveedores', methods=['POST'])
def addGuardarPreveedores():    
     id_proveedor = request.form['id_proveedor']
     tipo_identificacion = request.form['tipo_identificacion']
     numero_identificacion = request.form['numero_identificacion']
     nombre_proveedor = request.form['nombre_proveedor']
     email = request.form['email']
     direccion = request.form['direccion']
     telefono = request.form['telefono']
     dia_de_visita = request.form['dia_de_visita']
     dia_de_entrega = request.form['dia_de_entrega']
    
     if id_proveedor and tipo_identificacion and numero_identificacion and nombre_proveedor  and  email and direccion and  telefono and dia_de_visita and dia_de_entrega:
        db_connection, cursor = db.conectar_bd()
        sql = "INSERT INTO proveedor (id_proveedor,tipo_identificacion,numero_identificacion, nombre_proveedor , email,direccion, telefono , dia_de_visita, dia_de_entrega) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        data = (id_proveedor,tipo_identificacion,numero_identificacion, nombre_proveedor ,email,direccion,telefono,dia_de_visita,dia_de_entrega)
        cursor.execute(sql, data)
        db_connection.commit()
        cursor.close()
        db_connection.close()
     return redirect(url_for('proveedores'))

@app.route('/deleteProveedor/<string:id_proveedor>')
def deleteProveedor (id_proveedor):
        db_connection, cursor = db.conectar_bd()
        sql = "DELETE FROM proveedor WHERE id_proveedor=%s"
        data = (id_proveedor,)
        cursor.execute(sql, data)
        db_connection.commit()
        cursor.close()
        db_connection.close()
        return redirect(url_for('proveedores'))

#Ruta para guardar PRODUCTOS
@app.route("/productos")
def productos():
    db_connection, cursor = db.conectar_bd()
    
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
    if last_code:
        new_code = str(int(last_code) + 1).zfill(4)  # Incrementar el último código y rellenar con ceros
    else:
        new_code = "0001"  # Si no hay códigos en la base de datos, iniciar desde "0001"
    # Obtener los productos existentes
    cursor.execute("SELECT * FROM producto")
    myresult = cursor.fetchall()
    # Convertir datos a diccionario
    insertObjec = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObjec.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template("productos.html", data=insertObjec, next_id=next_id, new_code=new_code)

# Ruta para guardar productos
@app.route('/guardar', methods=['POST'])
def addGuardar():    
     codigo = request.form['codigo']
     descripcion = request.form['descripcion']
     categoria = request.form['categoria']
     nombre_proveedor = request.form['nombre_proveedor']
     stock = request.form['stock']
     valorUnitario = request.form['valor_unitario']
     unidadMedida = request.form['unidad_medida']

     if codigo and descripcion and categoria and nombre_proveedor and stock and valorUnitario and unidadMedida:
        db_connection, cursor = db.conectar_bd()
        sql = "INSERT INTO producto (codigo,descripcion,categoria,nombre_proveedor,stock,valor_unitario,unidad_medida) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        data = (codigo,descripcion,categoria,nombre_proveedor,stock,valorUnitario,unidadMedida)
        cursor.execute(sql, data)
        db_connection.commit()
    
        cursor.close()
        db_connection.close()
    
     return redirect(url_for('productos'))

# Ruta para agregar stock
@app.route('/addStock', methods=['POST'])
def addStock():
    id_producto = request.form['id_producto']
    cantidad = request.form['cantidad']

    if id_producto and cantidad:
        db_connection, cursor = db.conectar_bd()
        # Obtener el stock actual del producto
        cursor.execute("SELECT stock FROM producto WHERE id_producto = %s", (id_producto,))
        stock_actual = cursor.fetchone()[0]

        # Sumar la cantidad proporcionada al stock actual
        nuevo_stock = stock_actual + int(cantidad)

        # Actualizar el stock en la base de datos
        cursor.execute("UPDATE producto SET stock = %s WHERE id_producto = %s", (nuevo_stock, id_producto))  # Corregido aquí
        db_connection.commit()

        cursor.close()
        db_connection.close()

    return redirect(url_for('productos'))


@app.route('/deleteProducto/<string:id_producto>')
def delete (id_producto):
        db_connection, cursor = db.conectar_bd()
        sql = "DELETE FROM producto WHERE id_producto=%s"
        data = (id_producto,)
        cursor.execute(sql, data)
        db_connection.commit()
        cursor.close()
        db_connection.close()
        return redirect(url_for('productos'))

@app.route('/editar_producto/<string:id_producto>', methods=['POST'])
def editar(id_producto):
    codigo = request.form['codigo']
    descripcion = request.form['descripcion']
    categoria = request.form['categoria']
    nombre_proveedor = request.form[' nombre_proveedor']
    stock = request.form['stock']
    valorUnitario = request.form['valor_unitario']
    unidadMedida = request.form['unidad_medida']
        
    if codigo and descripcion and categoria and nombre_proveedor and stock and valorUnitario and unidadMedida:
        db_connection, cursor = db.conectar_bd()
        sql = "UPDATE producto SET codigo = %s, descripcion = %s, categoria = %s, nombre_proveedor= %s,stock= %s, valor_unitario = %s, unidad_medida = %s WHERE id_producto = %s"
        data = (codigo, descripcion, categoria,  nombre_proveedor,stock, valorUnitario, unidadMedida, id_producto)
        cursor.execute(sql, data)
        db_connection.commit()
        cursor.close()
        db_connection.close()
    return redirect(url_for('productos'))

# Ruta para mostrar usuarios
@app.route("/usuarios")
def usuarios():
    db_connection, cursor = db.conectar_bd()
    
    # Obtener el último ID insertado antes de eliminar registros
    cursor.execute("SELECT MAX(id_usuario) FROM usuarios")
    last_id = cursor.fetchone()[0]

    # Calcular el próximo ID
    if last_id is None:
        next_id = 1
    else:
        next_id = last_id + 1
    
    # Obtener los usuarios existentes
    cursor.execute("SELECT * FROM usuarios")
    myresult = cursor.fetchall()
    
    # Convertir datos a diccionario
    insertObjec = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObjec.append(dict(zip(columnNames, record)))
    
    cursor.close()
    
    return render_template("usuarios.html", data=insertObjec, next_id=next_id)

# Ruta para guardar usuarios
@app.route('/guardarUsuario', methods=['POST'])
def addGuardarUsuario():    
    nombre = request.form['nombre']
    tipo_Identificacion = request.form['tipo_Identificacion']
    numero_identificacion = request.form['numero_identificacion']
    telefono = request.form['telefono']
    email = request.form['email']
    usuario = request.form['usuario']
    contrasenia = request.form['contrasenia']
    tipo_usuario = request.form['tipo_usuario']

    if nombre and tipo_Identificacion and numero_identificacion and telefono and email and usuario and contrasenia and tipo_usuario:
        # Conectar a la base de datos
        db_connection, cursor = db.conectar_bd()

        # Obtener el último ID insertado antes de eliminar registros
        cursor.execute("SELECT MAX(id_usuario) FROM usuarios")
        last_id = cursor.fetchone()[0]

        # Calcular el próximo ID
        if last_id is None:
            next_id = 1
        else:
            next_id = last_id + 1

        # Insertar el nuevo usuario en la tabla usuarios
        sql = "INSERT INTO usuarios (id_usuario, nombre, tipo_Identificacion, numero_identificacion, telefono, email, usuario, contrasenia, tipo_usuario) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (next_id, nombre, tipo_Identificacion, numero_identificacion, telefono, email, usuario, contrasenia, tipo_usuario)
        cursor.execute(sql, data)
        db_connection.commit()

        # Cerrar la conexión
        cursor.close()
        db_connection.close()

    return redirect(url_for('usuarios'))

@app.route('/deleteUsuarios/<string:id_usuario>')
def deleteUsuarios(id_usuario):
        db_connection, cursor = db.conectar_bd()
        sql = "DELETE FROM usuarios WHERE id_usuario=%s"
        data = (id_usuario,)
        cursor.execute(sql, data)
        db_connection.commit()
        cursor.close()
        db_connection.close()
        return redirect(url_for('usuarios'))

if __name__ == "__main__":
    app.run(debug=True)


