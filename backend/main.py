from flask import Flask, request, jsonify
from alexa_skill import requisicao_alexa
from id_localizacao import salvar_dados, carregar_historico

app = Flask(__name__)

# Rota que recebe requisições da Alexa
@app.route("/alexa", methods=["POST"])
def alexa_webhook():
    dados = request.get_json()
    resposta = requisicao_alexa(dados)

    # Salva intent e resposta juntas no histórico
    salvar_dados(dados, resposta)

    return jsonify(resposta)

# Rota para fornecer o histórico
@app.route("/historico", methods=["GET"])
def historico():
    return jsonify(carregar_historico())

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
