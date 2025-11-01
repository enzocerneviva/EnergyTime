import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# --- URLs DO BACKEND ---
# (Definimos as constantes aqui para a página funcionar)
URL_BACKEND_CHAT_LOCAL = "http://127.0.0.1:10000/chat_ia"
URL_BACKEND_HISTORICO_LOCAL = "http://127.0.0.1:10000/historico"
URL_BACKEND_CHAT = "https://energytime-challenge-01.onrender.com/chat_ia"
URL_BACKEND_HISTORICO = "https://energytime-challenge-01.onrender.com/historico"

def render_principal_page():
    """
    Renderiza TODO o seu aplicativo principal (o app.py antigo).
    Esta função será chamada pelo app.py "controlador" se o utilizador ESTIVER logado.
    """

    # --- 1. GUARDIÃO DE LOGIN ---
    # (Verifica se o utilizador está logado, estado que será definido pelo app.py)
    if not st.session_state.get("autenticado", False):
        st.error("🔒 Acesso Negado")
        st.info("Por favor, faça o login para aceder ao dashboard.")
        
        # (Este botão só funcionará quando o app.py for o controlador)
        if st.button("Ir para o Login"):
            st.session_state.pagina_atual = "login" # Diz ao controlador para onde ir
            st.rerun()
        st.stop() # Para a execução aqui

    # --- 2. SEU CÓDIGO ORIGINAL (AGORA DENTRO DA FUNÇÃO) ---

    # (st.set_page_config FOI REMOVIDO DAQUI. Ficará no app.py controlador)

    # --- Sidebar (com Logout) ---
    st.sidebar.image("logo_energytime.png", width=100)
    st.sidebar.title("EnergyTime") 
    # Mostra quem está logado (variável vem do st.session_state)
    st.sidebar.success(f"Logado como: {st.session_state.get('user_id', 'Utilizador')}")
    
    paginas = st.sidebar.radio(
        "", 
        [ "🔌 Equipamentos GoodWe", "💡 Assistente Alexa", "💬 IA Personalizada"]
    )
    st.sidebar.markdown("---")
    
    # Adicionado botão de Logout
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.autenticado = False
        st.session_state.user_id = None
        st.session_state.pagina_atual = "bem_vindo" # Diz ao controlador para onde ir
        st.rerun() # Recarrega o app.py, que mostrará a pág. de login/boas-vindas

    # --- Página 1: Equipamentos ---
    if paginas == "🔌 Equipamentos GoodWe":
        st.title("Equipamentos GoodWe")
        
        # --- Funções de processamento de dados (aninhadas) ---
        # (No futuro, moveremos isto para o backend)
        def show_battery_data_monthly():
            file_path = os.path.join('content', 'BaseDeDados_BATERIA_MENSAL.xls')
            try: 
                df = pd.read_excel(file_path, engine="xlrd", header=None)
            except FileNotFoundError:
                st.error(f"ERRO: O ficheiro '{file_path}' (Mensal) não foi encontrado. Verifique o caminho.")
                return
            except Exception as e:
                st.error(f"Erro ao ler o ficheiro {file_path}: {e}")
                return
            
            df.columns = ["Monthly Report", "Plant", "Classification", "Capacity(kW)", "PV(kWh)", "Sell(kWh)", "Buy(kWh)", "Consumption(kWh)", "In-House(kWh)", "Self-Cons. Ratio(%)", "Contribution Ratio(%)", "Income(EUR)"]
            df = df.iloc[20:-1].copy()
            cols_to_convert = ['Consumption(kWh)', 'PV(kWh)', 'Income(EUR)', 'Buy(kWh)', 'Sell(kWh)']
            for col in cols_to_convert: df[col] = pd.to_numeric(df[col], errors='coerce')
            df.dropna(subset=cols_to_convert + ['Monthly Report'], inplace=True); df['Monthly Report'] = pd.to_datetime(df['Monthly Report'], format='%d.%m.%Y', errors='coerce')
            
            number_of_days_bat = len(df)
            if number_of_days_bat == 0: 
                st.warning("Não há dados mensais de bateria para exibir.")
                return # Evita divisão por zero
                
            total_monthly_consumption_bat = df['Consumption(kWh)'].sum(); daily_average_consumption_bat = total_monthly_consumption_bat / number_of_days_bat; total_income_bat = df['Income(EUR)'].sum(); total_monthly_buy = df['Buy(kWh)'].sum(); total_monthly_sell = df['Sell(kWh)'].sum(); daily_average_buy = total_monthly_buy / number_of_days_bat; daily_average_sell = total_monthly_sell / number_of_days_bat
            st.subheader("📊 Geração Solar x Consumo da Bateria (Mensal)"); df_indexed = df.set_index("Monthly Report"); st.line_chart(df_indexed[["PV(kWh)", "Consumption(kWh)"]])
            st.subheader("⚡ Métricas de Desempenho"); col1, col2, col3 = st.columns(3)
            with col1: st.metric("Consumo Mensal Total", f"{total_monthly_consumption_bat:,.2f} kWh"); st.metric("Consumo Médio Diário", f"{daily_average_consumption_bat:,.2f} kWh")
            with col2: st.metric("Renda Mensal Total", f"{total_income_bat:,.2f} EUR"); st.metric("Energia Total Vendida", f"{total_monthly_sell:,.2f} kWh")
            with col3: st.metric("Energia Total Comprada", f"{total_monthly_buy:,.2f} kWh"); st.metric("Energia Média Diária Comprada", f"{daily_average_buy:,.2f} kWh"); st.write(f"⚡ Energia Média Diária Vendida: **{daily_average_sell:.2f} kWh**")
        
        def show_battery_data_daily():
            st.header("Relatório Diário"); file_path_daily = os.path.join('content', 'BaseDeDados_BATERIA_DIARIA.xls')
            try: 
                df_daily = pd.read_excel(file_path_daily, engine="xlrd", header=None)
            except FileNotFoundError: 
                st.error(f"ERRO: O ficheiro '{file_path_daily}' (Diário) não foi encontrado."); return
            except Exception as e:
                st.error(f"Erro ao ler o ficheiro {file_path_daily}: {e}")
                return
                
            st.subheader("📊 Consumo x Geração (Diário)"); data_exemplo = pd.DataFrame({'Dia': pd.to_datetime(['2025-01-01', '2025-01-02', '2025-01-03']), 'Geração': [10.5, 12.1, 9.8], 'Consumo': [8.0, 7.5, 8.5]}); df_indexed = data_exemplo.set_index("Dia"); st.line_chart(df_indexed[["Geração", "Consumo"]])
            total_daily_generation = data_exemplo['Geração'].sum(); total_daily_consumption = data_exemplo['Consumo'].sum()
            st.subheader("⚡ Totais Diários"); colA, colB = st.columns(2)
            with colA: st.metric("Consumo Total", f"{total_daily_consumption:.2f} kWh")
            with colB: st.metric("Geração Total", f"{total_daily_generation:.2f} kWh")
        
        def show_inverter_data_monthly():
            file_path = os.path.join('content', 'BaseDeDados_INVERSOR_MENSAL.xls')
            try: 
                df = pd.read_excel(file_path, engine="xlrd", header=None)
            except FileNotFoundError: 
                st.error(f"ERRO: O ficheiro '{file_path}' (Mensal do Inversor) não foi encontrado."); return
            except Exception as e:
                st.error(f"Erro ao ler o ficheiro {file_path}: {e}")
                return
                
            df.columns = ["Monthly Report", "Plant", "Classification", "Capacity(kW)", "Generation(kWh)", "Income(EUR)"]; df = df.iloc[21:-1].copy()
            for col in ["Generation(kWh)", "Income(EUR)"]: df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "."), errors="coerce")
            df.dropna(subset=["Monthly Report", "Generation(kWh)", "Income(EUR)"], inplace=True); df["Monthly Report"] = pd.to_datetime(df["Monthly Report"], format="%d.%m.%Y", errors="coerce")
            
            num_days = len(df)
            if num_days == 0: 
                st.warning("Não há dados mensais de inversor para exibir.")
                return # Evita divisão por zero
                
            total_generation = df["Generation(kWh)"].sum(); total_income = df["Income(EUR)"].sum(); daily_avg_generation = total_generation / num_days
            st.subheader("📊 Geração Mensal do Inversor"); df_indexed = df.set_index("Monthly Report"); st.line_chart(df_indexed["Generation(kWh)"])
            st.subheader("⚡ Totais e Médias"); col1, col2, col3 = st.columns(3)
            with col1: st.metric("Geração Total", f"{total_generation:,.2f} kWh")
            with col2: st.metric("Geração Média Diária", f"{daily_avg_generation:,.2f} kWh")
            with col3: st.metric("Renda Total", f"{total_income:,.2f} EUR")
            
        # --- Layout da Página de Equipamentos ---
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
        st.markdown("### ⚡ Previsão de Queda de Energia (WIP)")
        st.info("Aqui vamos conectar o modelo de previsão que fizemos no `ia_engine.py`")
        col5, col6 = st.columns(2)
        with col5: st.metric(label="Hoje", value="Não", delta="Baseado em análise climática")
        with col6: st.metric(label="Amanhã", value="Sim", delta="Baseado em análise climática")

    # --- Página 2: Alexa ---
    elif paginas == "💡 Assistente Alexa":
        st.title("💡 Histórico de Interações Alexa")
        URL_BACKEND = URL_BACKEND_HISTORICO # Usa a constante
        INTENT_MAP = {
            "LaunchRequest": "Abrir a skill da Alexa",
            "CheckWeatherIntent": "Quero saber a previsão de queda de energia",
            "GetStateIntent": "Estou em {estado}",
            "CheckInversorIntent": "Quero saber os dados do inversor",
            "StartChargingIntent": "Ligue o carregador",
            "StopChargingIntent": "Desligue o carregador"
        }
        user_bg = "background-color:#1e3a8a; color:white; padding:10px; border-radius:10px; margin:5px;"
        alexa_bg = "background-color:#0f172a; color:white; padding:10px; border-radius:10px; margin:5px; font-style:italic; font-weight:400;"
        
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
        except Exception as e: 
            st.error(f"Erro ao conectar com o backend: {e}"); historico = []
            
        if not historico: 
            st.info("Nenhuma interação registada ainda.")
        else:
            for registro in historico:
                col1, col2 = st.columns([1,1])
                with col1: 
                    frase_usuario = traduzir_entrada(registro["entrada"])
                    st.markdown(f"<div style='{user_bg}'>👤 <b>Utilizador:</b> {frase_usuario}<br><small>{registro['timestamp']}</small></div>", unsafe_allow_html=True)
                with col2: 
                    st.markdown(f"<div style='{alexa_bg}'>🤖 <b>Alexa:</b> {registro['resposta']}</div>", unsafe_allow_html=True)

    # --- Página 3: IA Personalizada ---
    elif paginas == "💬 IA Personalizada":
        st.title("🤖 EnergyTimeAi - Assistente GoodWe")
        st.write("Pergunte sobre energia solar e equipamentos GoodWe!")

        # Renomeado para 'messages_dashboard' para não conflitar
        # com o chat da página de login.
        if "messages_dashboard" not in st.session_state:
            st.session_state.messages_dashboard = []

        for message in st.session_state.messages_dashboard:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if user_input := st.chat_input("Digite sua pergunta..."):
            st.session_state.messages_dashboard.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)
            
            try:
                with st.spinner("Energy_bot está a pensar..."):
                    response = requests.post(
                        URL_BACKEND_CHAT_LOCAL, # Usa a constante
                        json={"pergunta": user_input} 
                    )
                    response.raise_for_status()
                    resposta_ia = response.json().get("resposta", "Erro ao descodificar resposta do servidor.")
            except requests.exceptions.ConnectionError:
                resposta_ia = "⚠️ **Erro de Conexão:** Não foi possível conectar ao servidor de IA. O backend (main.py) está a funcionar?"
            except requests.exceptions.RequestException as e:
                resposta_ia = f"⚠️ **Erro de API:** {e}"
            except Exception as e:
                resposta_ia = f"⚠️ **Erro Inesperado:** {e}"

            st.session_state.messages_dashboard.append({"role": "assistant", "content": resposta_ia})
            with st.chat_message("assistant"):
                st.markdown(resposta_ia)
