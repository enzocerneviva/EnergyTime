import requests
from dotenv import load_dotenv # Função da biblioteca python-dotenv que carrega as variáveis do .env para o ambiente.
import os # Biblioteca nativa do python para trabalhar com arquivos, caminhos e variáveis de ambiente.
from datetime import datetime, timedelta # Importa classes para manipulação de datas e horas.

# Caminho para localizar o arquivo .env a partir da localização deste código.
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env') 
# Carrega as variáveis de ambiente do .env.
load_dotenv(dotenv_path) 

# Latitude e longitude de São Paulo, SP.
lat = -23.5489
lon = -46.6388

# Obtém a chave da API OpenWeather das variáveis de ambiente.
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Monta a URL base para requisição da previsão do tempo (5 dias a cada 3h), já com as coordenadas e chave da API.
BASE_URL = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

# Função que faz a requisição e o processamento dos dados climáticos.
def get_weather():

    # Faz uma requisição GET para a API do OpenWeather.
    response = requests.get(BASE_URL)

    # Verifica se a resposta foi bem-sucedida (status 200).
    if response.status_code != 200:
        return {"erro": "Erro ao buscar dados na API"}
    
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
    while x == 0:
        i += 1
        prev = lista[i]
        dt_prev = prev["dt_txt"] # Data e hora da previsão.
        data = dt_prev[0:10] # Extrai só a data.
        ano_p, mes_p, dia_p = data.split('-')
        ano_p, mes_p, dia_p = int(ano_p), int(mes_p), int(dia_p)

        # Quando a data da previsão for de um dia futuro, interrompe o loop.
        if ano_p > ano_n:
            x = 1
        if mes_p > mes_n:
            x = 1
        if dia_p > dia_n:
            x = 1

        # Soma os valores dos parâmetros climáticos.
        precipitacao += lista[i].get("rain", {}).get("3h", 0) # Se não houver chuva, assume 0.
        temperatura += prev["main"]["temp"]
        umidade += prev["main"]["humidity"]
        vento += prev["wind"]["speed"]

    # Calcula a média dos valores coletados para o dia de hoje.
    temperatura = temperatura / (i + 1)
    umidade = umidade / (i + 1)
    vento = vento / (i + 1)

    # Adiciona os resultados de hoje no array de resultados.
    result.append({"hoje": {
        "precipitacao": precipitacao,
        "temperatura": temperatura,
        "umidade": umidade,
        "vento": vento
    }})

    # Previsão para amanhã (próximas 8 faixas de 3h, ou seja, 24h seguintes após o loop anterior).
    for j in range(i + 1, i + 9, 1):
        prev2 = lista[j]
        precipitacao2 += lista[j].get("rain", {}).get("3h", 0)
        temperatura2 += prev2["main"]["temp"]
        umidade2 += prev2["main"]["humidity"]
        vento2 += prev2["wind"]["speed"]

    # Adiciona os resultados de amanhã no array de resultados.
    result.append({
        "amanhã": {
            "precipitacao": precipitacao,
            "temperatura": temperatura,
            "umidade": umidade,
            "vento": vento
        } 
    })

    # Retorna a lista com os resultados de hoje e amanhã.
    return result
