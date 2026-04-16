import fastapi_poe as fp
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

import fastapi_poe as fp
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# --- CONFIGURACIÓN DE GOOGLE SHEETS ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

# Nombre exacto de tu archivo de Google Sheets
NOMBRE_HOJA = "Reporte_Stock" 
sheet = client.open(NOMBRE_HOJA).sheet1

# --- LÓGICA DEL BOT ---
class MiBotConSheets(fp.PoeBot):
    async def get_response(self, request: fp.QueryRequest):
        pregunta = request.query[-1].content
        usuario = request.user_id 

        try:
            # ESCRIBIR en Google Sheets
            sheet.append_row([usuario, pregunta])

            yield fp.PartialResponse(text=f"¡Hola! He guardado tu mensaje '{pregunta}' en el Reporte_Stock exitosamente.")
        
        except Exception as e:
            yield fp.PartialResponse(text=f"Error: {str(e)}")

# --- EJECUCIÓN ---
if __name__ == "__main__":
    # Render usa la variable de entorno PORT, si no existe usa el 8080
    port = int(os.environ.get("PORT", 8080))
    fp.run(MiBotConSheets(), port=port, allow_without_key=True)