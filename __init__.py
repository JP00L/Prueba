from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from Funciones import validar_usuario
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

# Inicio Sesion
@app.route('/')
def index():
    if 'loggedin' in session and session['loggedin']:
        return redirect(url_for('Tabla'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            validation_result = validar_usuario(username, password)
            
            if validation_result == True:
                session['loggedin'] = True
                session['username'] = username
                return redirect(url_for('Tabla'))
            else:
                return render_template('login.html', error=validation_result)
        
        return redirect(url_for('index'))
    except Exception as e:
        return redirect(url_for('index'))


# index
@app.route('/index', methods=['GET', 'POST'])
def Tabla():
    return render_template("index.html")

# Cerrar Sesion
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('index'))

# Servir archivos estáticos
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

# # Manejar rutas no encontradas
# @app.errorhandler(404)
# def page_not_found(e):
#     session.pop('loggedin', None)
#     session.pop('username', None)
#     return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=50580)
