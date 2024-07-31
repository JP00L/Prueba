from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from Funciones import validar_usuario, obtener_datos, calcular_suma,Reset_Data,Extraccion_Data,InsertarRegistro,InsertarRecibo

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
@app.route('/index', methods=['GET', 'POST'])
def dashboard():
    if 'loggedin' not in session or not session['loggedin']:
        return redirect(url_for('index'))

    if request.method == 'POST':
        rango = int(request.form['rango'])
    else:
        rango = 10

    datos = obtener_datos(rango)
    suma = calcular_suma(rango)

    return render_template('index.html', datos=datos, suma=suma)

#Excel
@app.route('/insertar', methods=['POST'])
def Insertar():
    if request.method == 'POST':
        return f"{InsertarRegistro()}"
@app.route('/Productividad', methods=['POST'])
def Productividad():
    if request.method == 'POST':
        return f"{InsertarRecibo(request.form)}"

#Visualizacion Hmtl
@app.route('/Docs/<documento>')
def mostrar_pdf(documento):
    Valo = Extraccion_Data(documento)
    Valo = Valo[0]
    return render_template('tabla3.html', valores=Valo)

@app.route("/prueba")
def prueba():
    # Valo = Extraccion("Recibo B 00012")
    Valo = ('00012', 'B', '12', '03', '2024', '14', '03', '2024', '$240,000', '$117,000', '$123,000', 'Diana Marcela', '-', '-', '-', '-', '-', '3', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '58', '59', '60', '61', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 
'$0', '$0', '$0', '$0', '$0', '$0', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '$0', '$0', '$0', '$0', '$0', '$0', '$0', '-', '', '100', '101', '102', '103', '104')
    print(Valo)
    return render_template('tabla3.html', valores=Valo)
@app.route("/prueba2")
def prueba2():
    # Valo = Extraccion("Recibo B 00012")
    Valo = ('00012', 'B', '12', '03', '2024', '14', '03', '2024', '$240,000', '$117,000', '$123,000', 'Diana Marcela', '-', '-', '-', '-', '-', '3', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '58', '59', '60', '61', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 
'$0', '$0', '$0', '$0', '$0', '$0', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '$0', '$0', '$0', '$0', '$0', '$0', '$0', '-', '', '100', '101', '102', '103', '104')
    print(Valo)
    return render_template('tabla.html', valores=Valo)

#Reset SQL
@app.route("/JhanReset")
def Reset():
    Reset_Data()
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=50580)
