from flask import Flask, jsonify, request, render_template, redirect, url_for
from database import conectar_bd

app = Flask(__name__)

@app.route("/caja")
def caja():
    try:
        db_connection, cursor = conectar_bd()
        
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
            db_connection, cursor = conectar_bd()
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
        db_connection, cursor = conectar_bd()
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
    return render_template('factura.html', id_venta=id_venta)

if __name__ == "__main__":
    app.run(debug=True)
