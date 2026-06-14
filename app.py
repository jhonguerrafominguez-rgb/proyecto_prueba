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


def conectar_bd():
    conexion = sqlite3.connect('apuntes.db')
    conexion.row_factory = sqlite3.Row
    return conexion

def inicializar_bd():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    # Tabla actualizada: sin precio, con columna de likes (estrellas)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS apuntes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            materia TEXT NOT NULL,
            categoria TEXT NOT NULL,
            autor TEXT NOT NULL,
            archivo_nombre TEXT NOT NULL,
            estrellas INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('SELECT COUNT(*) FROM apuntes')
    if cursor.fetchone() == 0:
        datos_semilla = [
            ("Resumen Primer Parcial - Cálculo Integral", "Cálculo II", "Ciencias Básicas", "Carlos Mendoza", "ejemplo_calculo.pdf", 12),
            ("Guía Completa de Programación Orientada a Objetos", "Programación I", "Ingeniería", "Laura Restrepo", "ejemplo_poo.pdf", 24)
        ]
        cursor.executemany('''
            INSERT INTO apuntes (titulo, materia, categoria, autor, archivo_nombre, estrellas)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', datos_semilla)
        conexion.commit()
    conexion.close()

@app.route('/subir', methods=['GET', 'POST'])
def subir_apunte():
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        materia = request.form.get('materia', '').strip()
        categoria = request.form.get('categoria', '').strip()
        autor = request.form.get('autor', '').strip()
        archivo = request.files.get('archivo')
        
        if not (titulo and materia and categoria and autor and archivo):
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('subir_apunte'))
            
        if archivo.filename == '':
            flash('Archivo no válido.', 'error')
            return redirect(url_for('subir_apunte'))

        nombre_seguro = secure_filename(archivo.filename)
        ruta_guardado = os.path.join(app.config['UPLOAD_FOLDER'], nombre_seguro)
        archivo.save(ruta_guardado)
        
        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO apuntes (titulo, materia, categoria, autor, archivo_nombre)
            VALUES (?, ?, ?, ?, ?)
        ''', (titulo, materia, categoria, autor, nombre_seguro))
        conexion.commit()
        conexion.close()
        
        flash('¡Material compartido con éxito!', 'exito')
        return redirect(url_for('inicio'))
        
    return render_template('subir_apunte.html')
