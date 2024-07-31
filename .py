import mysql.connector
import hashlib
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

Reset_Data()
