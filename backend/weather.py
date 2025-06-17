import requests
from dotenv import load_dotenv #&  Função da biblioteca python-dotenv que carrega as variáveis do .env para o ambiente.
import os #& Biblioteca nativa do python para trabalhar com arquivos, caminhos e váriaveis de ambiente
from datetime import datetime, timedelta

#& Caminho para achar o .env na a partir da localização do arquivo desse código desde o início
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env') 
#& Lê as variáveis do arquivo .env
load_dotenv(dotenv_path) 

lat = -23.5489
lon = -46.6388

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

#& Função que recebe entradas: cidade -> cidade que vai pegar os dados de tempo; units -> tipo de unidade para receber os dados (definimos metrics por padrão)
def get_weather():
    response = requests.get(BASE_URL)

    #& Verificação de resposta da API
    if response.status_code != 200:
        return {"erro": "Erro ao buscar dados na API"}
    
    #& Conversão dos dados para json 
    dados = response.json()
    result = []
   
    #& Coletando data atual
    agora = str(datetime.now())
    data, hora = agora.split(' ')
    ano_n, mes_n, dia_n = data.split('-')
    ano_n, mes_n, dia_n = int(ano_n), int(mes_n), int(dia_n)
    
    #& Criando variáveis para tirar a média das informações

    precipitacao = 0
    temperatura = 0
    umidade = 0
    vento = 0
    
    precipitacao2 = 0
    temperatura2 = 0
    umidade2 = 0
    vento2 = 0

    #& Previsão do dia atual

    lista = dados["list"]
    i = -1
    x = 0

    while x == 0:
        i += 1
        prev = lista[i]
        dt_prev = prev["dt_txt"]
        data = dt_prev[0:10]
        ano_p, mes_p, dia_p = data.split('-')
        ano_p, mes_p, dia_p = int(ano_p), int(mes_p), int(dia_p)

        if ano_p > ano_n:
            x = 1
        if mes_p > mes_n:
            x = 1
        if dia_p > dia_n:
            x = 1

        precipitacao += lista[i].get("rain", {}).get("3h", 0)
        temperatura += prev["main"]["temp"]
        umidade += prev["main"]["humidity"]
        vento += prev["wind"]["speed"]

    temperatura = temperatura / (i + 1)
    umidade = umidade / (i + 1)
    vento = vento / (i + 1)

    result.append({"hoje": {
        "precipitacao": precipitacao,
        "temperatura": temperatura,
        "umidade": umidade,
        "vento": vento
    }})

    for j in range(i + 1, i + 9, 1):

        prev2 = lista[j]
        precipitacao2 += lista[j].get("rain", {}).get("3h", 0)
        temperatura2 += prev2["main"]["temp"]
        umidade2 += prev2["main"]["humidity"]
        vento2 += prev2["wind"]["speed"]

    result.append({
    "amanhã": {
        "precipitacao": precipitacao,
        "temperatura": temperatura,
        "umidade": umidade,
        "vento": vento
        } 
    })

    return result