import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# ============================
# Carrega a chave da OpenWeather do arquivo .env
# ============================
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# ============================
# Função para buscar latitude/longitude pelo estado
# ============================
def get_coordinates(state, country="BR"):
    """
    Usa a OpenWeather Geocoding API para converter o nome do estado
    em latitude e longitude. Normalmente retorna a capital do estado.
    """
    try:
        # Monta a URL da Geocoding API
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={state},{country}&limit=1&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()

        # Se não encontrou resultados
        if not data or len(data) == 0:
            return None, None

        # Retorna latitude e longitude do primeiro resultado
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        return lat, lon

    except Exception as e:
        print("Erro ao buscar coordenadas:", e)
        return None, None
