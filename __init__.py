from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from Funciones import validar_usuario, obtener_datos, calcular_suma

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Inicio Sesion
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
            
            print(f"Login attempt for user: {username}")  # Debug print

            if validar_usuario(username, password):
                session['loggedin'] = True
                session['username'] = username
                print("Login successful")  # Debug print
                return redirect(url_for('dashboard'))
            else:
                print("Invalid username or password")  # Debug print
                return render_template('login.html', error='Usuario o contraseña incorrectos')

        return redirect(url_for('index'))
    except Exception as e:
        print(f"An error occurred during login: {e}")  # Debug print
        return redirect(url_for('index'))

# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'loggedin' not in session or not session['loggedin']:
        return redirect(url_for('index'))

    if request.method == 'POST':
        rango = int(request.form['rango'])
    else:
        rango = 10

    datos = obtener_datos(rango)
    suma = calcular_suma(rango)

    return render_template('dashboard.html', datos=datos, suma=suma)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=50580)
