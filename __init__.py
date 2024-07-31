from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from Funciones import validar_usuario,obtener_datos,calcular_suma
app = Flask(__name__)
#Inicio Sesion
@app.route('/')
def index():
    if 'loggedin' in session and session['loggedin']:
        return redirect(url_for('dashboard'))

    return render_template('login.html')
@app.route('/login', methods=['POST'])
def login():
    try:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']        
            if validar_usuario(username, password):
                print(1)
                session['loggedin'] = True
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                print(2)
                return render_template('login.html', error='Usuario o contraseña incorrectos')

        return redirect(url_for('index'))
    except Exception as e:
        return redirect(url_for('index'))


@app.route("/", methods=['GET', 'POST'])
def mostrar_datos():
    if request.method == 'POST':
        rango = int(request.form['rango'])
    else:
        rango = 10
    
    datos = obtener_datos(rango)
    suma = calcular_suma(rango)

    return render_template('Tabla2.html', datos=datos, suma=suma)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=50580)
