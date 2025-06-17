from flask import Flask, request, jsonify
from alexa_skill import tratar_requisicao_alexa  # Função que vai processar a requisição Alexa

app = Flask(__name__)

@app.route("/alexa", methods=["POST"])
def alexa_webhook():
    dados = request.get_json()
    resposta = tratar_requisicao_alexa(dados)  # Chama a função da skill passando os dados
    return jsonify(resposta)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

