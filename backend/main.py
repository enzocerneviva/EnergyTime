# main.py

import os
from flask import Flask, request, jsonify
from openai import OpenAI
import pandas as pd
import json

# Nossos módulos locais
from alexa_skill import requisicao_alexa
from id_localizacao import salvar_dados, carregar_historico
import chatbot  # Nosso novo módulo de IA

# --- INICIALIZAÇÃO DO SERVIDOR ---
app = Flask(__name__)

USER_DB_PATH = os.path.join(os.path.dirname(__file__), 'bases_de_dados', 'usuarios.json')

def carregar_utilizadores():
    try:
        with open(USER_DB_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {} # Retorna vazio se o ficheiro não existi

# 1. Carregar chave da API (NUNCA DEIXE NO CÓDIGO)
#    (No seu terminal, rode: set OPENAI_API_KEY=sua_chave_aqui)
API_KEY = os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    print("ERRO CRÍTICO: Variável de ambiente OPENAI_API_KEY não definida.")
    # (Opcional: parar o app se a chave não existir)
    # exit() 
CLIENT_OPENAI = OpenAI(api_key=API_KEY)

# 2. Definir caminhos dos PDFs (Relativo ao 'main.py')
#    (Ajuste este caminho para onde seus PDFs estão no backend)
PDF_PATHS = [
    "backend/content/GW_Commercial & Industrial Smart Inverter Solutions_User Manual-ET 15-30kW-PT.pdf",
    "backend/content/GW_Residential Smart Inverter Solutions_User Manual-ES Uniq 3-6kW-PT.pdf"
]

# 3. Carregar o RAG em memória (Ocorre UMA VEZ ao ligar o servidor)
print("Inicializando o servidor... Carregando dados do RAG...")
try:
    DADOS_RAG, DADOS_EXEMPLO = chatbot.load_data(PDF_PATHS, CLIENT_OPENAI)
    print(f"Dados do RAG carregados com sucesso. {len(DADOS_RAG)} chunks processados.")
except Exception as e:
    print(f"ERRO CRÍTICO ao carregar RAG: {e}")
    DADOS_RAG, DADOS_EXEMPLO = pd.DataFrame(), {} # Inicia vazio para evitar crash
# --- FIM DA INICIALIZAÇÃO ---


# Rota que recebe requisições da Alexa (Seu código original)
@app.route("/alexa", methods=["POST"])
def alexa_webhook():
    dados = request.get_json()
    resposta = requisicao_alexa(dados)
    salvar_dados(dados, resposta)
    return jsonify(resposta)

# Rota para fornecer o histórico (Seu código original)
@app.route("/historico", methods=["GET"])
def historico():
    return jsonify(carregar_historico())

# --- NOVA ROTA PARA O CHATBOT DO STREAMLIT ---
@app.route("/chat_ia", methods=["POST"])
def handle_chat_ia():
    """
    Recebe uma pergunta do frontend Streamlit, processa no chatbot
    e devolve a resposta.
    """
    data = request.get_json()
    if not data or 'pergunta' not in data:
        return jsonify({"erro": "Nenhuma pergunta fornecida"}), 400

    pergunta_usuario = data['pergunta']

    # Chama a função do 'chatbot.py' usando os dados carregados em memória
    resposta_ia = chatbot.chat_ia(
        pergunta=pergunta_usuario,
        dados_do_rag=DADOS_RAG,
        dados_exemplo_dict=DADOS_EXEMPLO,
        client_instance=CLIENT_OPENAI
    )
    
    # Devolve a resposta para o Streamlit
    return jsonify({"resposta": resposta_ia})
# --- FIM DA NOVA ROTA ---

# --- Rota de Login (NOVA) ---
@app.route("/login", methods=["POST"])
def handle_login():
    dados = request.get_json()
    utilizadores = carregar_utilizadores()
    
    usuario_input = dados.get("usuario")
    senha_input = dados.get("senha")

    if not usuario_input or not senha_input:
        return jsonify({"erro": "Utilizador e senha são obrigatórios"}), 400

    # Verifica se o utilizador existe no JSON
    utilizador_db = utilizadores.get(usuario_input)
    
    if utilizador_db and utilizador_db["senha"] == senha_input:
        # Sucesso no login
        return jsonify({
            "sucesso": True,
            "user_id": utilizador_db["user_id"]
        }), 200
    else:
        # Falha no login
        return jsonify({"erro": "Utilizador ou senha inválidos"}), 401

if __name__ == "__main__":
    # A porta 10000 do seu código original
    port = int(os.environ.get("PORT", 10000))
    # host="0.0.0.0" permite conexões de fora (ex: Streamlit)
    app.run(host="0.0.0.0", port=port, debug=True) # debug=True é bom para dev