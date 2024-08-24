from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from Funciones import validar_usuario, Extracccion
from datetime import timedelta
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key' 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)  # Establece la duración de la sesión a 30 minutos

# Inicio Sesion
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'loggedin' in session and session['loggedin']:
        datos = Extracccion(session["compani_Id"])
        if datos =="Usuario Deshabilitado" or datos =="Usuario Infringió, Los Parámetros Establecidos, Usuario Inhabilitado":
            return render_template('login.html', error=datos)
        print(session)
        return render_template("index1.html", datos=datos)
    return render_template('login.html')

@app.route('/login', methods=['GET','POST'])
def login():
    try:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            validation_result = validar_usuario(username, password)
            if validation_result[0] == True:
                session.permanent = True
                session['loggedin'] = True
                session['username'] = username
                session['compani_Id'] = validation_result[1]
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error=validation_result)
        return redirect(url_for('index'))
    except Exception as e:
        return redirect(url_for('index'))

# Cerrar Sesion
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('index'))

# Servir archivos estáticos
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)
@app.route('/static/Js/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)



@app.route('/Maquinas_De_Procesamiento', methods=['GET', 'POST'])
def Maquinas_De_Procesamiento():
    return render_template("Maquinas_De_Procesamiento.html")

@app.route('/Dasboard_Vanti', methods=['GET', 'POST'])
def Dasboard_Vanti():
    return render_template("Dasboard_Vanti.html")



# # Manejar rutas no encontradas
# @app.errorhandler(404)
# def page_not_found(e):
#     session.pop('loggedin', None)
#     session.pop('username', None)
#     return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=50480)
