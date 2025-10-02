# ==============================
# CHAT Energy_bot - Energia & GoodWe (Streamlit)
# ==============================

import os
import openai
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader
import streamlit as st
from openai import OpenAI

# ==============================
# CONFIGURAÇÕES
# ==============================
# Defina a chave da OpenAI no ambiente (ou pelo secrets do Streamlit Cloud)
openai_api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# ==============================
# BASE DE DADOS DE EXEMPLO
# ==============================
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
    "fonte": ["exemplo", "exemplo", "exemplo", "exemplo", "exemplo"]
}
dados = pd.DataFrame(dados_exemplo_dict)

# ==============================
# FUNÇÃO: GERAR EMBEDDINGS
# ==============================
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

# Criar embeddings da base de exemplo
dados["embedding"] = gerar_embeddings(dados["descricao"].tolist())
dados.dropna(subset=["embedding"], inplace=True)
dados.reset_index(drop=True, inplace=True)

# ==============================
# FUNÇÃO: BUSCA (RAG)
# ==============================
def buscar_contexto(pergunta, top_k=3):
    if dados.empty:
        return "Nenhuma informação disponível na base de dados."
    valid_embeddings_df = dados[dados["embedding"].apply(lambda x: isinstance(x, np.ndarray))]
    if valid_embeddings_df.empty:
         return "Nenhuma informação útil na base de dados."

    valid_embeddings = valid_embeddings_df["embedding"].tolist()
    emb_pergunta_list = gerar_embeddings([pergunta])
    if not emb_pergunta_list:
         return "Não foi possível gerar embedding para a pergunta."
    emb_pergunta = emb_pergunta_list[0]

    sims = cosine_similarity([emb_pergunta], valid_embeddings)[0]
    sorted_indices_in_valid = np.argsort(sims)[::-1]
    top_k_indices_in_valid = sorted_indices_in_valid[:top_k]
    top_k_original_indices = valid_embeddings_df.iloc[top_k_indices_in_valid].index.tolist()
    contextos = dados.loc[top_k_original_indices]["descricao"].tolist()
    return "\n".join(contextos)

# ==============================
# FUNÇÃO: CHAT
# ==============================
def chat_ia(pergunta):
    pergunta_lower = pergunta.lower()
    if "produtos goodwe" in pergunta_lower or "equipamentos goodwe" in pergunta_lower:
        if dados_exemplo_dict and "equipamento" in dados_exemplo_dict:
            lista_equipamentos = "\n".join(dados_exemplo_dict["equipamento"])
            return f"Aqui estão alguns dos equipamentos GoodWe que conheço:\n{lista_equipamentos}"
        else:
            return "Não tenho uma lista específica de equipamentos GoodWe."

    contexto = buscar_contexto(pergunta)
    prompt = f"""
    Você é um assistente especialista em energia solar e equipamentos GoodWe.
    Responda à pergunta do usuário com base nas informações fornecidas e no contexto relevante.
    Se não tiver informações suficientes, diga isso claramente.

    Contexto relevante:
    {contexto}

    Pergunta do usuário:
    {pergunta}
    """

    try:
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return resposta.choices[0].message.content
    except Exception as e:
        return f"Ocorreu um erro: {e}"

# ==============================
# STREAMLIT APP
# ==============================
st.set_page_config(page_title="Energy_bot - GoodWe", page_icon="🔋")

st.title("🔋 Energy_bot - Assistente GoodWe")
st.write("Sou seu assistente sobre energia solar e equipamentos GoodWe. Faça sua pergunta!")

# Perguntas prontas
perguntas_prontas = [
    "Explique sobre o inversor híbrido GoodWe de 5kW.",
    "Como funciona a geração de energia com o painel solar de 550W?",
    "Qual a função da Bateria Lynx Home U no sistema de energia solar?",
    "Qual equipamento é adequado para armazenar energia?",
    "Onde posso encontrar informações sobre a instalação do inversor GW_XS G3?",
    "Quais são os inversores residenciais inteligentes da GoodWe mencionados nos manuais?",
    "Quais as características dos inversores da linha ES/EM/ET?",
    "Liste os equipamentos GoodWe"
]

# Interface
opcao = st.selectbox("Escolha uma pergunta pronta ou digite a sua:", ["Digite outra pergunta"] + perguntas_prontas)

if opcao == "Digite outra pergunta":
    pergunta_usuario = st.text_input("Digite sua pergunta aqui:")
else:
    pergunta_usuario = opcao

if st.button("Perguntar"):
    if pergunta_usuario.strip():
        resposta = chat_ia(pergunta_usuario)
        st.subheader("🤖 Resposta do Energy_bot:")
        st.write(resposta)
    else:
        st.warning("Digite ou selecione uma pergunta para continuar.")
