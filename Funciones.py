import mysql.connector
import hashlib

# User="335042"
# Pasww="admin2023"
# Hots='mysql-homeservices.alwaysdata.net'
# Database="homeservices_1"

User="prueba2"
Pasww="admin2023"
Hots='mysql-prueba2.alwaysdata.net'
Database="prueba2_data"
def validar_usuario(username, password):
    try:
        consulta = "SELECT * FROM empleado WHERE usuario = %s"
        with mysql.connector.connect(user=User, password=Pasww, host=Hots, database=Database) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(consulta, (username,))
                usuarios = cursor.fetchall()
                print(usuarios)
        if usuarios[0][2].strip() == username.strip():
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if hashed_password == usuarios[0][3]:
                if usuarios[0][4] == "inactivo":
                    return f"Usuario Deshabilitado" 
                else:
                    return True , usuarios[0][5]
            else:
                return f"Contraseña Errada"
        else:
            return "Usuario Invalido"
    except Exception as e:
        return f"Error en validar_usuario"


def validar_maquina(compania_id):
    try:
        consulta = "SELECT * FROM empleado WHERE compania_id = %s"
        with mysql.connector.connect(user=User, password=Pasww, host=Hots, database=Database) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(consulta, (compania_id,))
                columnas = cursor.column_names
                maquinas = cursor.fetchall()
                
                # Construir una lista de diccionarios con los nombres de las columnas
                resultado = [dict(zip(columnas, maquina)) for maquina in maquinas]
                
                return resultado
    except Exception as e:
        return f"Error en validar_maquina: {str(e)}"

