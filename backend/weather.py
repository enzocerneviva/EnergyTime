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

# ============================
# Função principal: previsão do tempo
# ============================
def get_weather(lat=-23.5489, lon=-46.6388):
    """
    Busca previsão do tempo para a latitude/longitude fornecida.
    Se não passar nada, usa São Paulo por padrão.
    Retorna resumo de hoje e amanhã.
    """
    try:
        # Monta a URL da API de forecast (5 dias a cada 3h)
        BASE_URL = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(BASE_URL)
        dados = response.json()
        result = []

        # Data atual
        agora = str(datetime.now())
        data, _ = agora.split(' ')
        ano_n, mes_n, dia_n = map(int, data.split('-'))

        # Variáveis acumuladoras
        precipitacao = temperatura = umidade = vento = 0
        precipitacao2 = temperatura2 = umidade2 = vento2 = 0

        lista = dados["list"]
        i = -1
        x = 0

        # ========================
        # Previsão de HOJE
        # ========================
        while x == 0:
            i += 1
            prev = lista[i]
            dt_prev = prev["dt_txt"]
            data_p = dt_prev[0:10]
            ano_p, mes_p, dia_p = map(int, data_p.split('-'))

            if (ano_p, mes_p, dia_p) > (ano_n, mes_n, dia_n):
                x = 1
            else:
                precipitacao += prev.get("rain", {}).get("3h", 0)
                temperatura += prev["main"]["temp"]
                umidade += prev["main"]["humidity"]
                vento += prev["wind"]["speed"]

        # Média do dia
        temperatura /= (i + 1)
        umidade /= (i + 1)
        vento /= (i + 1)

        result.append({
            "hoje": {
                "precipitacao": precipitacao,
                "temperatura": temperatura,
                "umidade": umidade,
                "vento": vento
            }
        })

        # ========================
        # Previsão de AMANHÃ (próximos 8 blocos de 3h)
        # ========================
        for j in range(i + 1, i + 9):
            prev2 = lista[j]
            precipitacao2 += prev2.get("rain", {}).get("3h", 0)
            temperatura2 += prev2["main"]["temp"]
            umidade2 += prev2["main"]["humidity"]
            vento2 += prev2["wind"]["speed"]

        # Média de amanhã
        temperatura2 /= 8
        umidade2 /= 8
        vento2 /= 8

        result.append({
            "amanhã": {
                "precipitacao": precipitacao2,
                "temperatura": temperatura2,
                "umidade": umidade2,
                "vento": vento2
            }
        })

        return result

    except Exception as e:
        print("Erro ao buscar previsão do tempo:", e)
        return {"erro": "Não foi possível obter a previsão"}

# ============================
# Exemplo de teste local
# ============================
if __name__ == "__main__":
    estado = input("Digite o nome do estado: ")
    lat, lon = get_coordinates(estado)
    if lat and lon:
        previsao = get_weather(lat, lon)
        print(f"Previsão para {estado}: {previsao}")
    else:
        print("Não foi possível encontrar a localização.")
