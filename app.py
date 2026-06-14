from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_apuntes_forge'

CARPETA_SUBIDAS = os.path.join('static', 'apuntes_pdf')
app.config['UPLOAD_FOLDER'] = CARPETA_SUBIDAS
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

if not os.path.exists(CARPETA_SUBIDAS):
    os.makedirs(CARPETA_SUBIDAS)

@app.route('/')
def inicio():
    return render_template('inicio.html')
Servidor:
if __name__ == '__main__':
    app.run(debug=True)
