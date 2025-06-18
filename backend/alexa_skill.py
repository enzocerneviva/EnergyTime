# ========================
# Importações das funções necessárias
# ========================
from goodwe import carregar_carro  # Função para iniciar o carregamento do carro
from ia_engine import texto_alexa  # Função que retorna o texto sobre previsão do tempo para Alexa
from goodwe import analise_inversor  # Função que retorna análise dos dados do inversor

# ========================
# Função principal para tratar as requisições da Alexa
# ========================
def tratar_requisicao_alexa(dados):
    try:
        tipo_requisicao = dados["request"]["type"]  # Obtém o tipo da requisição (LaunchRequest, IntentRequest, etc.)

        # Caso o usuário apenas abra a skill
        if tipo_requisicao == "LaunchRequest":
            resposta_texto = (
                "Bem-vindo! Você pode me pedir as seguintes funcionalidades: "
                "Ligar o carregador do carro, desligue o carregador do carro, "
                "analise de queda de energia ou dados do inversor"
            )

        # Caso o usuário tenha emitido um comando específico (intent)
        elif tipo_requisicao == "IntentRequest":
            intent_name = dados["request"]["intent"]["name"]  # Nome da intent solicitada

            # Verifica qual intent foi solicitada e age de acordo
            if intent_name == "StartChargingIntent":
                carregar_carro()
                resposta_texto = "Carregamento iniciado com sucesso."

            elif intent_name == "StopChargingIntent":
                resposta_texto = "Carregamento parado com segurança."

            elif intent_name == "CheckWeatherIntent":
                resposta_texto = texto_alexa()  # Resposta com previsão do tempo

            elif intent_name == "CheckInversorIntent":
                resposta_texto = f"Esses são os dados obtidos da análise do inversor: {analise_inversor()}"
                print(analise_inversor())  # Também imprime no console para debug

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
