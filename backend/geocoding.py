import requests
import os
from google.colab import userdata

API_KEY = userdata.get("OPENWEATHER_API_KEY")

# Verifica se a chave da API foi carregada
# print(f"API Key loaded: {API_KEY is not None}")
# if API_KEY:
#     print(f"First few characters of API Key: {API_KEY[:5]}...")
# else:
#     print("API Key is not loaded. Please check your Colab Secrets and ensure the key is named 'OPENWEATHER_API_KEY'.")


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

# Example usage and print the result
lat, lon = get_coordinates("Rio de Janeiro")
print(f"Latitude: {lat}, Longitude: {lon}")
