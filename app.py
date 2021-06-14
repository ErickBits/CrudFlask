from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__) 

mysql = MySQL()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crudflask'

mysql.init_app(app)

@app.route('/')
def Index():
    return render_template('crud.html')

@app.route('/añadir_datos', methods=['POST'])
def añadir_datos():
    nombre = request.form['nombre']
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO estudiante (nombre,correo,contraseña) VALUES (%s,%s, %s)',
    (nombre,correo,contraseña))
    mysql.connection.commit()

    return redirect("/mostrarDatos")

@app.route('/mostrarDatos') 
def estudiante():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM estudiante')
    data = cur.fetchall()
    return render_template('mostrarDatos.html', contacts = data) 

@app.route('/eliminar/<string:id>')
def eliminar(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM estudiante WHERE id = {0}".format(id))
    mysql.connection.commit()
    return redirect('/mostrarDatos') 

@app.route('/editar/<string:id>')
def editar(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM estudiante WHERE id = {0}'.format(id))
    data = cur.fetchall()
    print(data)
    mysql.connection.commit()
    return render_template('editar_datos.html', usuarios = data)

@app.route('/actualizar', methods=['POST'])
def actualizar():

    id_usu = request.form['id_usu']

    nombre = request.form['nombre']
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    sql = " UPDATE estudiante SET nombre = %s, correo = %s, contraseña = %s WHERE id = %s "
    infoUsuario = (nombre, correo, contraseña, id_usu)
    cur = mysql.connection.cursor()
    cur.execute(sql,infoUsuario)
    mysql.connection.commit()
    return redirect('/mostrarDatos')


if __name__ == "__main__":
    app.run(port = 3000, debug = True)