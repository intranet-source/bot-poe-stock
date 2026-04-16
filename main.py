import fastapi_poe as fp
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

# --- CONFIGURACIÓN DE GOOGLE SHEETS ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Leemos la variable de entorno que configuraste en Render
google_json = os.environ.get("GOOGLE_JSON")

if google_json:
    info_dict = json.loads(google_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(info_dict, scope)
else:
    # Respaldo por si acaso
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

# Nombre exacto de tu archivo de Google Sheets
NOMBRE_HOJA = "Reporte_Stock" 
sheet = client.open(NOMBRE_HOJA).sheet1

class MiBotConSheets(fp.PoeBot):
    async def get_response(self, request: fp.QueryRequest):
        pregunta = request.query[-1].content
        usuario = request.user_id 
        try:
            sheet.append_row([usuario, pregunta])
            yield fp.PartialResponse(text=f"He guardado tu mensaje: '{pregunta}'")
        except Exception as e:
            yield fp.PartialResponse(text=f"Error: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    fp.run(MiBotConSheets(), port=port, allow_without_key=True)
