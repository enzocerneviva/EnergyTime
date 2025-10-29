import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import openai
import pandas as pd
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from pypdf import PdfReader  # Leitor de PDF
import streamlit as st 

# --- Configuração da página ---
st.set_page_config(page_title="EnergyTime", page_icon="logo_energytime.png", layout="wide")

# --- Sidebar ---
st.sidebar.image("logo_energytime.png", width=100)
st.sidebar.title("EnergyTime")  

paginas = st.sidebar.radio(
    "", 
    [ "🔌 Equipamentos GoodWe", "💡 Assistente Alexa", "💬 IA Personalizada"]
)

st.sidebar.markdown("---")

# Conteúdo principal

if paginas == "🔌 Equipamentos GoodWe":

    st.title("Equipamentos GoodWe")

    # ===========================
    # FUNÇÃO 1: RELATÓRIO MENSAL DA BATERIA
    # ===========================
    def show_battery_data_monthly():
        """Processa e exibe o Relatório Mensal da Bateria."""
        file_path = 'content/BaseDeDados_BATERIA_MENSAL.xls'
        try:
            df = pd.read_excel(file_path, engine="xlrd", header=None)
        except FileNotFoundError:
            st.error(f"ERRO: O arquivo '{file_path}' (Mensal) não foi encontrado. Verifique o caminho.")
            return
        
        # Processamento e Limpeza
        df.columns = [
            "Monthly Report", "Plant", "Classification", "Capacity(kW)", "PV(kWh)", 
            "Sell(kWh)", "Buy(kWh)", "Consumption(kWh)", "In-House(kWh)", 
            "Self-Cons. Ratio(%)", "Contribution Ratio(%)", "Income(EUR)"
        ]
        df = df.iloc[20:-1].copy()
        cols_to_convert = ['Consumption(kWh)', 'PV(kWh)', 'Income(EUR)', 'Buy(kWh)', 'Sell(kWh)']
        for col in cols_to_convert:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df.dropna(subset=cols_to_convert + ['Monthly Report'], inplace=True)
        df['Monthly Report'] = pd.to_datetime(df['Monthly Report'], format='%d.%m.%Y', errors='coerce')

        # Cálculos
        total_monthly_consumption_bat = df['Consumption(kWh)'].sum()
        number_of_days_bat = len(df)
        daily_average_consumption_bat = total_monthly_consumption_bat / number_of_days_bat
        total_income_bat = df['Income(EUR)'].sum()
        total_monthly_buy = df['Buy(kWh)'].sum()
        total_monthly_sell = df['Sell(kWh)'].sum()
        daily_average_buy = total_monthly_buy / number_of_days_bat
        daily_average_sell = total_monthly_sell / number_of_days_bat

        # Gráfico
        st.subheader("📊 Geração Solar x Consumo da Bateria (Mensal)")
        df_indexed = df.set_index("Monthly Report")
        st.line_chart(df_indexed[["PV(kWh)", "Consumption(kWh)"]])

        # Métricas
        st.subheader("⚡ Métricas de Desempenho")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Consumo Mensal Total", f"{total_monthly_consumption_bat:,.2f} kWh")
            st.metric("Consumo Médio Diário", f"{daily_average_consumption_bat:,.2f} kWh")
        with col2:
            st.metric("Renda Mensal Total", f"{total_income_bat:,.2f} EUR")
            st.metric("Energia Total Vendida", f"{total_monthly_sell:,.2f} kWh")
        with col3:
            st.metric("Energia Total Comprada", f"{total_monthly_buy:,.2f} kWh")
            st.metric("Energia Média Diária Comprada", f"{daily_average_buy:,.2f} kWh")
            st.write(f"⚡ Energia Média Diária Vendida: **{daily_average_sell:.2f} kWh**")

    # ===========================
    # FUNÇÃO 2: RELATÓRIO DIÁRIO DA BATERIA
    # ===========================
    def show_battery_data_daily():
        st.header("Relatório Diário")
        file_path_daily = 'content/BaseDeDados_BATERIA_DIARIA.xls'
        try:
            df_daily = pd.read_excel(file_path_daily, engine="xlrd", header=None)
        except FileNotFoundError:
            st.error(f"ERRO: O arquivo '{file_path_daily}' (Diário) não foi encontrado. Verifique o caminho.")
            return

        # Exemplo de simulação — substituir pelos dados reais depois
        st.subheader("📊 Consumo x Geração (Diário)")
        data_exemplo = pd.DataFrame({
            'Dia': pd.to_datetime(['2025-01-01', '2025-01-02', '2025-01-03']),
            'Geração': [10.5, 12.1, 9.8],
            'Consumo': [8.0, 7.5, 8.5]
        })
        df_indexed = data_exemplo.set_index("Dia")
        st.line_chart(df_indexed[["Geração", "Consumo"]])

        # Totais
        total_daily_generation = data_exemplo['Geração'].sum()
        total_daily_consumption = data_exemplo['Consumo'].sum()
        st.subheader("⚡ Totais Diários")
        colA, colB = st.columns(2)
        with colA:
            st.metric("Consumo Total", f"{total_daily_consumption:.2f} kWh")
        with colB:
            st.metric("Geração Total", f"{total_daily_generation:.2f} kWh")

    # ===========================
    # FUNÇÃO 3: RELATÓRIO MENSAL DO INVERSOR
    # ===========================
    def show_inverter_data_monthly():
        """Processa e exibe o Relatório Mensal do Inversor GoodWe."""
        file_path = 'content/BaseDeDados_INVERSOR_MENSAL.xls'
        try:
            df = pd.read_excel(file_path, engine="xlrd", header=None)
        except FileNotFoundError:
            st.error(f"ERRO: O arquivo '{file_path}' (Mensal do Inversor) não foi encontrado.")
            return

        # Processamento
        df.columns = ["Monthly Report", "Plant", "Classification", "Capacity(kW)", "Generation(kWh)", "Income(EUR)"]
        df = df.iloc[21:-1].copy()
        for col in ["Generation(kWh)", "Income(EUR)"]:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "."), errors="coerce")
        df.dropna(subset=["Monthly Report", "Generation(kWh)", "Income(EUR)"], inplace=True)
        df["Monthly Report"] = pd.to_datetime(df["Monthly Report"], format="%d.%m.%Y", errors="coerce")

        # Cálculos
        total_generation = df["Generation(kWh)"].sum()
        total_income = df["Income(EUR)"].sum()
        num_days = len(df)
        daily_avg_generation = total_generation / num_days if num_days > 0 else 0.0

        # Gráfico
        st.subheader("📊 Geração Mensal do Inversor")
        df_indexed = df.set_index("Monthly Report")
        st.line_chart(df_indexed["Generation(kWh)"])

        # Métricas
        st.subheader("⚡ Totais e Médias")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Geração Total", f"{total_generation:,.2f} kWh")
        with col2:
            st.metric("Geração Média Diária", f"{daily_avg_generation:,.2f} kWh")
        with col3:
            st.metric("Renda Total", f"{total_income:,.2f} EUR")

    # ===========================
    # ESTRUTURA PRINCIPAL COM EXPANDERS
    # ===========================
    with st.expander("Inversor", expanded=True):
        st.header("Relatórios Detalhados do Inversor")
        show_inverter_data_monthly()

    st.markdown("---")

    with st.expander("Bateria", expanded=True):
        st.header("Relatórios Detalhados da Bateria")
        with st.expander("Relatório Mensal", expanded=True):
            show_battery_data_monthly()
        st.markdown("---")
        with st.expander("Relatório Diário"):
            show_battery_data_daily()

    st.markdown("---")
    st.markdown("### ⚡ Previsão de Queda de Energia")
    col5, col6 = st.columns(2)
    with col5:
        st.metric(label="Hoje", value="Não", delta="Baseado em análise climática")
    with col6:
        st.metric(label="Amanhã", value="Sim", delta="Baseado em análise climática")


elif paginas == "💡 Assistente Alexa":

    URL_BACKEND = "https://energytime-challenge-01.onrender.com/historico"  # ajustar no deploy

    # Dicionário para traduzir intents em frases
    INTENT_MAP = {
        "LaunchRequest": "Abrir a skill da Alexa",
        "CheckWeatherIntent": "Quero saber a previsão de queda de energia",
        "GetStateIntent": "Estou em {estado}",
        "CheckInversorIntent": "Quero saber os dados do inversor",
        "StartChargingIntent": "Ligue o carregador",
        "StopChargingIntent": "Desligue o carregador"
    }

    st.set_page_config(page_title="Histórico Alexa", layout="wide")

    # Estilo das mensagens
    user_bg = "background-color:#1e3a8a; color:white; padding:10px; border-radius:10px; margin:5px;"
    alexa_bg = "background-color:#0f172a; color:white; padding:10px; border-radius:10px; margin:5px; font-style:italic; font-weight:400;"

    st.title("💬 Histórico de Interações Alexa")
    st.markdown("---")

    # Função para traduzir intent para frase de usuário
    def traduzir_entrada(entrada):
        # Caso seja só string (ex: "CheckWeatherIntent")
        if isinstance(entrada, str):
            return INTENT_MAP.get(entrada, entrada)

        # Caso seja dict (ex: {"GetStateIntent": {"estado": "são paulo"}})
        elif isinstance(entrada, dict):
            intent_name, slots = list(entrada.items())[0]
            frase = INTENT_MAP.get(intent_name, intent_name)

            # Substitui placeholders pelos valores dos slots
            if isinstance(slots, dict):
                for k, v in slots.items():
                    frase = frase.replace(f"{{{k}}}", v)
            return frase

        # Fallback
        return str(entrada)

    try:
        response = requests.get(URL_BACKEND)
        if response.status_code == 200:
            historico = response.json()
        else:
            historico = []
    except Exception as e:
        st.error(f"Erro ao conectar com o backend: {e}")
        historico = []

    if not historico:
        st.info("Nenhuma interação registrada ainda.")
    else:
        for registro in historico:
            col1, col2 = st.columns([1,1])

            with col1:
                frase_usuario = traduzir_entrada(registro["entrada"])
                st.markdown(
                    f"<div style='{user_bg}'>👤 <b>Usuário:</b> {frase_usuario}<br><small>{registro['timestamp']}</small></div>",
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    f"<div style='{alexa_bg}'>🤖 <b>Alexa:</b> {registro['resposta']}</div>",
                    unsafe_allow_html=True
                )

elif paginas == "💬 IA Personalizada":
    try:
        client = OpenAI(api_key="")
    except Exception:
        st.error("⚠️ Chave da API OpenAI não encontrada. Adicione-a em .streamlit/secrets.toml.")
        st.stop()

    # ==============================
    # FUNÇÃO: GERAR EMBEDDINGS
    # ==============================
    def gerar_embeddings(textos):
        """Gera embeddings para uma lista de textos"""
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

    # ==============================
    # BASE DE DADOS DE EXEMPLO E PDF
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

    @st.cache_resource
    def load_data(pdf_paths):
        """Carrega dados do dicionário + PDFs"""
        dados = pd.DataFrame(dados_exemplo_dict)

        for pdf_path in pdf_paths:
            novos_dados_lista = []
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
                st.warning(f"📂 Arquivo PDF não encontrado: {pdf_path}")
            except Exception as e:
                st.warning(f"⚠️ Erro ao processar {pdf_path}: {e}")

            if novos_dados_lista:
                novos_dados_df = pd.DataFrame(novos_dados_lista)
                dados = pd.concat([dados, novos_dados_df], ignore_index=True)

        # Embeddings
        dados["embedding"] = gerar_embeddings(dados["descricao"].tolist())
        dados.dropna(subset=["embedding"], inplace=True)
        dados.reset_index(drop=True, inplace=True)
        return dados

    # Arquivos de exemplo
    pdf_paths = [
        "content/GW_Commercial & Industrial Smart Inverter Solutions_User Manual-ET 15-30kW-PT.pdf",
        "content/GW_Residential Smart Inverter Solutions_User Manual-ES Uniq 3-6kW-PT.pdf"
    ]
    dados = load_data(pdf_paths)

    # ==============================
    # FUNÇÃO: BUSCA (RAG)
    # ==============================
    def buscar_contexto(pergunta, top_k=3):
        """Busca contexto relevante com embeddings"""
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

    # ==============================
    # FUNÇÃO: CHAT
    # ==============================
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

    # ==============================
    # INTERFACE STREAMLIT
    # ==============================
    st.title("🤖 Energy_bot - Assistente GoodWe")
    st.write("Pergunte sobre energia solar e equipamentos GoodWe!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("Digite sua pergunta..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        resposta = chat_ia(user_input)
        st.session_state.messages.append({"role": "assistant", "content": resposta})
        with st.chat_message("assistant"):
            st.markdown(resposta)



