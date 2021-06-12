from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL

#instanciamos al framwork flask 
app = Flask(__name__) 

#configuracion para la base de datos

#variable que sirve para ejecutar el modulo MySQL de la libreria flask_mysqldb
mysql = MySQL()

#especificamos los parametros que se utilizaran para la conexion a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tourist'

mysql.init_app(app)

#decoradores para especificar las rutas y las funciones o el resultado que arrojaren 

#especificamos la ruta del index por medio de la url
@app.route('/')
def Index():
    return render_template('index.html')

#especificamos la ruta del registrar por medio de la url
@app.route('/registrar')
def Registrar():
    return render_template('Registrar.html')

#decorador cuya funcion permite crear usuarios
@app.route('/añadir_datos', methods=['POST'])
def añadir_datos():
    #pasamos los parametros de el formulario a la base de datos 
    nombre_usu = request.form['nombre_usu']
    apellido_usu = request.form['apellido_usu']
    documento_usu = request.form['documento_usu']
    telefono_usu = request.form['telefono_usu']
    correo_usu = request.form['correo_usu']
    usuario = request.form['usuario']
    Pass = request.form['Pass']
    #ejecutamos la consulta de MySQL
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO usuario (nombre_usu, apellido_usu, documento_usu, telefono_usu, correo_usu, usuario, Pass) VALUES (%s,%s, %s, %s, %s, %s, %s)',
    (nombre_usu, apellido_usu, documento_usu, telefono_usu, correo_usu, usuario, Pass))
    mysql.connection.commit()

    return redirect("/admin")

    #redirigimos al usuario a la ruta inicial
    return redirect('/') 

#decorador cuya funcion permite mostrar a todos los usuarios en el modulo admin
@app.route('/admin')
def PerfilAdmin():
    #ejecutamos la consulta MySQL
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuario')
    #por medio de un parametro mostramos los datos en los campos del modulo especificado admin
    data = cur.fetchall()
    return render_template('/admin.html', contacts = data) 

#decorador cuya funcion permite eliminar los datos de la base de datos
@app.route('/eliminar/<string:id>')
def eliminar(id):
    #ejecutamos la consulta MySQL
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM usuario WHERE id = {0}".format(id))
    mysql.connection.commit()
    #redirigimos al usuario a la ruta admin
    return redirect('/admin') 

#decorador cuya funcion permite traer datos de la base de datos y mostrarlos en los parametros 
@app.route('/editar/<string:id>')
def editar(id):
    #ejecutamos la consulta MySQL
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuario WHERE id = {0}'.format(id))
    #por medio de un parametro mostramos los datos en los campos del modulo especificado editar_datos
    data = cur.fetchall()
    print(data)
    mysql.connection.commit()
    return render_template('editar_datos.html', usuarios = data)

#decorador cuya funcion permite actualizar los datos de un registro ya creado anteriormente
@app.route('/actualizar', methods=['POST'])
def actualizar():

    #pasamos los nuevos parametros de el usuario a la base de datos 
    id_usu = request.form['id_usu']

    nombre_usu = request.form['nombre_usu']
    apellido_usu = request.form['apellido_usu']
    documento_usu = request.form['documento_usu']
    telefono_usu = request.form['telefono_usu']
    correo_usu = request.form['correo_usu']
    usuario = request.form['usuario']
    Pass = request.form['Pass']
    #ejecutamos la consulta de MySQL
    sql = " UPDATE usuario SET nombre_usu = %s, apellido_usu = %s, documento_usu = %s, telefono_usu = %s, correo_usu = %s, usuario = %s, Pass = %s WHERE id = %s "
    infoUsuario = (nombre_usu, apellido_usu, documento_usu, telefono_usu, correo_usu, usuario, Pass, id_usu)
    cur = mysql.connection.cursor()
    cur.execute(sql,infoUsuario)
    mysql.connection.commit()
    #redirigimos al usuario a la ruta admin
    return redirect('/admin')


#validacion para determinar que estamos en el archvo principal
if __name__ == "__main__":
    #inicializar el servidor 
    app.run(port = 3000, debug = True)