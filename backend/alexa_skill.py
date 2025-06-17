from flask import Flask, request, jsonify
from goodwe import *

# -- Define a rota "/alexa" que aceita requisições "POST" da Alexa Skills --
# @app.route("/alexa", methods=["POST"])

def alexa_webhook():
            # Pega o JSON enviado pela Alexa na requisição HTTP
    dados = request.get_json()
 
    try:
        # Extrai o nome da intent enviada pela Alexa
        intent_name = dados["request"]["intent"]["name"]
 
        # Verifica qual intent foi recebida e define a resposta de voz correspondente
        if intent_name == "StartChargingIntent":
            carregar_carro()
            resposta_texto = "Carregamento iniciado com sucesso."
 
        elif intent_name == "StopChargingIntent":
            resposta_texto = "Carregamento parado com segurança."
 
        elif intent_name == "CheckWeatherIntent":
            resposta_texto = "A temperatura está X graus celcius"
 
        else:
            # Caso a intent seja desconhecida, responde com mensagem padrão
            resposta_texto = "Desculpe, não entendi seu comando."
 
    except Exception as e:
        # Se ocorrer algum erro (ex: JSON mal formatado), imprime o erro no console
        print("Erro:", e)
        # Define uma resposta de erro para a Alexa falar
        resposta_texto = "Houve um erro ao processar sua solicitação."
 
    # Monta o JSON que será enviado de volta para a Alexa
    resposta = {
        "version": "1.0",  # Versão da API Alexa
        "response": {
            "outputSpeech": {
                "type": "PlainText",  # Tipo de fala: texto simples
                "text": resposta_texto  # Texto que a Alexa vai falar
            },
            "shouldEndSession": True  # Indica que a sessão deve ser encerrada após essa resposta
        }
    }
 
    # Verifica qual tipo de resultado o usuário quer saber

    return jsonify(resposta)