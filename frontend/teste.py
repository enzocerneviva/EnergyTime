import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader
import os

# --- Configuração da página ---
st.set_page_config(page_title="EnergyTime", page_icon="logo_energytime.png", layout="wide")

# --- Tema personalizado ---
custom_css = """
<style>
/* Fundo geral */
.stApp {
    background-color: #e4d4b4; 
    color: #000000; 
    font-family: 'Segoe UI', sans-serif;
    font-size: 18px;
}

/* Títulos */
h1, h2, h3 {
    color: #2e7d32; 
    font-weight: 800;
    text-align: center;
}

/* Texto centralizado */
.section-text {
    text-align: center;
    max-width: 800px;
    margin: auto;
    font-size: 1.2em;
    line-height: 1.8em;
    color: #000000;
}

/* Botões */
.stButton>button {
    background-color: #2e7d32;
    color: white;
    border-radius: 8px;
    padding: 0.8em 1.6em;
    border: none;
    font-weight: bold;
    font-size: 1em;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
}
.stButton>button:hover {
    background-color: #256428;
    color: #f1f1f1;
}

/* Chat bolhas */
.chat-bubble-user {
    background-color: #4A90E2;
    color: white;
    padding: 12px 16px;
    border-radius: 15px;
    margin: 10px auto;
    max-width: 70%;
    font-size: 1.05em;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}
.chat-bubble-bot {
    background-color: #2e7d32;
    color: white;
    padding: 12px 16px;
    border-radius: 15px;
    margin: 10px auto;
    max-width: 70%;
    font-size: 1.05em;
    font-style: italic;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- Barra superior (logo + login) ---
col1, col2 = st.columns([6,1])
with col1:
    st.image("logo_energytime.png", width=90)
with col2:
    st.markdown("<div style='text-align:right;'>", unsafe_allow_html=True)
    st.button("Login")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# --- Container central para apresentação ---
st.title("🌱 Bem-vindo à EnergyTime")
st.markdown(
    """
    <div class="section-text">
        <p>
        A <b>EnergyTime</b> conecta pessoas e tecnologia para transformar a forma como lidamos com energia.  
        Nosso objetivo é <b>simplificar o gerenciamento de energia solar</b> e integrar equipamentos inteligentes da GoodWe com assistentes virtuais como a Alexa.  
        </p>
        <p>
        Com a EnergyTime, você pode:
        </p>
        <ul style="text-align: left; display: inline-block; font-size: 1.1em; color: #000000;">
            <li>Receber recomendações personalizadas sobre uso eficiente de energia</li>
            <li>Monitorar seus equipamentos GoodWe em tempo real</li>
            <li>Obter previsões inteligentes para reduzir custos e evitar imprevistos</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ==============================
# 💬 Chat da IA (3 créditos)
# ==============================
st.subheader("💬 Assistente Virtual (3 créditos grátis)")
st.info("Você possui **3 créditos gratuitos** para conversar com a IA sobre energia e equipamentos GoodWe.")

# --- Mensagens pré-carregadas ---
st.markdown('<div class="chat-bubble-user">👤 Usuário: Como posso melhorar o uso da minha bateria?</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-bubble-bot">🤖 EnergyTime IA: Recomendo manter a bateria entre 20% e 80% para maior vida útil.</div>', unsafe_allow_html=True)

# --- OpenAI Client ---
try:
    client = OpenAI(api_key="")
except Exception:
    st.error("⚠️ Chave da API OpenAI não encontrada. Adicione-a em .streamlit/secrets.toml.")
    st.stop()

# --- Base de dados de exemplo para RAG ---
dados_exemplo_dict = {
    "equipamento": [
        "Inversor GW5000",
        "Painel Solar 550W",
        "Bateria Lynx Home U",
        "Inversor ET 10kW",
        "Bateria Lynx Home F Plus"
    ],
    "descricao": [
        "Inversor híbrido GoodWe GW5000 de 5kW, alta eficiência, suporte a monitoramento remoto via aplicativo e compatível com sistemas de baterias residenciais.",
        "Módulo fotovoltaico monocristalino de 550W para geração de energia solar, ideal para sistemas conectados à rede.",
        "Bateria de lítio GoodWe Lynx Home U, indicada para uso doméstico, com proteção avançada BMS e design modular para fácil expansão.",
        "Inversor trifásico GoodWe ET de 10kW, projetado para aplicações residenciais e comerciais, com suporte a backup de energia e ampla faixa de tensão de entrada.",
        "Bateria de lítio GoodWe Lynx Home F Plus, de alta capacidade, adequada para aplicações maiores, com alta densidade energética e vida útil estendida"
    ],
    "fonte": ["exemplo"]*5
}
dados = pd.DataFrame(dados_exemplo_dict)

# --- Funções de IA ---
def gerar_embeddings(textos):
    if not textos:
        return []
    valid_textos = [str(t) for t in textos if isinstance(t, (str, bytes))]
    if not valid_textos:
        return []
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=valid_textos
        )
        return [np.array(r.embedding) for r in response.data]
    except Exception as e:
        st.error(f"Erro ao gerar embeddings: {e}")
        return [None] * len(valid_textos)

# Gera embeddings uma vez para a base de exemplo
dados["embedding"] = gerar_embeddings(dados["descricao"].tolist())

def buscar_contexto(pergunta, top_k=3):
    if dados.empty:
        return "Nenhuma informação disponível na base de dados."
    valid_embeddings_df = dados[dados["embedding"].apply(lambda x: isinstance(x, np.ndarray))]
    if valid_embeddings_df.empty:
        return "Nenhuma informação útil (embeddings ausentes)."
    emb_pergunta_list = gerar_embeddings([pergunta])
    if not emb_pergunta_list or emb_pergunta_list[0] is None:
        return "Não foi possível gerar embedding para a pergunta."
    emb_pergunta = emb_pergunta_list[0]
    sims = cosine_similarity([emb_pergunta], valid_embeddings_df["embedding"].tolist())[0]
    indices = np.argsort(sims)[::-1][:top_k]
    return "\n".join(valid_embeddings_df.iloc[indices]["descricao"].tolist())

def chat_ia(pergunta):
    pergunta_lower = pergunta.lower()
    if "produtos goodwe" in pergunta_lower or "equipamentos goodwe" in pergunta_lower:
        return "Aqui estão alguns dos equipamentos GoodWe que conheço:\n" + "\n".join(dados_exemplo_dict["equipamento"])
    contexto = buscar_contexto(pergunta)
    prompt = f"""
Você é um assistente especialista em energia solar e equipamentos GoodWe.
Use o contexto abaixo para responder de forma clara e confiável.

Contexto:
{contexto}

Pergunta:
{pergunta}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Erro no chat: {e}")
        return "⚠️ Ocorreu um erro ao gerar a resposta."

# --- Input do usuário ---
user_input = st.text_input("Digite sua mensagem para a EnergyTime:")

if user_input:
    st.markdown(f'<div class="chat-bubble-user">👤 Usuário: {user_input}</div>', unsafe_allow_html=True)
    resposta = chat_ia(user_input)
    st.markdown(f'<div class="chat-bubble-bot">🤖 EnergyTime IA: {resposta}</div>', unsafe_allow_html=True)
