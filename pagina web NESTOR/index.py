from flask import Flask, render_template, request, redirect, flash, session
from flask_mysqldb import MySQL

#Archivos locales
import controlador_login
import controlador_productos

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'clarinunefin'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


app.secret_key = b"algosecreto"

#Rutas principales y secundarias de la pagina

@app.route("/")
def principal():
    return render_template("index.html")    


@app.route("/usuario")
def usuario():
    if 'usuario' in session:
        return render_template("usuario.html")
    else: 
        return redirect("/formularioLogin")


@app.route("/formularioLogin")
def formularioLogin():
    return render_template("formularioLogin.html")


@app.route("/biblioteca")
def biblioteca():
    if 'usuario' in session:
        return render_template("biblioteca.html")
    else: 
        return redirect("/formularioLogin")

@app.route("/noticias")
def noticias():
    return render_template("noticias.html")


@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")


@app.route("/formularioRegistro")
def formularioRegistro():
    return render_template("formularioRegistro.html")

#<---------------- Apartado paginas de venta ----------------------->#
@app.route("/ventas")
def ventas():
    if 'usuario' in session:    
        return render_template("ventas.html")
    else: 
        return redirect("/formularioLogin")

@app.route("/formularioVenta")
def formularioVenta():
    if 'usuario' in session:
        return render_template("formularioVenta.html")
    else: 
        return redirect("/formularioLogin")
#<------------------------------------------------>#


#FUNCIONA BASE DE DATOS

@app.route("/guardar_usuario", methods=["POST"])
def guardar_usuario():
    Nombrecompleto = request.form["Nombrecompleto"]
    Cedula = request.form["Cedula"]
    Usuario = request.form["Usuario"]
    Contraseña = request.form["Contraseña"]
    Correo = request.form["Correo"]
    controlador_login.inser_user(Nombrecompleto, Cedula, Usuario, Contraseña, Correo)
    return redirect("/")


@app.route("/guardar_producto", methods=["POST"])
def guardar_producto():
    producto = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    numeroVendedor = request.form["numeroVendedor"]
    correoVendedor = request.form["correoVendedor"]
    controlador_productos.inser_productos(
        producto, descripcion, precio, numeroVendedor, correoVendedor
    )
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
@app.route("/articulo")
def articulo():
    if 'usuario' in session:
        return render_template("articulo.html")
    else: 
        return redirect("/formularioLogin")   

#<-------------- HACER LOGIN -------------------->#
@app.route("/consultar", methods=["GET", "POST"])
def consultar():

    if request.method == 'POST':
        email = request.form['Correo']
        password = request.form['Contraseña']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM login WHERE Correo=%s",(email,))
        user = cur.fetchone()
        cur.close()

        if len(user)>0:
            if password == user["Contraseña"]:
                session['name'] = user['Nombrecompleto']
                session['email'] = user['Correo']
                session['usuario'] = user['Usuario']
                session['identificacion'] = user['Cedula']
                return redirect("/")


            else:
                return render_template("formularioLogin.html")
        else:
            return render_template("formularioLogin.html")
    else:
        
        return render_template("formularioLogin.html")
#<-------------- FIN HACER LOGIN -------------------->#

#<-------------- MOSTRAR PRODUCTOS -------------------->#

@app.route("/consultar_producto", methods=["GET", "POST"])
def consultar_producto():

    if request.method == 'POST':
        ident = request.form['iden']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM productos WHERE id_producto=%s",(ident,))
        prod = cur.fetchone()
        cur.close()
        
        session['nombreprod'] = prod['nombre']
        session['descripcion'] = prod['descripcion']
        session['precio'] = prod['precio']
        session['numeroVendedor'] = prod['numeroVendedor']
        session['correoVendedor'] = prod['correoVendedor']
        return redirect("/articulo")


#<-------------- FIN MOSTRAR PRODUCTOS -------------------->#



#FIN DE LO QUE FUNCIONA 


if (__name__ == "__main__"):  # con esto lograremos revisar el resultado en un navegador web#
    app.run(debug=True)
