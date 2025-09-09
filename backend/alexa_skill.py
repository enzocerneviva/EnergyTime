# ========================
# Importações
# ========================
from goodwe import carregar_carro  # Inicia o carregamento do carro
from goodwe import analise_inversor  # Analisa dados do inversor
from weather import get_coordinates, get_weather  # Funções do weather.py
# ia_engine.texto_alexa não será usado, porque vamos gerar o texto direto com get_weather

# ========================
# Função principal da skill Alexa
# ========================
def tratar_requisicao_alexa(dados):
    try:
        tipo_requisicao = dados["request"]["type"]  # Tipo de requisição (LaunchRequest, IntentRequest, etc.)

        # 1️⃣ Caso o usuário apenas abra a skill
        if tipo_requisicao == "LaunchRequest":
            resposta_texto = (
                "Bem-vindo! Você pode me pedir: "
                "Ligar o carregador do carro, desligar o carregador, "
                "análise do inversor ou previsão do tempo."
            )

        # 2️⃣ Caso o usuário emita um comando específico
        elif tipo_requisicao == "IntentRequest":
            intent_name = dados["request"]["intent"]["name"]

            # 🚗 Iniciar carregamento do carro
            if intent_name == "StartChargingIntent":
                carregar_carro()
                resposta_texto = "Carregamento iniciado com sucesso."

            # 🚗 Parar carregamento do carro
            elif intent_name == "StopChargingIntent":
                resposta_texto = "Carregamento parado com segurança."

            # ☀️ Previsão do tempo
            elif intent_name == "CheckWeatherIntent":
                # 2.1 Captura o estado informado no slot da Alexa
                slots = dados["request"]["intent"].get("slots", {})
                state = slots.get("state", {}).get("value") if "state" in slots else None

                # 2.2 Se o usuário ainda não informou o estado, Alexa pergunta
                if not state:
                    resposta_texto = "Qual estado você está?"
                
                # 2.3 Se o estado foi informado, busca coordenadas e previsão
                else:
                    lat, lon = get_coordinates(state)  # Pega lat/lon pelo estado
                    if lat is None or lon is None:
                        resposta_texto = f"Não consegui encontrar localização para {state}. Pode repetir?"
                    else:
                        previsao = get_weather(lat, lon)  # Busca previsão
                        # Formata a resposta em texto amigável
                        hoje = previsao[0]["hoje"]
                        amanha = previsao[1]["amanhã"]
                        resposta_texto = (
                            f"A previsão para {state}:\n"
                            f"Hoje → Temp: {hoje['temperatura']:.1f}°C, "
                            f"Umidade: {hoje['umidade']}%, "
                            f"Vento: {hoje['vento']:.1f} m/s, "
                            f"Chuva: {hoje['precipitacao']} mm.\n"
                            f"Amanhã → Temp: {amanha['temperatura']:.1f}°C, "
                            f"Umidade: {amanha['umidade']}%, "
                            f"Vento: {amanha['vento']:.1f} m/s, "
                            f"Chuva: {amanha['precipitacao']} mm."
                        )

            # ⚡ Análise do inversor
            elif intent_name == "CheckInversorIntent":
                resposta_texto = f"Esses são os dados do inversor: {analise_inversor()}"
                print(analise_inversor())  # Para debug no console

            # ❌ Comando não reconhecido
            else:
                resposta_texto = "Desculpe, não entendi seu comando."

        # Tipo de requisição desconhecido
        else:
            resposta_texto = "Tipo de requisição desconhecido."

    except Exception as e:
        import traceback
        traceback.print_exc()
        print("ERRO DETECTADO:", str(e))
        print("DADOS RECEBIDOS:", dados)
        resposta_texto = "Houve um erro ao processar sua solicitação."

    # Retorna a resposta no formato esperado pela Alexa
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
