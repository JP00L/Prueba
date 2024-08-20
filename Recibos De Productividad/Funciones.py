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

def Reset_Data():
    conexion = mysql.connector.connect(
        host="mysql-easyocr.alwaysdata.net",
        user="easyocr",
        password="admin2023",
        database="easyocr_2"
    )
    cursor = conexion.cursor()

    alter_query = "ALTER TABLE `Bogota` AUTO_INCREMENT = 1;"
    delete_query = "DELETE FROM Recibos_Pro;"
    delete_query2 = "DELETE FROM Bogota;"

    cursor.execute(delete_query2)
    conexion.commit() 

    cursor.execute(delete_query)
    conexion.commit()

    cursor.execute(alter_query)
    conexion.commit()

    cursor.close()
    conexion.close()

    return "OK"

def Extraccion_Data(Data):
    try:
        conexion = mysql.connector.connect(
            host="mysql-easyocr.alwaysdata.net",
            user="easyocr",
            password="admin2023",
            database="easyocr_2"
        )
        cursor = conexion.cursor()

        select_query = "SELECT * FROM `Recibos_Pro` WHERE `ReciboPro` = %s"
   
        cursor.execute(select_query, (Data,))
        dato = cursor.fetchall()
        Datos=[(dato[0][0],dato[0][1],dato[0][2],dato[0][3],dato[0][4],dato[0][5],dato[0][6],dato[0][7],'${:,.0f}'.format(int(dato[0][8])),'${:,.0f}'.format(int(dato[0][9])),'${:,.0f}'.format(int(dato[0][10])),dato[0][11],dato[0][12],dato[0][13],dato[0][14],dato[0][15],dato[0][16],dato[0][17],dato[0][18],dato[0][19],dato[0][20],dato[0][21],dato[0][22],dato[0][23],dato[0][24],dato[0][25],dato[0][26],dato[0][27],dato[0][28],dato[0][29],dato[0][30],dato[0][31],dato[0][32],dato[0][33],dato[0][34],dato[0][35],dato[0][36],dato[0][37],dato[0][38],dato[0][39],dato[0][40],dato[0][41],dato[0][42],dato[0][43],dato[0][44],dato[0][45],dato[0][46],dato[0][47],dato[0][48],dato[0][49],dato[0][50],dato[0][51],dato[0][52],dato[0][53],dato[0][54],dato[0][55],dato[0][56],dato[0][57],dato[0][58],dato[0][59],dato[0][60],dato[0][61],dato[0][62],dato[0][63],dato[0][64],dato[0][65],dato[0][66],dato[0][67],dato[0][68],dato[0][69],dato[0][70],dato[0][71],dato[0][72],dato[0][73],'${:,.0f}'.format(int(dato[0][74])),'${:,.0f}'.format(int(dato[0][75])),'${:,.0f}'.format(int(dato[0][76])),'${:,.0f}'.format(int(dato[0][77])),'${:,.0f}'.format(int(dato[0][78])),'${:,.0f}'.format(int(dato[0][79])),dato[0][80],dato[0][81],dato[0][82],dato[0][83],dato[0][84],dato[0][85],dato[0][86],dato[0][87],dato[0][88],dato[0][89],'${:,.0f}'.format(int(dato[0][90])),'${:,.0f}'.format(int(dato[0][91])),'${:,.0f}'.format(int(dato[0][92])),'${:,.0f}'.format(int(dato[0][93])),'${:,.0f}'.format(int(dato[0][94])),'${:,.0f}'.format(int(dato[0][95])),'${:,.0f}'.format(int(dato[0][96])),dato[0][97],dato[0][98],dato[0][99],dato[0][100],dato[0][101],dato[0][102],dato[0][103])]
        cursor.close()
        conexion.close()

        return Datos
    except Exception as e:
        return str("Error:")

def InsertarRegistro():
    try:
        conexion = mysql.connector.connect(
            host="mysql-easyocr.alwaysdata.net",
            user="easyocr",
            password="admin2023",
            database="easyocr_2"
        )
        cursor = conexion.cursor()
        query = "INSERT INTO Bogota (id, Quien_Solicita,Valor_Neto,Valor_Inspector,Valor_Ingresado,Link) VALUES (NULL, %s, %s, %s, %s, %s)"
        cursor.execute(query, ("","","","",""))
        conexion.commit()
        nueva_id = cursor.lastrowid
        conexion.close()
        return nueva_id
    except Exception as e:
        return str(400)
    
def InsertarRecibo(Data):
    try:
        conexion = mysql.connector.connect(
            host="mysql-easyocr.alwaysdata.net",
            user="easyocr",
            password="admin2023",
            database="easyocr_2"
        )
        cursor = conexion.cursor()

        Link = f"Recibo {Data.get('Sede')} {Data.get('Consecutivo')}"
        
        query = "INSERT INTO Recibos_Pro (Consecutivo, Sede, Dia_Producido, Mes_Producido, Año_Producido, Dia_Recibido, Mes_Recibido, Año_Recibido, Valor_Inspecciones, Valor_Inspector, Valor_A_Liquidar, Inspector, I_Pv_Res_GM, I_Pv_Res_Ref, I_Re_Res_GM, I_Re_Res_Ref, I_P_Res_GM, I_P_Res_Ref, I_Pv_Com_GM, I_Pv_Com_Ref, I_P_Com_GM, I_P_Com_Ref, I_Rm_GM, I_Rm_Ref, I_Monoxidos, I_Seg_Visita, I_Ter_Visita, I_Cambio, I_Fact_Pv, I_Fact_P, I_Fact_C, I_Fact_Rm, I_Fact_Obs, Comprobante_1, Fecha_1, Valor_1, Comprobante_2, Fecha_2, Valor_2, Comprobante_3, Fecha_3, Valor_3, Comprobante_4, Fecha_4, Valor_4, Comprobante_5, Fecha_5, Valor_5, Comprobante_6, Fecha_6, Valor_6, Comprobante_7, Fecha_7, Valor_7, Comprobante_8, Fecha_8, Valor_8, Porcentaje_1, Porc_1, Porcentaje_2, Porc_2, L_Pv_Res_GM, L_Pv_Ref_Ref_Cs, L_Pv_Ref_Ref_Ss, L_Re_Res_GM, L_Re_Ref_Ref_Cs, L_Re_Ref_Ref_Ss, L_P_Res_GM, L_P_Ref_Ref, L_Pv_Com_GM, L_Pv_Com_Ref_Cs, L_Pv_Com_Ref_Ss, L_P_Com_Gm, L_P_Com_Ref, L_Valor_Inspector, L_Val_1, L_Val_2, L_Val_3, L_Val_4, L_Val_5, L_Rm_Gm, L_Rm_Ref, L_Monoxido, L_Seg_Visita, L_Ter_Visita, L_Cambios, L_Fact_Pv, L_Fact_P, L_Fact_C, L_Fact_Rm, L_Val_6, L_Val_7, L_Val_8, L_Val_9, L_Val_10, L_Val_11, L_Val_12, E_Nombre, E_Reviso, Obs_1, Obs_2, Obs_3, Obs_4, Obs_5, ReciboPro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (Data.get('Consecutivo'),Data.get('Sede'),Data.get('Dia_Producido'),Data.get('Mes_Producido'),Data.get('Año_Producido'),Data.get('Dia_Recibido'),Data.get('Mes_Recibido'),Data.get('Año_Recibido'),Data.get('Valor_Inspecciones'),Data.get('Valor_Inspector'),Data.get('Valor_A_Liquidar'),Data.get('Inspector'),Data.get('I_Pv_Res_GM'),Data.get('I_Pv_Res_Ref'),Data.get('I_Re_Res_GM'),Data.get('I_Re_Res_Ref'),Data.get('I_P_Res_GM'),Data.get('I_P_Res_Ref'),Data.get('I_Pv_Com_GM'),Data.get('I_Pv_Com_Ref'),Data.get('I_P_Com_GM'),Data.get('I_P_Com_Ref'),Data.get('I_Rm_GM'),Data.get('I_Rm_Ref'),Data.get('I_Monoxidos'),Data.get('I_Seg_Visita'),Data.get('I_Ter_Visita'),Data.get('I_Cambio'),Data.get('I_Fact_Pv'),Data.get('I_Fact_P'),Data.get('I_Fact_C'),Data.get('I_Fact_Rm'),Data.get('I_Fact_Obs'),Data.get('Comprobante_1'),Data.get('Fecha_1'),Data.get('Valor_1'),Data.get('Comprobante_2'),Data.get('Fecha_2'),Data.get('Valor_2'),Data.get('Comprobante_3'),Data.get('Fecha_3'),Data.get('Valor_3'),Data.get('Comprobante_4'),Data.get('Fecha_4'),Data.get('Valor_4'),Data.get('Comprobante_5'),Data.get('Fecha_5'),Data.get('Valor_5'),Data.get('Comprobante_6'),Data.get('Fecha_6'),Data.get('Valor_6'),Data.get('Comprobante_7'),Data.get('Fecha_7'),Data.get('Valor_7'),Data.get('Comprobante_8'),Data.get('Fecha_8'),Data.get('Valor_8'),Data.get('Porcentaje_1'),Data.get('Porc_1'),Data.get('Porcentaje_2'),Data.get('Porc_2'),Data.get('L_Pv_Res_GM'),Data.get('L_Pv_Ref_Ref_Cs'),Data.get('L_Pv_Ref_Ref_Ss'),Data.get('L_Re_Res_GM'),Data.get('L_Re_Ref_Ref_Cs'),Data.get('L_Re_Ref_Ref_Ss'),Data.get('L_P_Res_GM'),Data.get('L_P_Ref_Ref'),Data.get('L_Pv_Com_GM'),Data.get('L_Pv_Com_Ref_Cs'),Data.get('L_Pv_Com_Ref_Ss'),Data.get('L_P_Com_Gm'),Data.get('L_P_Com_Ref'),Data.get('L_Valor_Inspector'),Data.get('L_Val_1'),Data.get('L_Val_2'),Data.get('L_Val_3'),Data.get('L_Val_4'),Data.get('L_Val_5'),Data.get('L_Rm_Gm'),Data.get('L_Rm_Ref'),Data.get('L_Monoxido'),Data.get('L_Seg_Visita'),Data.get('L_Ter_Visita'),Data.get('L_Cambios'),Data.get('L_Fact_Pv'),Data.get('L_Fact_P'),Data.get('L_Fact_C'),Data.get('L_Fact_Rm'),Data.get('L_Val_6'),Data.get('L_Val_7'),Data.get('L_Val_8'),Data.get('L_Val_9'),Data.get('L_Val_10'),Data.get('L_Val_11'),Data.get('L_Val_12'),Data.get('E_Nombre'),Data.get('E_Reviso'),Data.get('Obs_1'),Data.get('Obs_2'),Data.get('Obs_3'),Data.get('Obs_4'),Data.get('Obs_5'),Link)) 
        conexion.commit()

        
        query = "UPDATE Bogota SET Quien_Solicita = %s, Valor_Inspector = %s, Valor_Neto = %s, Valor_Ingresado = %s, Link = %s WHERE Bogota.id = %s;"
        cursor.execute(query, (str(Data.get('E_Nombre')),str(Data.get('Valor_Inspector')),str(Data.get('Valor_Inspecciones')), str(Data.get('Valor_A_Liquidar')), Link, int(Data.get('Consecutivo'))))
        conexion.commit()

        return 200
    except Exception as e:
        return 400
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()





