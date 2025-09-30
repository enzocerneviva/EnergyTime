# ==============================
# CHAT Energy_bot - Energia & GoodWe (Colab)
# ==============================

# Instalar dependências se necessário
!pip install openai -q # Removido openpyxl

import os
import openai
import pandas as pd
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from google.colab import userdata # Import userdata to access Colab secrets

# ==============================
os.environ["OPENAI_API_KEY"] = userdata.get('OPENAI_API_KEY')

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ==============================
# BASE DE DADOS DE EXEMPLO
# ==============================
dados = pd.DataFrame({
    "equipamento": ["Inversor GW5000", "Painel Solar 550W", "Bateria Lynx Home U"],
    "descricao": [
        "Inversor híbrido GoodWe de 5kW, alta eficiência e compatível com baterias.",
        "Módulo fotovoltaico monocristalino de 550W para geração de energia solar.",
        "Bateria de lítio para armazenamento de energia, modelo Lynx Home U da GoodWe."
    ]
})

# Removida a parte de carregamento e processamento de arquivos .xls
# xls_files = glob.glob("*.xls")
# novos_dados_lista = []
# ... (código removido)
# if novos_dados_lista:
#     ... (código removido)
# else:
#     print("⚠️ Nenhum dado processado foi carregado dos arquivos .xls.")


# ==============================
# FUNÇÃO: GERAR EMBEDDINGS
# ==============================
def gerar_embeddings(textos):
    if not textos:
        return []
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=textos
    )
    return [np.array(r.embedding) for r in response.data]

# Criar embeddings da base (apenas dados de exemplo)
dados["embedding"] = gerar_embeddings(dados["descricao"].tolist())

# ==============================
# FUNÇÃO: BUSCA (RAG)
# ==============================
def buscar_contexto(pergunta, top_k=3):
    if dados.empty:
        return "Nenhuma informação disponível na base de dados."
    valid_embeddings = [emb for emb in dados["embedding"] if isinstance(emb, np.ndarray)]
    if not valid_embeddings:
        return "Nenhuma informação útil na base de dados (embeddings ausentes)."

    emb_pergunta = gerar_embeddings([pergunta])[0]
    sims = cosine_similarity([emb_pergunta], valid_embeddings)[0]

    original_indices = [i for i, emb in enumerate(dados["embedding"]) if isinstance(emb, np.ndarray)]
    sorted_indices_in_valid = np.argsort(sims)[::-1]
    top_k_original_indices = [original_indices[i] for i in sorted_indices_in_valid[:top_k]]

    contextos = dados.iloc[top_k_original_indices]["descricao"].tolist()
    return "\n".join(contextos)

# ==============================
# FUNÇÃO: CHAT
# ==============================
def chat_ia(pergunta):
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

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return resposta.choices[0].message.content

# ==============================
# TESTE INTERATIVO
# ==============================

def main():
    perguntas_prontas = [
        "Explique sobre o inversor híbrido GoodWe de 5kW.",
        "Como funciona a geração de energia com o painel solar de 550W?",
        "Qual a função da Bateria Lynx Home U no sistema de energia solar?",
        "Qual equipamento é adequado para armazenar energia?",
    ]

    print("Olá! Sou seu assistente sobre energia solar e equipamentos GoodWe.")
    print("Como posso ajudar hoje?")

    while True:
        print("\nEscolha uma opção ou digite a sua pergunta:")
        for i, pergunta in enumerate(perguntas_prontas):
            print(f"{i + 1}. {pergunta}")
        print(f"{len(perguntas_prontas) + 1}. Digitar outra pergunta")
        print(f"{len(perguntas_prontas) + 2}. Sair")

        escolha = input("Digite o número da sua escolha: ")

        if escolha == str(len(perguntas_prontas) + 2):
            print("\n🤖 Energy_bot: Foi um prazer ajudar! Tenha um ótimo dia!")
            break
        elif escolha.isdigit() and 1 <= int(escolha) <= len(perguntas_prontas):
            pergunta_usuario = perguntas_prontas[int(escolha) - 1]
            print(f"\n🧑 Você: {pergunta_usuario}")
            print(f"🤖 Energy_bot: {chat_ia(pergunta_usuario)}")
        elif escolha == str(len(perguntas_prontas) + 1):
            pergunta_usuario = input("Digite sua pergunta: ")
            if pergunta_usuario.lower() == 'sair':
                print("\n🤖 Energy_bot: Foi um prazer ajudar! Tenha um ótimo dia!")
                break
            print(f"\n🧑 Você: {pergunta_usuario}")
            print(f"🤖 Energy_bot: {chat_ia(pergunta_usuario)}")
        else:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    main()
