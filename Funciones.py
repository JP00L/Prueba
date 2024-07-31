import mysql.connector
import hashlib

def validar_usuario(username, password):
    try:
        consulta = "SELECT * FROM ADM WHERE Nombre = %s"
        with mysql.connector.connect(user='335042', password='admin2023', host='mysql-homeservices.alwaysdata.net', database='homeservices_1') as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(consulta, (username,))
                usuarios = cursor.fetchall()

        for usuario in usuarios:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if hashed_password == usuario[2]:
                return True

        return False
    except Exception as e:
        return f"Error en validar_usuario: {str(e)}"
    
def obtener_datos(rango):
    try:
        conexion = mysql.connector.connect(
            host="mysql-easyocr.alwaysdata.net",
            user="easyocr",
            password="admin2023",
            database="easyocr_2"
        )
        cursor = conexion.cursor()
        cursor.execute(f"SELECT * FROM Bogota LIMIT {rango}")
        datos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return datos
    except Exception as e:
        return str(400)

def calcular_suma(rango):
    try:
        conexion = mysql.connector.connect(
            host="mysql-easyocr.alwaysdata.net",
            user="easyocr",
            password="admin2023",
            database="easyocr_2"
        )
        cursor = conexion.cursor()
        cursor.execute(f"SELECT SUM(Valor_Ingresado) FROM (SELECT * FROM Bogota LIMIT {rango}) AS subconsulta")
        suma = cursor.fetchone()[0]
        suma_formateada = "${:,.0f}".format(suma)
        cursor.close()
        conexion.close()
        return suma_formateada
    except Exception as e:
        return str("Error 400")

    