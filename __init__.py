from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from Funciones import validar_usuario, obtener_datos, calcular_suma, Reset_Data, Extraccion_Data, InsertarRegistro, InsertarRecibo
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

# Verificar autenticación para todas las rutas excepto login, logout y archivos estáticos
@app.before_request
def require_login():
    if request.endpoint and not request.endpoint.startswith('static'):
        allowed_routes = ['index', 'login', 'logout']
        if request.endpoint not in allowed_routes and ('loggedin' not in session or not session['loggedin']):
            return redirect(url_for('index'))

# index
@app.route('/index', methods=['GET', 'POST'])
def Tabla():
    if 'loggedin' not in session or not session['loggedin']:
        return redirect(url_for('index'))

    if request.method == 'POST':
        rango = int(request.form['rango'])
    else:
        rango = 10

    datos = obtener_datos(rango)
    suma = calcular_suma(rango)

    return render_template('index.html', datos=datos, suma=suma, rango=rango)

# Excel
@app.route('/insertar', methods=['POST'])
def Insertar():
    if request.method == 'POST':
        return f"{InsertarRegistro()}"

@app.route('/Productividad', methods=['POST'])
def Productividad():
    if request.method == 'POST':
        return f"{InsertarRecibo(request.form)}"

# Visualizacion HTML
@app.route('/Docs/<documento>')
def mostrar_pdf(documento):
    Valo = Extraccion_Data(documento)
    Valo = Valo[0]
    return render_template('dashboard.html', valores=Valo)

@app.route("/prueba")
def prueba():
    # Valo = Extraccion("Recibo B 00012")
    Valo = ('00012', 'B', '12', '03', '2024', '14', '03', '2024', '$240,000', '$117,000', '$123,000', 'Diana Marcela', '-', '-', '-', '-', '-', '3', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '58', '59', '60', '61', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 
'$0', '$0', '$0', '$0', '$0', '$0', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '$0', '$0', '$0', '$0', '$0', '$0', '$0', '-', '', '100', '101', '102', '103', '104')
    print(Valo)
    return render_template('tabla3.html', valores=Valo)

@app.route("/prueba2")
def prueba2():
    # Valo = Extraccion("Recibo B 00012")
    Valo = ('00012', 'B', '12', '03', '2024', '14', '03', '2024', '$240,000', '$117,000', '$123,000', 'Diana Marcela', '-', '-', '-', '-', '-', '3', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '58', '59', '60', '61', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 
'$0', '$0', '$0', '$0', '$0', '$0', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '$0', '$0', '$0', '$0', '$0', '$0', '$0', '-', '', '100', '101', '102', '103', '104')
    print(Valo)
    return render_template('tabla.html', valores=Valo)

# # Reset SQL
# @app.route("/JhanReset")
# def Reset():
#     Reset_Data()
#     return render_template('index.html')

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

# Manejar rutas no encontradas
@app.errorhandler(404)
def page_not_found(e):
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=50580)
