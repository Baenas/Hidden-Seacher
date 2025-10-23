import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template
import webbrowser
import threading
from busqueda import buscar, listar_txt, leer_lineas
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', mensaje="")


@app.route('/buscar')
def agregar():
    return render_template('buscar.html', mensaje="")



@app.route('/buscar/add',methods=['POST'])
def add():
    texto = request.form['texto']
    buscar(texto)
    return render_template('buscar.html', mensaje=f"✅ Entrada '{texto}' agregada correctamente.")


@app.route('/listar')
def list():
    return render_template('listar.html', mensaje="")

@app.route('/files')
def files():
    archivos = listar_txt('webs')
    return render_template('files.html', archivos=archivos)

@app.route('/files/<nombre>')
def ver_archivo(nombre):
    lineas = leer_lineas('webs', nombre)
    return render_template('file.html', archivo=nombre, lineas=lineas)

@app.route('/web/<name>')
def webs(name):
    return render_template('website.html', name=name)

def abrir_navegador():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == '__main__':
    threading.Timer(1.0, abrir_navegador).start()
    app.run(debug=False)
