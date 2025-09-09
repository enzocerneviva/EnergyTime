from goodwe import ligarCarregador, desligarCarregador, analiseInversor  # Funções que retornam textos para alexa da atividade
from ia_engine import previsaoQuedaDeEnergiaAlexa  # Função que retorna o texto sobre previsão do tempo para Alexa

import os
import pandas as pd
from geocoding import geocoding
import json

# caminho do arquivo JSON com user_id -> estado
caminho_base_de_dados = os.path.join(os.path.dirname(__file__), 'basesDeDados', 'id_location.json')


def carregar_dados():
    """Carrega o JSON com user_id -> estado. Se não existir, cria vazio."""
    if not os.path.exists(caminho_base_de_dados):
        return {}
    with open(caminho_base_de_dados, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_dados(dados):
    """Salva o dicionário atualizado no JSON."""
    with open(caminho_base_de_dados, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


# ---------------------- INTENTS ----------------------

def handle_check_weather(dados):
    user_id = dados["session"]["user"]["userId"]
    dadosIdLocation = carregar_dados()

    if user_id in dadosIdLocation:  # já temos estado salvo
        estado = dadosIdLocation[user_id]
        lat, lon = geocoding(estado)
        resposta_texto = previsaoQuedaDeEnergiaAlexa(lat, lon, estado)
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {"type": "PlainText", "text": resposta_texto},
                "shouldEndSession": True
            }
        }
    else:  # ainda não temos estado salvo
        resposta_texto = (
            "Qual é o estado em que você está localizado? "
            "Você pode responder como: 'Eu estou em São Paulo'."
        )
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {"type": "PlainText", "text": resposta_texto},
                "shouldEndSession": False
            }
        }


def handle_get_state(dados):
    user_id = dados["session"]["user"]["userId"]
    estado = dados["request"]["intent"]["slots"]["estado"]["value"]

    # salvar no JSON
    dadosIdLocation = carregar_dados()
    dadosIdLocation[user_id] = estado
    salvar_dados(dadosIdLocation)

    # já responde com previsão
    lat, lon = geocoding(estado)
    resposta_texto = previsaoQuedaDeEnergiaAlexa(lat, lon, estado)

    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {"type": "PlainText", "text": resposta_texto},
            "shouldEndSession": True
        }
    }


# Função principal para tratar as requisições da Alexa
def requisicao_alexa(dados):
    try:
        tipo_requisicao = dados["request"]["type"]  # Obtém o tipo da requisição (LaunchRequest, IntentRequest, etc.)

        # Caso o usuário apenas abra a skill
        if tipo_requisicao == "LaunchRequest":
            resposta_texto = (
                "Bem-vindo! Você pode me pedir as seguintes funcionalidades: "
                "Ligar o carregador, Desligar o carregador, Previsão de queda de energia, "
                "Informação de índice solar, Status da planta ou Dados do inversor"
            )

        # Caso o usuário tenha emitido um comando específico (intent)
        elif tipo_requisicao == "IntentRequest":
            intent_name = dados["request"]["intent"]["name"]  # Nome da intent solicitada

            # Verifica qual intent foi solicitada e age de acordo
            if intent_name == "StartChargingIntent":
                resposta_texto = ligarCarregador()

            elif intent_name == "StopChargingIntent":
                resposta_texto = desligarCarregador()

            elif intent_name == "CheckWeatherIntent":
                return handle_check_weather(dados)

            elif intent_name == "GetStateIntent":
                return handle_get_state(dados)

            elif intent_name == "CheckInversorIntent":
                resposta_texto = f"Esses são os dados obtidos da análise do inversor: {analiseInversor()}"

            else:
                resposta_texto = "Desculpe, não entendi seu comando."

        else:
            resposta_texto = "Tipo de requisição desconhecido."

    except Exception as e:
        import traceback
        traceback.print_exc()
        print("ERRO DETECTADO:", str(e))
        print("DADOS RECEBIDOS:", dados)
        resposta_texto = "Houve um erro ao processar sua solicitação."

    # Retorna o formato esperado pela Alexa para resposta
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": resposta_texto
            },
            "shouldEndSession": True
        }
    }
