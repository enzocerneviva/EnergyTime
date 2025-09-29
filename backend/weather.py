import requests
import os
from datetime import datetime, timedelta
from google.colab import userdata

# Obtém a chave da API OpenWeather dos variáveis de ambiente do Colab Secrets.
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
    if not API_KEY:
        print("API Key not loaded, cannot get coordinates.")
        return None, None
    try:
        # Monta a URL da Geocoding API
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={state},{country}&limit=1&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()

        # Se não encontrou resultados
        if not data or len(data) == 0:
            print(f"No coordinates found for {state}, {country}")
            return None, None

        # Retorna latitude e longitude do primeiro resultado
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        return lat, lon

    except Exception as e:
        print("Erro ao buscar coordenadas:", e)
        return None, None


# Função que faz a requisição e o processamento dos dados climáticos.
def get_weather(lat, lon):
    """
    Faz a requisição para a API OpenWeather e processa os dados climáticos
    para as coordenadas fornecidas.
    """
    if not API_KEY:
        print("API Key not loaded, cannot get weather data.")
        return {"erro": "API Key not loaded"}

    # Monta a URL base para requisição da previsão do tempo (5 dias a cada 3h), já com as coordenadas e chave da API.
    BASE_URL = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    # Faz uma requisição GET para a API do OpenWeather.
    response = requests.get(BASE_URL)

    # Verifica se a resposta foi bem-sucedida (status 200).
    if response.status_code != 200:
        return {"erro": f"Erro ao buscar dados na API. Status code: {response.status_code}"}

    # Converte a resposta da API de JSON para um dicionário Python.
    dados = response.json()
    result = []

    # Coleta a data e hora atual.
    agora = str(datetime.now())
    data, hora = agora.split(' ')
    ano_n, mes_n, dia_n = data.split('-')
    ano_n, mes_n, dia_n = int(ano_n), int(mes_n), int(dia_n)

    # Inicializa variáveis para calcular médias dos parâmetros climáticos.
    precipitacao = 0
    temperatura = 0
    umidade = 0
    vento = 0

    precipitacao2 = 0
    temperatura2 = 0
    umidade2 = 0
    vento2 = 0

    # Previsão para o dia atual (soma os valores até mudar de dia no dataset).
    lista = dados["list"]
    i = -1
    x = 0

    # Loop para percorrer as previsões do dia atual.
    while x == 0 and i + 1 < len(lista): # Added boundary check
        i += 1
        prev = lista[i]
        dt_prev = prev["dt_txt"] # Data e hora da previsão.
        data = dt_prev[0:10] # Extrai só a data.
        ano_p, mes_p, dia_p = data.split('-')
        ano_p, mes_p, dia_p = int(ano_p), int(mes_p), int(dia_p)

        # Quando a data da previsão for de um dia futuro, interrompe o loop.
        if ano_p > ano_n or mes_p > mes_n or dia_p > dia_n: # Simplified condition
            x = 1
        else: # Only sum if it's today's data
            # Soma os valores dos parâmetros climáticos.
            precipitacao += lista[i].get("rain", {}).get("3h", 0) # Se não houver chuva, assume 0.
            temperatura += prev["main"]["temp"]
            umidade += prev["main"]["humidity"]
            vento += prev["wind"]["speed"]

    # Calculate the count of entries for today
    count_today = i if x == 1 else i + 1 # If loop broke due to date change, i is the last index of today, so count is i+1. If loop finished all entries and they were all today, count is i+1.
    if count_today > 0:
        # Calcula a média dos valores coletados para o dia de hoje.
        temperatura = temperatura / count_today
        umidade = umidade / count_today
        vento = vento / count_today
    else: # Handle case where no data for today was found (unlikely with 5-day forecast)
        temperatura = 0
        umidade = 0
        vento = 0


    # Adiciona os resultados de hoje no array de resultados.
    result.append({"hoje": {
        "precipitacao": precipitacao,
        "temperatura": temperatura,
        "umidade": umidade,
        "vento": vento
    }})

    # Previsão para amanhã (próximas 8 faixas de 3h, ou seja, 24h seguintes após o loop anterior).
    # Ensure there are enough entries left for tomorrow
    if i + 9 <= len(lista):
        for j in range(i + 1, i + 9): # Range is exclusive of the stop value
            prev2 = lista[j]
            precipitacao2 += lista[j].get("rain", {}).get("3h", 0)
            temperatura2 += prev2["main"]["temp"]
            umidade2 += prev2["main"]["humidity"]
            vento2 += prev2["wind"]["speed"]

        # Calcula a média dos valores coletados para amanhã.
        temperatura2 = temperatura2 / 8
        umidade2 = umidade2 / 8
        vento2 = vento2 / 8

        # Adiciona os resultados de amanhã no array de resultados.
        result.append({
            "amanhã": {
                "precipitacao": precipitacao2,
                "temperatura": temperatura2,
                "umidade": umidade2,
                "vento": vento2
            }
        })
    else:
         result.append({
            "amanhã": {
                "precipitacao": "Dados indisponíveis",
                "temperatura": "Dados indisponíveis",
                "umidade": "Dados indisponíveis",
                "vento": "Dados indisponíveis"
            }
        })


    # Retorna a lista com os resultados de hoje e amanhã.
    return result

# Example usage: Get weather for Rio de Janeiro
state_name = "Rio de Janeiro"
lat, lon = get_coordinates(state_name)

if lat is not None and lon is not None:
    # print(f"Coordinates for {state_name}: Latitude = {lat}, Longitude = {lon}")
    weather_data = get_weather(lat, lon)
    print(weather_data)
# else:
    # print(f"Could not get coordinates for {state_name}. Cannot fetch weather data.")
