import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- CONFIGURACIÓN ROBUSTA ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

google_json = os.environ.get("GOOGLE_JSON")

if google_json:
    info_dict = json.loads(google_json)
    
    # REPARACIÓN CRÍTICA: Asegura que los saltos de línea de la llave privada sean correctos
    if "private_key" in info_dict:
        info_dict["private_key"] = info_dict["private_key"].replace("\\n", "\n")
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(info_dict, scope)
else:
    raise ValueError("La variable GOOGLE_JSON no está configurada en Render")

# Conexión
client = gspread.authorize(creds)
sheet = client.open("Reporte_Stock").sheet1
