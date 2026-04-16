import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import fastapi_poe as fp

# --- CONFIGURACIÓN ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

def obtener_creds():
    # Buscamos la variable que pegaste en Render
    google_json = os.environ.get("GOOGLE_JSON")
    if not google_json:
        raise ValueError("No se encontró la variable GOOGLE_JSON en Render")
    
    # Cargamos el JSON
    info_dict = json.loads(google_json)
    
    # REPARACIÓN DE LLAVE: Esto arregla el error 'Invalid JWT Signature'
    if "private_key" in info_dict:
        # Reemplaza los saltos de línea mal formateados
        info_dict["private_key"] = info_dict["private_key"].replace("\\n", "\n")
    
    return ServiceAccountCredentials.from_json_keyfile_dict(info_dict, scope)

# Intentar conectar a Google Sheets al arrancar
try:
    creds = obtener_creds()
    client = gspread.authorize(creds)
    # Asegúrate que el archivo se llame exactamente así en tu Drive
    sheet = client.open("Reporte_Stock").sheet1
    print("Conexión exitosa a Google Sheets")
except Exception as e:
    print(f"Error conectando a Sheets: {e}")

class MiBotConSheets(fp.PoeBot):
    async def get_response(self, request: fp.QueryRequest):
        pregunta = request.query[-1].content
        usuario = request.user_id 
        try:
            # Escribir en la hoja
            sheet.append_row([usuario, pregunta])
            yield fp.PartialResponse(text=f"He guardado tu reporte: '{pregunta}'")
        except Exception as e:
            yield fp.PartialResponse(text=f"Error al escribir: {e}")

if __name__ == "__main__":
    # Render usa el puerto 8080 por defecto
    port = int(os.environ.get("PORT", 8080))
    fp.run(MiBotConSheets(), port=port, allow_without_key=True)
