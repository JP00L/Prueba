from flask import Flask, render_template, request, jsonify
import pdfplumber

app = Flask(__name__)

def Extraccion(Certificado):
    TD = []
    item={}
    with pdfplumber.open(f'{Certificado}.pdf') as pdf:
        for i, pagina in enumerate(pdf.pages):
            tablas = pagina.extract_tables()        
            for tabla in tablas:
                if i != 1:
                    for fila in tabla:
                        fila_sin_none = [elemento for elemento in fila if elemento is not None]
                        if fila_sin_none:
                            TD.append(fila_sin_none)
            break

    def Buscar_Dentro_PDF(Tabla_Datos,Busqueda,Recuento=None):
        
        for fila in Tabla_Datos:
            try:
                Cuenta=fila.index(Busqueda)
                if Recuento is None:
                    return fila
                else:
                    return fila[Cuenta+Recuento]
            except:
                pass
    Buscar_Dentro_PDF(TD,'Cuenta Número',1)


# Ray={
# "DIA":1
# "MES":1
# "AÑO":1
# }


# Uso: Residencial______Comercial______

# Hora Inicio Insp
# Hora Final Insp

# Cuenta Número
# Ciudad/Municipio


# CUENTA CON VACIO INTERNO

# Corresponde Medidor:

# Medidor Factura
# Medidor Rea

# Lectura
# Lectura


# Censos{}
# Recintos{}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            return 'No file part'
        file = request.files['pdf_file']
        if file.filename == '':
            return 'No selected file'
        if file:
            extracted_data = Extraccion(file)
            return jsonify(extracted_data)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
