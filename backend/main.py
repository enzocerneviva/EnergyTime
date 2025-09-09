# Importações e configuração inicial
from flask import Flask, request, jsonify
from alexa_skill import requisicao_alexa  # Função que vai processar a requisição Alexa

app = Flask(__name__)

# Rota para receber requisições da Alexa
@app.route("/alexa", methods=["POST"])
def alexa_webhook():
    dados = request.get_json()
    resposta = requisicao_alexa(dados)  # Chama a função da skill passando os dados
    return jsonify(resposta)

# Execução do servidor Flask
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
