from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
import hashlib

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY = 'key.json'
SPREADSHEET_ID = '1Fdw6tCFKXqZd2hMDBbztSmhmus3hSFTP7BEb9UkAdZA'
LIST_REQUEST = {
    "empleado": {
        "Type": None,
        "Sheet": "empleado!A:F"
    },
    "VtMachine": {
        "Type": None,
        "Sheet": "MaquinaDeTrabajo!A:E"
    },
    "Vanti": {
        "Type": "Table",
        "Sheet": "TableVanti!A:E"
    }


}

creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

def get_sheet_id(sheet_name):
    spreadsheet = sheet.get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets = spreadsheet.get('sheets', [])

    for sheet_item in sheets:
        if sheet_item.get("properties", {}).get("title") == sheet_name:
            return sheet_item.get("properties", {}).get("sheetId")
    return None

def Get_Rq(sheet_range, exclusions=None,Table=None):
    try:
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=sheet_range).execute()
        values = result.get('values', [])
        columnas = values[0]

        exclusions = exclusions.split(",") if exclusions else []
        lista = []
        if Table is not None:
            return values[0]
        else:
            for datos in values[1:]:
                item = {col: valor for col, valor in zip(columnas, datos) if col not in exclusions}
                lista.append(item)

        return lista
    except Exception as e:
        print(f"Error al extraer datos: {e}")
        return []

def Input_Rq(data):
    columnas = Get_Rq(LIST_REQUEST[data["Sheet"]]["Sheet"])[0].keys()
    required_fields = list(columnas)
    new_entry = data.get("D_Send", {})
    ordered_values = [new_entry.get(field, "") for field in required_fields]
    for field in required_fields:
        if field not in new_entry or not new_entry[field]:
            return f"El campo {field} es requerido y no puede estar vacío."

    sheet_range = LIST_REQUEST[data["Sheet"]]["Sheet"]
    values = [ordered_values]

    body = {'values': values}
    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=sheet_range,
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()

    return "Datos insertados correctamente"

def Delete_Rq(data, sesion):
    sheet_name = LIST_REQUEST[data["Sheet"]]["Sheet"].split('!')[0]
    sheet_id = get_sheet_id(sheet_name)
    if sheet_id is None:
        return f"No se encontró el ID de la hoja {sheet_name}."

    values = Get_Rq(LIST_REQUEST[data["Sheet"]]["Sheet"])
    
    id_to_delete = data["D_Send"].get("id")
    index_to_delete = next((i for i, item in enumerate(values) if item.get("id") == id_to_delete), None)

    if index_to_delete is None:
        return f"ID {id_to_delete} no encontrado."

    if values[index_to_delete].get("compania_id") != str(sesion.get("compani_Id")):
        return f"No tienes permiso para eliminar el ID {id_to_delete}."

    delete_request = {
        "requests": [
            {
                "deleteDimension": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "ROWS",
                        "startIndex": index_to_delete + 1,
                        "endIndex": index_to_delete + 2,
                    }
                }
            }
        ]
    }

    # Ejecutar la solicitud
    sheet.batchUpdate(spreadsheetId=SPREADSHEET_ID, body=delete_request).execute()

    return f"Elemento con ID {id_to_delete} eliminado correctamente."

def Update_Rq(data, sesion):
    sheet_range = LIST_REQUEST[data["Sheet"]]["Sheet"]
    values = Get_Rq(sheet_range)
    
    id_to_update = data["D_Send"].get("id")
    index_to_update = next((i for i, item in enumerate(values) if item.get("id") == id_to_update), None)

    if index_to_update is None:
        return f"ID {id_to_update} no encontrado."


    if values[index_to_update].get("compania_id") != str(sesion.get("compani_Id")):
        return f"No tienes permiso para actualizar el ID {id_to_update}."

    columnas = list(values[0].keys())
    update_data = data["D_Send"]

    for key, value in update_data.items():
        if key == "id":
            continue
        if key in columnas:
            col_index = columnas.index(key)
            col_letter = chr(65 + col_index)
            cell_range = f"{sheet_range.split('!')[0]}!{col_letter}{index_to_update + 2}"
            body = {'values': [[value]]}
            sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=cell_range, valueInputOption="USER_ENTERED", body=body).execute()

    return f"Elemento con ID {id_to_update} actualizado correctamente."

def Funciones_Request(sesion, data=None):
    try:
        lista = None
        empleados = Get_Rq("empleado!A:F", "id,contraseña")
        
        for datos in empleados:
            if datos.get("usuario") == sesion.get("username"):
                if datos.get("estado") == "inactivo":
                    return "Usuario Deshabilitado"

                lista = {"Datos Comapñia": [datos]}
                # lista.append(resultado)

                if data:
                    if data.get("Type") == "Get":
                        Datos_Rq = Get_Rq(LIST_REQUEST[data["Sheet"]]["Sheet"])
                        Datos_Rq_filtradas = [d for d in Datos_Rq if str(d.get("compania_id")) == str(sesion.get("compani_Id"))]
                        if LIST_REQUEST[data["Sheet"]]["Type"] =="Table":
                            Table_Th= Datos_Rq = Get_Rq(LIST_REQUEST[data["Sheet"]]["Sheet"],Table=True)
                            lista["Tabla"]={"Th":Table_Th,"Tr":Datos_Rq_filtradas}
                        else:
                            lista[data["Sheet"]] = Datos_Rq_filtradas
                        # lista.append({"VtMachine": maquinas_filtradas})

                    elif data.get("Type") == "input":
                        RT = Get_Rq(LIST_REQUEST[data["Sheet"]]["Sheet"])
                        id = str(int(RT[len(RT)-1]["id"])+1)
                        data["D_Send"]["id"] =id
                        data["D_Send"]["compania_id"] = sesion.get("compani_Id")
                        data["D_Send"]["estado"] = "activo"
                        return Input_Rq(data)
                        
                    elif data.get("Type") == "delet":
                        return Delete_Rq(data, sesion)

                    elif data.get("Type") == "update":
                        return Update_Rq(data, sesion)

                return lista

        return "Usuario no encontrado"
    except Exception as e:
        print(f"Error en Get: {e}")
        return "Error Get"


def Login_Validation(username, password):
   try:
      creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
      service = build('sheets', 'v4', credentials=creds)
      sheet = service.spreadsheets()
      RANGE = 'empleado!A:F'
      result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
      values = result.get('values', [])
      Index_Columnas= values[0].index("usuario")
      for Datos in values:
         if Datos[Index_Columnas] != "usuario":
            if Datos[Index_Columnas] == username.strip():
               if hashlib.sha256(password.encode()).hexdigest() == hashlib.sha256(Datos[Index_Columnas+1].encode()).hexdigest():
                  if Datos[Index_Columnas+2] == "inactivo":
                     return f"Usuario Deshabilitado" 
                  else:
                     return True , Datos[Index_Columnas+3]
               else:
                  return f"Contraseña Errada"
      return f"Usuario No Regitra En La Compañia"
   except Exception as e:
      return f"Error en validar_usuario"
