from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
# from Funciones import validar_usuario, Extracccion,Actualizaciones_Machines
from Funciones_2 import Login_Validation,Funciones_Request
from datetime import timedelta
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key' 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)  # Establece la duración de la sesión a 30 minutos
#Verificacion De Sesion
@app.route('/login', methods=['GET','POST'])
def login():
    try:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            validation_result = Login_Validation(username, password)
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

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('compani_Id', None)
    return redirect(url_for('index'))


# Servir archivos estáticos
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)
@app.route('/static/Js/<path:filename>')
def static_J_files(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/Js'), filename)

#______________________________Paginas_____________________________
#>Index
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'loggedin' in session and session['loggedin']:
        datos = Funciones_Request(session)
        if datos =="Usuario Deshabilitado" or datos =="Usuario Infringió, Los Parámetros Establecidos, Usuario Inhabilitado":
            return render_template('login.html', error=datos)

        return render_template("index1.html", datos=datos)
    return render_template('login.html')

#>Maquinas
@app.route('/VtMachine', methods=['GET', 'POST'])
def VtMachine():
    if 'loggedin' in session and session['loggedin']:
        datos = Funciones_Request(session,{"Sheet": "VtMachine","Type": "Get",})
        if datos =="Usuario Deshabilitado" or datos =="Usuario Infringió, Los Parámetros Establecidos, Usuario Inhabilitado":
            return render_template('login.html', error=datos)
        print(datos)
        return render_template("Maquinas_De_Procesamiento.html", datos=datos)
    return render_template('login.html')



@app.route('/update_machine/<int:machine_id>', methods=['POST'])
def update_machine(machine_id):
    print("Form Data:", request.form)
    for key, value in request.form.items():
        print(f"{key}: {value}")
    return "OK"
    # if 'loggedin' in session and session['loggedin']:
    #     Actualizaciones_Machines(session,request,machine_id)
    #     return redirect(url_for('Maquinas_De_Procesamiento'))
    # return redirect(url_for('index'))

#>Tablas
@app.route('/Dasboard', methods=['GET', 'POST'])
def Dasboard():
    if 'loggedin' in session and session['loggedin']:
        datos = Funciones_Request(session,{"Sheet": "Vanti","Type": "Get",})
        if datos =="Usuario Deshabilitado" or datos =="Usuario Infringió, Los Parámetros Establecidos, Usuario Inhabilitado":
            return render_template('login.html', error=datos)
        return render_template("Dasboard_Vanti.html", datos=datos)
    return render_template('login.html')



# # Manejar rutas no encontradas
# @app.errorhandler(404)
# def page_not_found(e):
#     session.pop('loggedin', None)
#     session.pop('username', None)
#     return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=50380)
