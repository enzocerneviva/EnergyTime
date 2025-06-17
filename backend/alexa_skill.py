from backend.goodwe import carregar_carro  # ou qualquer função que precise

def tratar_requisicao_alexa(dados):
    try:
        tipo_requisicao = dados["request"]["type"]

        if tipo_requisicao == "LaunchRequest":
            resposta_texto = "Bem-vindo! Pode me pedir para iniciar ou parar o carregamento."

        elif tipo_requisicao == "IntentRequest":
            intent_name = dados["request"]["intent"]["name"]

            if intent_name == "StartChargingIntent":
                carregar_carro()
                resposta_texto = "Carregamento iniciado com sucesso."

            elif intent_name == "StopChargingIntent":
                resposta_texto = "Carregamento parado com segurança."

            elif intent_name == "CheckWeatherIntent":
                resposta_texto = "A temperatura está X graus celsius."

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
