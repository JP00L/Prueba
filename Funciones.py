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
    

    