from goodwe import carregar_carro  # ou qualquer função que precise
from ia_engine import texto_alexa
from goodwe import analise_inversor

def tratar_requisicao_alexa(dados):
    try:
        tipo_requisicao = dados["request"]["type"]

        if tipo_requisicao == "LaunchRequest":
            resposta_texto = "Bem-vindo! Você pode me pedir as seguintes funcionalidades: Ligar o carregador do carro, desligue o carregador do carro, analise de queda de energia ou dados do inversor"

        elif tipo_requisicao == "IntentRequest":
            intent_name = dados["request"]["intent"]["name"]

            if intent_name == "StartChargingIntent":
                carregar_carro()
                resposta_texto = "Carregamento iniciado com sucesso."

            elif intent_name == "StopChargingIntent":
                resposta_texto = "Carregamento parado com segurança."

            elif intent_name == "CheckWeatherIntent":
                resposta_texto = texto_alexa()

            elif intent_name == "CheckInversorIntent":
                resposta_texto = f"Esses são os dados obtidos da análise do inversor: {analise_inversor()}"
                print(analise_inversor())
                
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
