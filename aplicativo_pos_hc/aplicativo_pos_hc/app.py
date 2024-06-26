from flask import Flask, request, render_template, redirect, session, url_for
from venta import obtener_detalles_de_venta
from flask import jsonify
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usuario:contraseña@localhost/nombre_base_de_datos'
db = SQLAlchemy(app)

import database as db

app = Flask(__name__, template_folder="C:\\Users\\cindy\\OneDrive\\Escritorio\\Proyecto de GRADO\\Proyecto_web\\aplicativo_pos_hc\\aplicativo_pos_hc\\templates")

from flask import Flask
from usuarios import usuarios
from productos import productos
from proveedores import proveedores
from registro import ventas
from auth import auth

app = Flask(__name__)

# Registrar los blueprints de los diferentes módulos
app.register_blueprint(usuarios)
app.register_blueprint(productos)
app.register_blueprint(proveedores)
app.register_blueprint(ventas)
app.register_blueprint(auth)
"""# Ruta para la página de inicio
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
        query = "SELECT * FROM usuario WHERE Usuario = %s AND Contrasenia = %s"
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
    return redirect(url_for("index"))"""


"""@app.route("/caja")
def caja():
    try:
        db_connection, cursor = db.conectar_bd()
        
        # Obtener el próximo valor autoincremental de id_venta
        cursor.execute("SHOW TABLE STATUS LIKE 'venta'")
        table_status = cursor.fetchone()
        if table_status is not None:
            next_id = table_status[10] if table_status[10] else 1
            
            # Generar el nuevo código de factura
            cursor.execute("SELECT MAX(id_factura) FROM venta")
            last_code = cursor.fetchone()[0]
            new_code = str(int(last_code) + 1).zfill(7) if last_code else "0000001"

            # Obtener los productos existentes
            cursor.execute("SELECT * FROM venta")
            insertObjects = [dict(zip([column[0] for column in cursor.description], record)) for record in cursor.fetchall()]

            cursor.close()
            return render_template("caja.html", data=insertObjects, next_id=next_id, new_code=new_code)
        else:
            return "No se pudo obtener información de la tabla 'venta'"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/guardarVenta', methods=['POST'])
def add_guardar_venta():    
    try:
        id_venta = request.form['id_venta']
        id_factura = request.form['id_factura']  
        medio_pago = request.form['medio_pago']
        descuento = request.form['descuento']
        iva = request.form['iva']
        fecha_registro = request.form['fecha_registro']
        total_a_pagar = request.form['total_a_pagar']
        id_cliente = request.form['id_cliente']
        
        if id_venta and id_factura and medio_pago and descuento and iva and fecha_registro and total_a_pagar and id_cliente:
            db_connection, cursor = db.conectar_bd()
            sql_venta = "INSERT INTO venta (id_venta, id_factura, medio_pago, descuento, iva, fecha_registro, total_a_pagar, id_cliente) VALUES (%s,  %s, %s, %s, %s, %s,%s,  %s)"
            data_venta = (id_venta, id_factura, medio_pago, descuento, iva, fecha_registro, total_a_pagar, id_cliente)
            cursor.execute(sql_venta, data_venta)
            
            db_connection.commit()
            cursor.close()
            db_connection.close()
            return redirect(url_for('caja'))
        else:
            return "Por favor, complete todos los campos."
    except Exception as e:
        return f"Error al guardar la venta: {str(e)}"

@app.route('/delete_venta/<string:id_venta>')
def delete_venta(id_venta):
    try:
        db_connection, cursor = db.conectar_bd()
        sql = "DELETE FROM venta WHERE id_venta = %s"
        cursor.execute(sql, (id_venta,))
        db_connection.commit()
        cursor.close()
        db_connection.close()
        return redirect(url_for('caja'))
    except Exception as e:
        print("Error al eliminar la venta:", e)
        return "Error al eliminar la venta. Por favor, inténtalo de nuevo más tarde."

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    try:
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        valor_unitario = request.form['precio']

        success = db.actualizar_detalle_venta(1, descripcion, cantidad, valor_unitario, 1, 1)  

        if success:
            return jsonify({'success': True, 'message': 'Producto agregado correctamente.'})
        else:
            return jsonify({'success': False, 'message': 'Error al agregar el producto.'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})
    # Esta función simula la obtención de datos de venta desde alguna fuente
# Esta función simula la obtención de datos de venta desde alguna fuente


@app.route('/ruta_para_mostrar_detalle_de_venta')
def mostrar_detalle_de_venta():
    venta = obtener_datos_de_venta()  # Obtener los datos de venta
    return render_template('caja.html', venta=venta)

def obtener_detalles_de_venta_desde_la_base_de_datos(id_venta):
    try:
        # Consulta la venta por su ID utilizando SQLAlchemy
        venta = venta.query.get(id_venta)
        return venta
    except Exception as e:
        print(f"Error al obtener los detalles de la venta: {str(e)}")
        return None

@app.route('/detalle_venta/<int:id_venta>')
def detalle_venta(id_venta):
    venta = obtener_datos_de_venta(id_venta)
    
    if venta:
        return render_template('detalle_venta.html', venta=venta)
    else:
        return render_template('venta_no_encontrada.html')

def obtener_datos_de_venta(id_venta):
    try:
        # Lógica para obtener los detalles de la venta con el ID proporcionado
        venta = ...  # Implementa aquí tu lógica para obtener los detalles de la venta
        return venta
    except Exception as e:
        print(f"Error al obtener los detalles de la venta: {str(e)}")
        return None
@app.route('/guardar_detalles_venta', methods=['POST'])
def guardar_detalles_venta():
    try:
        return redirect(url_for('caja'))
    except Exception as e:
        print(f"Error al guardar los detalles de la venta: {str(e)}")
        return redirect(url_for('error_page'))

@app.route('/generar_ticket/<id_venta>')
def generar_ticket(id_venta):
    # Lógica para generar el ticket
    return render_template('factura.html', id_venta=id_venta)"""

"""
@app.route("/clientes")
def clientes():
    db_connection, cursor = db.conectar_bd()
    
    # Obtener el próximo valor autoincremental de id_producto
    cursor.execute("SHOW TABLE STATUS LIKE 'cliente'")
    table_status = cursor.fetchone()
    next_id = table_status[10]  # El índice 10 corresponde a la columna Auto_increment
    
    # Contar la cantidad de registros
    cursor.execute("SELECT COUNT(*) FROM cliente")
    count = cursor.fetchone()[0]
    if count == 0:
        next_id = 1  # Si no hay registros, comenzar desde 1
    else:
        # Obtener el último ID y ajustar para el siguiente ID
        cursor.execute("SELECT MAX(id_cliente) FROM cliente")
        last_id = cursor.fetchone()[0]
        next_id = last_id + 1
    
    # Obtener los productos existentes
    cursor.execute("SELECT * FROM cliente")
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
        sql = "DELETE FROM cliente WHERE id_cliente=%s"
        data = (id_cliente,)
        cursor.execute(sql, data)
        db_connection.commit()
        cursor.close()
        db_connection.close()
        return redirect(url_for('clientes'))"""

"""@app.route("/proveedores")
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

@app.route('/editar_proveedor', methods=['POST'])
def editar_proveedor():
    # Tu lógica para editar el proveedor aquí

    if request.method == 'POST':
        id_proveedor = request.form['id_proveedor']
        tipo_identificacion = request.form['tipo_identificacion']
        numero_identificacion = request.form['numero_identificacion']
        nombre_proveedor = request.form['nombre_proveedor']
        email = request.form['email']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        dia_de_visita = request.form['dia_de_visita']
        dia_de_entrega = request.form['dia_de_entrega']

        if id_proveedor and tipo_identificacion and numero_identificacion and nombre_proveedor and email and direccion and telefono and dia_de_visita and dia_de_entrega:
            if db.actualizar_proveedor(id_proveedor, tipo_identificacion, numero_identificacion, nombre_proveedor, email, direccion, telefono, dia_de_visita, dia_de_entrega):
                return 'Proveedor editado exitosamente'
            else:
                return 'Proveedor no encontrado'
        else:
            return 'Todos los campos son obligatorios'"""



"""#Ruta para guardar PRODUCTOS
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
     id_proveedor = request.form['id_proveedor']
     stock = request.form['stock']
     valorUnitario = request.form['valor_unitario']
     unidadMedida = request.form['unidad_medida']

     if codigo and descripcion and categoria and id_proveedor and stock and valorUnitario and unidadMedida:
        db_connection, cursor = db.conectar_bd()
        sql = "INSERT INTO producto (codigo,descripcion,categoria,id_proveedor,stock,valor_unitario,unidad_medida) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        data = (codigo,descripcion,categoria,id_proveedor,stock,valorUnitario,unidadMedida)
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

@app.route('/editar_producto', methods=['POST'])
def editar_producto():
    if request.method == 'POST':
        id_producto = request.form['id_producto']
        codigo = request.form['codigo']
        descripcion = request.form['descripcion']
        categoria = request.form['categoria']
        id_proveedor = request.form['id_proveedor']
        valor_unitario = request.form['valor_unitario']
        unidad_medida = request.form['unidad_medida']
        stock = request.form['stock']

        if id_producto and codigo and descripcion and categoria and id_proveedor  and valor_unitario and unidad_medida and stock:
            if db.actualizar_producto(id_producto, codigo, descripcion, categoria, id_proveedor, valor_unitario, unidad_medida, stock):
                return 'Producto editado exitosamente', 200
            else:
                return 'Producto no encontrado', 404
        else:
            return 'Todos los campos son obligatorios', 400"""


"""# Ruta para mostrar usuarios
@app.route("/usuario")
def usuarios():
    db_connection, cursor = db.conectar_bd()
    
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
    tipo_Identificacion = request.form['tipo_identificacion']
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
        cursor.execute("SELECT MAX(id_usuario) FROM usuario")
        last_id = cursor.fetchone()[0]

        # Calcular el próximo ID
        if last_id is None:
            next_id = 1
        else:
            next_id = last_id + 1

        # Insertar el nuevo usuario en la tabla usuarios
        sql = "INSERT INTO usuario (id_usuario, nombre, tipo_Identificacion, numero_identificacion, telefono, email, usuario, contrasenia, tipo_usuario) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
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
        sql = "DELETE FROM usuario WHERE id_usuario=%s"
        data = (id_usuario,)
        cursor.execute(sql, data)
        db_connection.commit()
        cursor.close()
        db_connection.close()
        return redirect(url_for('usuarios'))


@app.route('/editar_usuario', methods=['POST'])
def editar_usuario():
    # Tu lógica para editar el proveedor aquí

    if request.method == 'POST':
        id_usuario = request.form['id_usuario']
        nombre = request.form['nombre']
        tipo_Identificacion = request.form['tipo_identificacion']
        numero_identificacion = request.form['numero_identificacion']
        telefono = request.form['telefono']
        email = request.form['email']
        usuario = request.form['usuario']
        contrasenia = request.form['contrasenia']
        tipo_usuario = request.form['tipo_usuario']

        if nombre and tipo_Identificacion and numero_identificacion and telefono and email and usuario and contrasenia and tipo_usuario:
            if db.actualizar_usuario(id_usuario, nombre, tipo_Identificacion, numero_identificacion, telefono, email, usuario, contrasenia, tipo_usuario):
                return 'Usuario editado exitosamente'
            else:
                return 'Usuario no encontrado'
        else:
            return 'Todos los campos son obligatorios'"""

if __name__ == "__main__":
    app.run(debug=True)


