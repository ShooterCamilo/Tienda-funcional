from flask import Flask, render_template
from flask import request, redirect, url_for
import requests
from blueprints.productos import productos_db
from blueprints.usuarios import usuarios_bp


servidor = Flask(__name__)

#Registrar los blueprint
servidor.register_blueprint(productos_db, url_prefix="/api")
servidor.register_blueprint(usuarios_bp, url_prefix="/api")

#cambiamos url backend usuarios
backend_url_usuarios = "http://127.0.0.1:5000/api/usuarios"
backend_url_productos = "http://127.0.0.1:5000/api/productos"

#Defino la función para el index
@servidor.route('/')
def home():
    return render_template('index.html')

@servidor.route("/productos")
def listar_productos():
    response = requests.get(backend_url_productos)
    productos = response.json() if response.status_code == 200 else []
    return render_template("productos.html", productos=productos)


@servidor.route("/producto/<int:id>")
def producto_detalle(id):
    response = requests.get(f"{backend_url_productos}/{id}")
    if response.status_code == 200:
        producto = response.json()
        return render_template("editar_producto.html", producto=producto)
    else:
        return redirect(url_for("listar_productos"))

@servidor.route("/crear_producto", methods=["GET", "POST"])
def crear_producto():
    if request.method == "POST":
        producto = {
            "nombre": request.form["nombre"],
            "descripcion": request.form["descripcion"]
        }
        response = requests.post(backend_url_productos, json=producto)
        if response.status_code == 201:
            return redirect(url_for("listar_productos"))
    return render_template("crear_producto.html")

@servidor.route("/editar_producto/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    if request.method == "POST":

        producto = {
            "nombre": request.form["nombre"],
            "descripcion": request.form["descripcion"]
        }
        response = requests.put(f"{backend_url_productos}/{id}", json=producto)
        if response.status_code == 200:
            return redirect(url_for("listar_productos"))
        else:
            return "Error al actualizar el producto", response.status_code
    response = requests.get(f"{backend_url_productos}/{id}")
    try:
        producto = response.json()
        return render_template("editar_producto.html", producto=producto)
    except:
        return redirect(url_for("listar_productos")), 404

@servidor.route("/eliminar_producto/<int:id>", methods=["POST"])
def eliminar_producto(id):
    response = requests.delete(f"{backend_url_productos}/{id}")
    return redirect(url_for("listar_productos"))

#Usuarios
@servidor.route('/usuarios')
def listar_usuarios():
    response = requests.get(backend_url_usuarios)
    usuarios = response.json() if response.status_code == 200 else []
    return render_template("usuarios.html", usuarios=usuarios)

@servidor.route("/usuarios/<int:id>")
def usuario_detalle(id):
    response = requests.get(f"{backend_url_usuarios}/{id}")
    if response.status_code == 200:
        usuario = response.json()
        return render_template("editar_usuario.html", usuario=usuario)
    else:
        return redirect(url_for("listar_usuarios"))
    
@servidor.route("/crear_usuario", methods=["GET", "POST"])
def crear_usuario():
    if request.method == "POST":
        usuario = {
            "nombre": request.form["nombre"],
            "apellido": request.form["apellido"],
            "telefono": request.form["telefono"],
            "direccion": request.form["direccion"]
        }
        response = requests.post(backend_url_usuarios, json=usuario)
        if response.status_code == 201:
            return redirect(url_for("listar_usuarios"))
    return render_template("crear_usuario.html")

@servidor.route("/editar_usuario/<int:id>", methods=["GET", "POST"])
def editar_usuario(id):
    if request.method == "POST":
        usuario = {
            "nombre": request.form["nombre"],
            "apellido": request.form["apellido"],
            "telefono": request.form["telefono"],
            "direccion": request.form["direccion"]
        }
        response = requests.put(f"{backend_url_usuarios}/{id}", json=usuario)
        if response.status_code == 200:
            return redirect(url_for("listar_usuarios"))
        else:
            return "Error al actualizar el usuario", response.status_code
    response = requests.get(f"{backend_url_usuarios}/{id}")
    try:
        usuario = response.json()
        return render_template("editar_usuario.html", usuario=usuario)
    except:
        return redirect(url_for("listar_usuarios")), 404
    
@servidor.route("/eliminar_usuario/<int:id>", methods=["POST"])
def eliminar_usuario(id):
    response = requests.delete(f"{backend_url_usuarios}/{id}")
    return redirect(url_for("listar_usuarios"))

#Ejecutar el server
if __name__ == "__main__":
    servidor.run(debug=True)