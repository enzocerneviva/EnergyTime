# app.py

import streamlit as st
import requests  # Para chamar nossa API Flask
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
# import openai  -> REMOVIDO
# from openai import OpenAI -> REMOVIDO
# from sklearn.metrics.pairwise import cosine_similarity -> REMOVIDO
# import numpy as np -> REMOVIDO
# from pypdf import PdfReader -> REMOVIDO
import streamlit as st 

# --- Configuração da página (Igual) ---
st.set_page_config(page_title="EnergyTime", page_icon="logo_energytime.png", layout="wide")

# --- Sidebar (Igual) ---
st.sidebar.image("logo_energytime.png", width=100)
st.sidebar.title("EnergyTime") 
paginas = st.sidebar.radio(
    "", 
    [ "🔌 Equipamentos GoodWe", "💡 Assistente Alexa", "💬 IA Personalizada"]
)
st.sidebar.markdown("---")

# --- Página 1: Equipamentos (Igual por enquanto) ---
if paginas == "🔌 Equipamentos GoodWe":
    # (Todo o seu código de 'pd.read_excel' e 'st.metric' continua aqui...)
    # (Nosso próximo passo será mover esta lógica para a API também!)
    st.title("Equipamentos GoodWe")
    def show_battery_data_monthly():
        file_path = 'content/BaseDeDados_BATERIA_MENSAL.xls'
        try: df = pd.read_excel(file_path, engine="xlrd", header=None)
        except FileNotFoundError:
            st.error(f"ERRO: O arquivo '{file_path}' (Mensal) não foi encontrado. Verifique o caminho.")
            return
        df.columns = ["Monthly Report", "Plant", "Classification", "Capacity(kW)", "PV(kWh)", "Sell(kWh)", "Buy(kWh)", "Consumption(kWh)", "In-House(kWh)", "Self-Cons. Ratio(%)", "Contribution Ratio(%)", "Income(EUR)"]
        df = df.iloc[20:-1].copy()
        cols_to_convert = ['Consumption(kWh)', 'PV(kWh)', 'Income(EUR)', 'Buy(kWh)', 'Sell(kWh)']
        for col in cols_to_convert: df[col] = pd.to_numeric(df[col], errors='coerce')
        df.dropna(subset=cols_to_convert + ['Monthly Report'], inplace=True); df['Monthly Report'] = pd.to_datetime(df['Monthly Report'], format='%d.%m.%Y', errors='coerce')
        total_monthly_consumption_bat = df['Consumption(kWh)'].sum(); number_of_days_bat = len(df); daily_average_consumption_bat = total_monthly_consumption_bat / number_of_days_bat; total_income_bat = df['Income(EUR)'].sum(); total_monthly_buy = df['Buy(kWh)'].sum(); total_monthly_sell = df['Sell(kWh)'].sum(); daily_average_buy = total_monthly_buy / number_of_days_bat; daily_average_sell = total_monthly_sell / number_of_days_bat
        st.subheader("📊 Geração Solar x Consumo da Bateria (Mensal)"); df_indexed = df.set_index("Monthly Report"); st.line_chart(df_indexed[["PV(kWh)", "Consumption(kWh)"]])
        st.subheader("⚡ Métricas de Desempenho"); col1, col2, col3 = st.columns(3)
        with col1: st.metric("Consumo Mensal Total", f"{total_monthly_consumption_bat:,.2f} kWh"); st.metric("Consumo Médio Diário", f"{daily_average_consumption_bat:,.2f} kWh")
        with col2: st.metric("Renda Mensal Total", f"{total_income_bat:,.2f} EUR"); st.metric("Energia Total Vendida", f"{total_monthly_sell:,.2f} kWh")
        with col3: st.metric("Energia Total Comprada", f"{total_monthly_buy:,.2f} kWh"); st.metric("Energia Média Diária Comprada", f"{daily_average_buy:,.2f} kWh"); st.write(f"⚡ Energia Média Diária Vendida: **{daily_average_sell:.2f} kWh**")
    def show_battery_data_daily():
        st.header("Relatório Diário"); file_path_daily = 'content/BaseDeDados_BATERIA_DIARIA.xls'
        try: df_daily = pd.read_excel(file_path_daily, engine="xlrd", header=None)
        except FileNotFoundError: st.error(f"ERRO: O arquivo '{file_path_daily}' (Diário) não foi encontrado."); return
        st.subheader("📊 Consumo x Geração (Diário)"); data_exemplo = pd.DataFrame({'Dia': pd.to_datetime(['2025-01-01', '2025-01-02', '2025-01-03']), 'Geração': [10.5, 12.1, 9.8], 'Consumo': [8.0, 7.5, 8.5]}); df_indexed = data_exemplo.set_index("Dia"); st.line_chart(df_indexed[["Geração", "Consumo"]])
        total_daily_generation = data_exemplo['Geração'].sum(); total_daily_consumption = data_exemplo['Consumo'].sum()
        st.subheader("⚡ Totais Diários"); colA, colB = st.columns(2)
        with colA: st.metric("Consumo Total", f"{total_daily_consumption:.2f} kWh")
        with colB: st.metric("Geração Total", f"{total_daily_generation:.2f} kWh")
    def show_inverter_data_monthly():
        file_path = 'content/BaseDeDados_INVERSOR_MENSAL.xls'
        try: df = pd.read_excel(file_path, engine="xlrd", header=None)
        except FileNotFoundError: st.error(f"ERRO: O arquivo '{file_path}' (Mensal do Inversor) não foi encontrado."); return
        df.columns = ["Monthly Report", "Plant", "Classification", "Capacity(kW)", "Generation(kWh)", "Income(EUR)"]; df = df.iloc[21:-1].copy()
        for col in ["Generation(kWh)", "Income(EUR)"]: df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "."), errors="coerce")
        df.dropna(subset=["Monthly Report", "Generation(kWh)", "Income(EUR)"], inplace=True); df["Monthly Report"] = pd.to_datetime(df["Monthly Report"], format="%d.%m.%Y", errors="coerce")
        total_generation = df["Generation(kWh)"].sum(); total_income = df["Income(EUR)"].sum(); num_days = len(df); daily_avg_generation = total_generation / num_days if num_days > 0 else 0.0
        st.subheader("📊 Geração Mensal do Inversor"); df_indexed = df.set_index("Monthly Report"); st.line_chart(df_indexed["Generation(kWh)"])
        st.subheader("⚡ Totais e Médias"); col1, col2, col3 = st.columns(3)
        with col1: st.metric("Geração Total", f"{total_generation:,.2f} kWh")
        with col2: st.metric("Geração Média Diária", f"{daily_avg_generation:,.2f} kWh")
        with col3: st.metric("Renda Total", f"{total_income:,.2f} EUR")
    with st.expander("Inversor", expanded=True): st.header("Relatórios Detalhados do Inversor"); show_inverter_data_monthly()
    st.markdown("---")
    with st.expander("Bateria", expanded=True):
        st.header("Relatórios Detalhados da Bateria")
        with st.expander("Relatório Mensal", expanded=True): show_battery_data_monthly()
        st.markdown("---")
        with st.expander("Relatório Diário"): show_battery_data_daily()
    st.markdown("---")
    st.markdown("### ⚡ Previsão de Queda de Energia") # (Próximo passo: conectar na API)
    col5, col6 = st.columns(2)
    with col5: st.metric(label="Hoje", value="Não", delta="Baseado em análise climática")
    with col6: st.metric(label="Amanhã", value="Sim", delta="Baseado em análise climática")

# --- Página 2: Alexa (Igual) ---
elif paginas == "💡 Assistente Alexa":
    # (Seu código original, que já é um cliente de API. Perfeito!)
    URL_BACKEND = "https://energytime-challenge-01.onrender.com/historico" 
    INTENT_MAP = {
        "LaunchRequest": "Abrir a skill da Alexa",
        "CheckWeatherIntent": "Quero saber a previsão de queda de energia",
        "GetStateIntent": "Estou em {estado}",
        "CheckInversorIntent": "Quero saber os dados do inversor",
        "StartChargingIntent": "Ligue o carregador",
        "StopChargingIntent": "Desligue o carregador"
    }
    #... (resto do seu código da página Alexa) ...
    user_bg = "background-color:#1e3a8a; color:white; padding:10px; border-radius:10px; margin:5px;"
    alexa_bg = "background-color:#0f172a; color:white; padding:10px; border-radius:10px; margin:5px; font-style:italic; font-weight:400;"
    st.title("💬 Histórico de Interações Alexa")
    st.markdown("---")
    def traduzir_entrada(entrada):
        if isinstance(entrada, str): return INTENT_MAP.get(entrada, entrada)
        elif isinstance(entrada, dict):
            intent_name, slots = list(entrada.items())[0]; frase = INTENT_MAP.get(intent_name, intent_name)
            if isinstance(slots, dict):
                for k, v in slots.items(): frase = frase.replace(f"{{{k}}}", v)
            return frase
        return str(entrada)
    try:
        response = requests.get(URL_BACKEND)
        historico = response.json() if response.status_code == 200 else []
    except Exception as e: st.error(f"Erro ao conectar com o backend: {e}"); historico = []
    if not historico: st.info("Nenhuma interação registrada ainda.")
    else:
        for registro in historico:
            col1, col2 = st.columns([1,1])
            with col1: frase_usuario = traduzir_entrada(registro["entrada"]); st.markdown(f"<div style='{user_bg}'>👤 <b>Usuário:</b> {frase_usuario}<br><small>{registro['timestamp']}</small></div>", unsafe_allow_html=True)
            with col2: st.markdown(f"<div style='{alexa_bg}'>🤖 <b>Alexa:</b> {registro['resposta']}</div>", unsafe_allow_html=True)


# --- Página 3: IA Personalizada (TOTALMENTE MODIFICADA) ---
elif paginas == "💬 IA Personalizada":

    # --- TODA A LÓGICA DE IA FOI REMOVIDA DAQUI ---
    # - client = OpenAI(...) -> REMOVIDO
    # - def gerar_embeddings(...) -> REMOVIDO
    # - def load_data(...) -> REMOVIDO
    # - def buscar_contexto(...) -> REMOVIDO
    # - def chat_ia(...) -> REMOVIDO
    # - pdf_paths = [...] -> REMOVIDO
    # - dados = load_data(...) -> REMOVIDO
    
    # URL do nosso backend Flask (rodando na porta 10000)
    # Se o Streamlit e o Flask estiverem em máquinas diferentes, 
    # troque '127.0.0.1' pelo IP do servidor backend.
    URL_BACKEND_CHAT = "http://127.0.0.1:10000/chat_ia"

    # --- INTERFACE STREAMLIT (ÚNICA COISA QUE SOBRA) ---
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
            
        # --- LÓGICA DE CHAMADA DE API (O "GARÇOM") ---
        try:
            with st.spinner("Energy_bot está pensando..."):
                # 1. Envia a pergunta para o backend Flask
                response = requests.post(
                    URL_BACKEND_CHAT,
                    json={"pergunta": user_input} 
                )
                response.raise_for_status() # Lança erro se a API falhar (ex: 404, 500)

                # 2. Pega a resposta do JSON
                resposta_ia = response.json().get("resposta", "Erro ao decodificar resposta do servidor.")
                
        except requests.exceptions.ConnectionError:
            resposta_ia = "⚠️ **Erro de Conexão:** Não foi possível conectar ao servidor de IA. O backend (main.py) está rodando?"
        except requests.exceptions.RequestException as e:
            resposta_ia = f"⚠️ **Erro de API:** {e}"
        except Exception as e:
            resposta_ia = f"⚠️ **Erro Inesperado:** {e}"
        # --- FIM DA LÓGICA DE API ---

        # 3. Mostra a resposta na tela
        st.session_state.messages.append({"role": "assistant", "content": resposta_ia})
        with st.chat_message("assistant"):
            st.markdown(resposta_ia)