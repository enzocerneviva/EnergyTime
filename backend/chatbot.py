# chatbot.py

import os
import numpy as np
import pandas as pd
from openai import OpenAI
from pypdf import PdfReader
from sklearn.metrics.pairwise import cosine_similarity

# ==============================
# FUNÇÃO: GERAR EMBEDDINGS
# ==============================
def gerar_embeddings(textos, client_instance):
    """Gera embeddings para uma lista de textos"""
    if not textos:
        return []
    valid_textos = [str(t) for t in textos if isinstance(t, (str, bytes))]
    if not valid_textos:
        return []

    try:
        response = client_instance.embeddings.create(
            model="text-embedding-3-small",
            input=valid_textos
        )
        return [np.array(r.embedding) for r in response.data]
    except Exception as e:
        print(f"ERRO: Erro ao gerar embeddings: {e}")
        return [None] * len(valid_textos)

# ==============================
# FUNÇÃO: CARREGAR E PROCESSAR DADOS (PDFs, etc.)
# ==============================
def load_data(pdf_paths, client_instance):
    """Carrega dados dos PDFs e gera embeddings"""
    
    # Base de dados de exemplo
    dados_exemplo_dict = {
        "equipamento": [
            "Inversor GW5000", "Painel Solar 550W", "Bateria Lynx Home U",
            "Inversor ET 10kW", "Bateria Lynx Home F Plus"
        ],
        "descricao": [
            "Inversor híbrido GoodWe GW5000 de 5kW...",
            "Módulo fotovoltaico monocristalino de 550W...",
            "Bateria de lítio GoodWe Lynx Home U...",
            "Inversor trifásico GoodWe ET de 10kW...",
            "Bateria de lítio GoodWe Lynx Home F Plus..."
        ],
        "fonte": ["exemplo", "exemplo", "exemplo", "exemplo", "exemplo"]
    }
    dados = pd.DataFrame(dados_exemplo_dict)
    
    # Processamento dos PDFs
    novos_dados_lista = []
    for pdf_path in pdf_paths:
        try:
            reader = PdfReader(pdf_path)
            for page_num in range(len(reader.pages)):
                text = reader.pages[page_num].extract_text()
                if text:
                    chunks = [text[i:i + 1000] for i in range(0, len(text), 1000)]
                    for chunk in chunks:
                        novos_dados_lista.append({
                            "equipamento": f"PDF_{os.path.basename(pdf_path)}",
                            "descricao": chunk,
                            "fonte": pdf_path
                        })
        except FileNotFoundError:
            print(f"AVISO: Arquivo PDF não encontrado: {pdf_path}")
        except Exception as e:
            print(f"AVISO: Erro ao processar {pdf_path}: {e}")

    if novos_dados_lista:
        novos_dados_df = pd.DataFrame(novos_dados_lista)
        dados = pd.concat([dados, novos_dados_df], ignore_index=True)

    # Embeddings
    dados["embedding"] = gerar_embeddings(dados["descricao"].tolist(), client_instance)
    dados.dropna(subset=["embedding"], inplace=True)
    dados.reset_index(drop=True, inplace=True)
    
    # Salva o dict de exemplo para a regra de negócio
    return dados, dados_exemplo_dict

# ==============================
# FUNÇÃO: BUSCA (RAG)
# ==============================
def buscar_contexto(pergunta, dados_do_rag, client_instance, top_k=3):
    """Busca contexto relevante com embeddings"""
    if dados_do_rag.empty:
        return "Nenhuma informação disponível na base de dados."

    valid_embeddings_df = dados_do_rag[dados_do_rag["embedding"].apply(lambda x: isinstance(x, np.ndarray))]
    if valid_embeddings_df.empty:
        return "Nenhuma informação útil (embeddings ausentes)."

    emb_pergunta_list = gerar_embeddings([pergunta], client_instance)
    if not emb_pergunta_list or emb_pergunta_list[0] is None:
        return "Não foi possível gerar embedding para a pergunta."
    emb_pergunta = emb_pergunta_list[0]

    sims = cosine_similarity([emb_pergunta], valid_embeddings_df["embedding"].tolist())[0]
    indices = np.argsort(sims)[::-1][:top_k]

    return "\n".join(valid_embeddings_df.iloc[indices]["descricao"].tolist())

# ==============================
# FUNÇÃO: CHAT (A FUNÇÃO PRINCIPAL)
# ==============================
def chat_ia(pergunta, dados_do_rag, dados_exemplo_dict, client_instance):
    pergunta_lower = pergunta.lower()

    # Regra de negócio simples
    if "produtos goodwe" in pergunta_lower or "equipamentos goodwe" in pergunta_lower:
        return "Aqui estão alguns dos equipamentos GoodWe que conheço:\n" + "\n".join(dados_exemplo_dict["equipamento"])

    # Processo RAG
    contexto = buscar_contexto(pergunta, dados_do_rag, client_instance)
    prompt = f"""
    Você é um assistente especialista em energia solar e equipamentos GoodWe.
    Use o contexto abaixo para responder de forma clara e confiável.

    Contexto:
    {contexto}

    Pergunta:
    {pergunta}
    """

    try:
        response = client_instance.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"ERRO: Erro no chat: {e}")
        return "⚠️ Ocorreu um erro ao gerar a resposta no servidor."