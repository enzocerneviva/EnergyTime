# ==============================
# CHAT Energy_bot - Energia & GoodWe (Colab)
# ==============================

# Instalar dependências se necessário
!pip install openai pypdf -q # Adicionado pypdf

import os
import openai
import pandas as pd
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from google.colab import userdata
from pypdf import PdfReader # Importar PdfReader

# ==============================
# CONFIGURAÇÕES
# ==============================
# Coloque sua chave da OpenAI no Secrets Manager do Colab.
# Clique no ícone de chave (🔑) no painel à esquerda,
# adicione um novo segredo com o nome 'OPENAI_API_KEY' e cole sua chave lá.
# A linha abaixo irá carregar a chave automaticamente.
os.environ["OPENAI_API_KEY"] = userdata.get('OPENAI_API_KEY')

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ==============================
# BASE DE DADOS DE EXEMPLO E PDF
# ==============================
# Armazenar os dados de exemplo separadamente para fácil acesso
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
    "fonte": ["exemplo", "exemplo", "exemplo", "exemplo", "exemplo"] # Ajustado para ter o mesmo número de elementos
}

dados = pd.DataFrame(dados_exemplo_dict)


# --- Processamento do PDF 1 ---
pdf_path_1 = "/content/GW_XS G3_User Manual-PT.pdf"
novos_dados_lista_1 = []

try:
    reader_1 = PdfReader(pdf_path_1)
    for page_num in range(len(reader_1.pages)):
        page_1 = reader_1.pages[page_num]
        text_1 = page_1.extract_text()
        if text_1:
            # Dividir texto em chunks menores (ajustar conforme necessário)
            chunks_1 = [text_1[i:i + 1000] for i in range(0, len(text_1), 1000)]
            for chunk_1 in chunks_1:
                 novos_dados_lista_1.append({"equipamento": "PDF_Manual_XS_G3", "descricao": chunk_1, "fonte": pdf_path_1})

except Exception as e:
    print(f"Erro ao processar o PDF 1 ({pdf_path_1}): {e}")
    print("⚠️ Nenhum dado do PDF 1 foi carregado.")

if novos_dados_lista_1:
    novos_dados_df_1 = pd.DataFrame(novos_dados_lista_1)
    dados = pd.concat([dados, novos_dados_df_1], ignore_index=True)
    print(f"✅ {len(novos_dados_lista_1)} trechos de texto do PDF 1 carregados e adicionados à base de dados.")
else:
    print(f"⚠️ Nenhum dado processado foi carregado do arquivo PDF 1 ({pdf_path_1}).")

# --- Processamento do PDF 2 ---
pdf_path_2 = "/content/GW_Residential Smart Inverter Solutions_User Manual-ES Uniq 3-6kW-PT.pdf"
novos_dados_lista_2 = []

try:
    reader_2 = PdfReader(pdf_path_2)
    for page_num in range(len(reader_2.pages)):
        page_2 = reader_2.pages[page_num]
        text_2 = page_2.extract_text()
        if text_2:
            # Dividir texto em chunks menores (ajustar conforme necessário)
            chunks_2 = [text_2[i:i + 1000] for i in range(0, len(text_2), 1000)]
            for chunk_2 in chunks_2:
                 novos_dados_lista_2.append({"equipamento": "PDF_Manual_Uniq", "descricao": chunk_2, "fonte": pdf_path_2})

except Exception as e:
    print(f"Erro ao processar o PDF 2 ({pdf_path_2}): {e}")
    print("⚠️ Nenhum dado do PDF 2 foi carregado.")

if novos_dados_lista_2:
    novos_dados_df_2 = pd.DataFrame(novos_dados_lista_2)
    dados = pd.concat([dados, novos_dados_df_2], ignore_index=True)
    print(f"✅ {len(novos_dados_lista_2)} trechos de texto do PDF 2 carregados e adicionados à base de dados.")
else:
    print(f"⚠️ Nenhum dado processado foi carregado do arquivo PDF 2 ({pdf_path_2}).")

# ==============================
# FUNÇÃO: GERAR EMBEDDINGS
# ==============================
def gerar_embeddings(textos):
    if not textos:
        return []
    # Certifique-se de que os textos são strings antes de enviar para a API
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
        print(f"Erro ao gerar embeddings: {e}")
        return [None] * len(valid_textos) # Retorna None para indicar falha


# Criar embeddings da base (dados de exemplo + dados do PDF)
# Gerar embeddings para todos os dados (incluindo os dos PDFs)
dados["embedding"] = gerar_embeddings(dados["descricao"].tolist())

# Remover linhas onde a geração de embedding falhou
dados.dropna(subset=["embedding"], inplace=True)
dados.reset_index(drop=True, inplace=True)

# ==============================
# FUNÇÃO: BUSCA (RAG)
# ==============================
def buscar_contexto(pergunta, top_k=3):
    if dados.empty:
        return "Nenhuma informação disponível na base de dados."
    # Filtrar embeddings válidos
    valid_embeddings_df = dados[dados["embedding"].apply(lambda x: isinstance(x, np.ndarray))]
    if valid_embeddings_df.empty:
         return "Nenhuma informação útil na base de dados (embeddings ausentes ou inválidos)."

    valid_embeddings = valid_embeddings_df["embedding"].tolist()

    try:
        emb_pergunta_list = gerar_embeddings([pergunta])
        if not emb_pergunta_list:
             return "Não foi possível gerar embedding para a pergunta."
        emb_pergunta = emb_pergunta_list[0]

        sims = cosine_similarity([emb_pergunta], valid_embeddings)[0]

        sorted_indices_in_valid = np.argsort(sims)[::-1]
        top_k_indices_in_valid = sorted_indices_in_valid[:top_k]

        # Mapear de volta para os índices originais no DataFrame 'dados'
        top_k_original_indices = valid_embeddings_df.iloc[top_k_indices_in_valid].index.tolist()


        contextos = dados.loc[top_k_original_indices]["descricao"].tolist()
        return "\n".join(contextos)
    except Exception as e:
        print(f"Erro durante a busca de contexto: {e}")
        return "Ocorreu um erro ao buscar informações relevantes."


# ==============================
# FUNÇÃO: CHAT
# ==============================
def chat_ia(pergunta):
    # Converter a pergunta para minúsculas para comparação sem distinção de maiúsculas/minúsculas
    pergunta_lower = pergunta.lower()

    # Verificar se a pergunta é sobre listar produtos/equipamentos da base inicial
    if "produtos goodwe" in pergunta_lower or "equipamentos goodwe" in pergunta_lower or "quais sao os produtos" in pergunta_lower or "quais sao os equipamentos" in pergunta_lower:
        if dados_exemplo_dict and "equipamento" in dados_exemplo_dict:
            lista_equipamentos = "\n".join(dados_exemplo_dict["equipamento"])
            return f"Aqui estão alguns dos equipamentos GoodWe que conheço:\n{lista_equipamentos}"
        else:
            return "Não tenho uma lista específica de equipamentos GoodWe na minha base inicial."


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
        print(f"Erro ao gerar resposta do chat: {e}")
        return "Ocorreu um erro ao tentar gerar a resposta."


# ==============================
# TESTE INTERATIVO
# ==============================

def main():
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
            print(f"\n Você: {pergunta_usuario}")
            print(f"🤖 Energy_bot: {chat_ia(pergunta_usuario)}")
        elif escolha == str(len(perguntas_prontas) + 1):
            pergunta_usuario = input("Digite sua pergunta: ")
            if pergunta_usuario.lower() == 'sair':
                print("\n🤖 Energy_bot: Foi um prazer ajudar! Tenha um ótimo dia!")
                break
            print(f"\n Você: {pergunta_usuario}")
            print(f"🤖 Energy_bot: {chat_ia(pergunta_usuario)}")
        else:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    main()
