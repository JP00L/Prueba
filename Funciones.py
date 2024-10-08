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
    cursor = None
    conexion = None
    try:
        consulta = "SELECT * FROM empleado WHERE usuario = %s"
        with mysql.connector.connect(user=User, password=Pasww, host=Hots, database=Database) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(consulta, (username,))
                usuarios = cursor.fetchall()
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
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
def Extracccion(Sesion,VtMachine=None):
    cursor = None
    conexion = None
    RETORNO=None
    try:
        consulta = "SELECT * FROM empleado WHERE compania_id = %s AND usuario = %s "
        with mysql.connector.connect(user=User, password=Pasww, host=Hots, database=Database) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(consulta, (Sesion["compani_Id"],Sesion["username"],))
                columnas = cursor.column_names
                DATA = cursor.fetchall()
                columnas_excluir = ['id', 'contraseña'] 
                Lista = [{col: valor for col, valor in zip(columnas, datos) if col not in columnas_excluir}for datos in DATA]
                resultado = {"Datos Comapñia": Lista}                
                if Sesion["username"] == resultado["Datos Comapñia"][0]["usuario"]:
                    if resultado["Datos Comapñia"][0]["estado"] == "activo":
                        RETORNO=resultado

                    if resultado["Datos Comapñia"][0]["estado"] == "inactivo":
                        return "Usuario Deshabilitado"
                    
                    if VtMachine is not None:
                        consulta = "SELECT * FROM MaquinaDeTrabajo WHERE compania_id = %s"
                        cursor.execute(consulta, (Sesion["compani_Id"],))
                        columnas = cursor.column_names
                        maquinas = cursor.fetchall()
                        columnas_excluir = [] 
                        Lista = [{col: valor for col, valor in zip(columnas, maquina) if col not in columnas_excluir}for maquina in maquinas]
                        RETORNO["VtMachine"]=Lista

                    return RETORNO
                else:
                    return "Usuario Infringió, Los Parámetros Establecidos, Usuario Inhabilitado"
    except Exception as e:
        return f"Error en validar_maquina: {str(e)}"
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
def Actualizaciones_Machines(Sesion,request,machine_id):
    cursor = None
    conexion = None
    try:

        consulta = "SELECT * FROM empleado WHERE compania_id = %s AND usuario = %s "
        with mysql.connector.connect(user=User, password=Pasww, host=Hots, database=Database) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(consulta, (Sesion["compani_Id"],Sesion["username"],))
                columnas = cursor.column_names
                DATA = cursor.fetchall()
                columnas_excluir = ['id', 'contraseña'] 
                Lista = [{col: valor for col, valor in zip(columnas, datos) if col not in columnas_excluir}for datos in DATA]
                resultado = {"Datos Comapñia": Lista}
                
                if Sesion["username"] == resultado["Datos Comapñia"][0]["usuario"]:
                    if resultado["Datos Comapñia"][0]["estado"] == "inactivo":
                        return "Usuario Deshabilitado"

                    consulta = "UPDATE MaquinaDeTrabajo SET cookie = %s, parametro = %s, estado = %s WHERE id = %s AND compania_id = %s"
                    cursor.execute(consulta, (request.form['cookie'], request.form['parametro'], 'activo', machine_id, Sesion['compani_Id']))
                    conexion.commit()
                else:
                    return "Usuario Infringió, Los Parámetros Establecidos, Usuario Inhabilitado"
    except Exception as e:
        print(e)
        return f"Error en Actualizaciones_Machines"
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
