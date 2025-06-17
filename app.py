from flask import Flask, request, jsonify
from backend.goodwe import carregar_carro  # ou qualquer outro nome correto

app = Flask(__name__)

@app.route("/alexa", methods=["POST"])
def alexa_webhook():
    dados = request.get_json()

    try:
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

    except Exception as e:
        print("Erro:", e)
        resposta_texto = "Houve um erro ao processar sua solicitação."

    resposta = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": resposta_texto
            },
            "shouldEndSession": True
        }
    }

    return jsonify(resposta)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

