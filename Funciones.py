import mysql.connector
import hashlib

def validar_usuario(username, password):
    try:
        consulta = "SELECT * FROM ADM WHERE Nombre = %s"
        with mysql.connector.connect(user='335042', password='admin2023', host='mysql-homeservices.alwaysdata.net', database='homeservices_1') as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(consulta, (username,))
                usuarios = cursor.fetchall()
        if usuarios[0][1].strip() == username.strip():
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if hashed_password == usuarios[0][2]:
                if usuarios[0][3] == "False":
                    return f"Usuario Deshabilitado" 
                else:
                    return True
            else:
                return f"Contraseña Errada"
        else:
            return "Usuario Invalido"
    except Exception as e:
        return f"Error en validar_usuario"




