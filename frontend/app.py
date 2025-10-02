import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="EnergyTime", page_icon="logo_energytime.png", layout="wide")

# Sidebar
st.sidebar.image("logo_energytime.png", width=100)
st.sidebar.title("EnergyTime")  

paginas = st.sidebar.radio("", ["☰ Sobre", "📊 Análises", "🔌 Equipamentos GoodWe", "💡 Assistente Alexa","💬 IA Personalizada", "⚙️ Configurações"])

st.sidebar.markdown("---")

# Conteúdo principal
if paginas == "☰ Sobre":

    st.title("🌱 O que é a EnergyTime?")
    st.markdown("---")

    # Seção: Nosso Objetivo
    st.subheader("📌 Nosso Objetivo")
    st.write("""
    A EnergyTime conecta equipamentos de energia com assistentes virtuais, oferecendo ferramentas inovadoras para melhorar a experiência do usuário.  
    Queremos tornar a tecnologia sustentável acessível, prática e intuitiva, mesmo para quem não tem familiaridade com energia ou automação residencial.
    """)
    st.write("""
    Com nossas soluções, o usuário terá acesso a recursos como:  
    - Previsão de quedas de energia usando IA  
    - Controle de dispositivos via Alexa  
    - Respostas personalizadas sobre consumo e eficiência energética  
    - Entre outros recursos que facilitam a vida no dia a dia
    """)

    # Seção: Colaboração com a GoodWe
    st.subheader("🤝 Colaboração com a GoodWe")
    st.write("""
    Estamos integrando nossos sistemas com os carregadores, inversores e outros equipamentos da GoodWe, garantindo uma automação inteligente e confiável para o gerenciamento de energia.
    """)

    # Seção: Funcionalidades do Projeto
    # Seção: Funcionalidades do Projeto
    st.subheader("⚡ Funcionalidades do Nosso Projeto")
    st.write("""
    A EnergyTime oferece uma experiência completa para gestão de energia de forma prática e inteligente, tanto pelo site/app quanto pela Alexa. Entre as principais funcionalidades, destacamos:  

    - **Gráficos de energia e créditos**: acompanhe a energia gerada, consumida e a renda total com crédito da rede, tanto no último dia quanto no último mês.  
    - **Monitoramento de equipamentos em tempo real**: veja o status de cada dispositivo da sua casa, como a bateria principal, por exemplo, com a porcentagem de carga atual.  
    - **Previsão de quedas de energia**: receba alertas para o dia atual e o próximo, garantindo que você esteja sempre preparado.  
    - **Histórico de comunicações com a Alexa**: consulte todas as interações anteriores, mantendo o controle sobre os comandos e respostas.  
    - **IA personalizada para dúvidas e orientação**: converse sobre o funcionamento dos equipamentos e receba informações detalhadas sobre energia e eficiência diretamente no app ou site.
    """)

    # Seção: Sobre a Equipe
    st.subheader("👨‍💻 Sobre a Equipe")
    st.write("""
    Nosso time é formado por estudantes de Ciências da Computação apaixonados por tecnologia e sustentabilidade:  
    - Enzo Cerneviva  
    - Gustavo Cordeiro Braga  
    - Murilo Justino Arcanjo  
    - Rafael Quattrer Dalla Costa  
    """)
    st.write("Trabalhamos juntos para aproximar pessoas das tecnologias que tornam a energia mais inteligente e sustentável.")

    st.markdown("---")


    # Três colunas: logo1 | espaço | logo2
    col1, col2, a, b, c, d, e, f, g = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1])   

    with col1:
        st.image("logo_energytime.png", width=150)
    with col2:
        st.image("logo_goodwe.png", width=150)


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuração da página
st.set_page_config(layout="centered")
st.title("Equipamentos Goodwe")

# --- FUNÇÃO 1: RELATÓRIO MENSAL (Seu Código Original) ---
def show_battery_data_monthly():
    """Processa e exibe o Relatório Mensal da Bateria."""
    
    file_path = 'BaseDeDados_BATERIA_MENSAL.xls'
    
    try:
        df = pd.read_excel(file_path, engine="xlrd", header=None)
    except FileNotFoundError:
        st.error(f"ERRO: O arquivo '{file_path}' (Mensal) não foi encontrado. Verifique o caminho.")
        return
    
    # Processamento e Limpeza de Dados
    df.columns = ["Monthly Report", "Plant", "Classification", "Capacity(kW)", "PV(kWh)", "Sell(kWh)", "Buy(kWh)", "Consumption(kWh)", "In-House(kWh)", "Self-Cons. Ratio(%)", "Contribution Ratio(%)", "Income(EUR)"]
    df = df.iloc[20:-1].copy()

    cols_to_convert = ['Consumption(kWh)', 'PV(kWh)', 'Income(EUR)', 'Buy(kWh)', 'Sell(kWh)']
    for col in cols_to_convert:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df.dropna(subset=cols_to_convert, inplace=True) 
    
    df['Monthly Report'] = pd.to_datetime(df['Monthly Report'], format='%d.%m.%Y', errors='coerce')
    df.dropna(subset=['Monthly Report'], inplace=True)
    
    # Cálculos
    total_monthly_consumption_bat = df['Consumption(kWh)'].sum()
    number_of_days_bat = len(df)
    daily_average_consumption_bat = total_monthly_consumption_bat / number_of_days_bat
    total_income_bat = df['Income(EUR)'].sum()
    total_monthly_buy = df['Buy(kWh)'].sum()
    total_monthly_sell = df['Sell(kWh)'].sum()
    daily_average_buy = total_monthly_buy / number_of_days_bat
    daily_average_sell = total_monthly_sell / number_of_days_bat

    # Exibição do Gráfico
    st.subheader("Gráfico de Consumo e Produção (Mensal)")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df, x='Monthly Report', y='Consumption(kWh)', label='Consumo (Bateria)', ax=ax)
    sns.lineplot(data=df, x='Monthly Report', y='PV(kWh)', label='Produção (Bateria)', ax=ax)
    ax.set_xlabel('Data')
    ax.set_ylabel('Valor (kWh)')
    ax.set_title('Consumo e Produção da Bateria (Dados Mensais)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig) 

    # Exibição das Métricas
    st.subheader("Métricas de Desempenho")
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
        st.write(f"Energia Média Diária Vendida: **{daily_average_sell:.2f} kWh**")


# --- FUNÇÃO 2: RELATÓRIO DIÁRIO (ADAPTE SEU CÓDIGO AQUI) ---
def show_battery_data_daily():
    """
    Processa e exibe o Relatório Diário da Bateria.
    
    NOTA: O CÓDIGO ABAIXO É UM EXEMPLO GENÉRICO. VOCÊ DEVE SUBSTITUÍ-LO
    INTEIRAMENTE PELO SEU CÓDIGO DE PROCESSAMENTO DO RELATÓRIO DIÁRIO.
    """
    st.header("Relatório Diário")
    
    file_path_daily = 'BaseDeDados_BATERIA_DIARIA.xls'
    
    try:
        # Tenta carregar o arquivo diário
        df_daily = pd.read_excel(file_path_daily, engine="xlrd", header=None)
    except FileNotFoundError:
        st.error(f"ERRO: O arquivo '{file_path_daily}' (Diário) não foi encontrado. Verifique o caminho.")
        return
    
    # --------------------------------------------------------
    # *** SUBSTITUA ESTA SEÇÃO PELO SEU CÓDIGO DE PROCESSAMENTO DIÁRIO! ***
    # --------------------------------------------------------
    st.info("Aqui entrará o seu **código completo de processamento de dados diários**, incluindo limpeza, cálculos, e as chamadas do Streamlit (`st.pyplot`, `st.metric`, etc.) para exibir os resultados.")
    st.markdown("Exemplo de como ficaria a exibição de dados e gráficos:")
    
    # Exemplo: Simulação de Gráfico Diário
    st.subheader("Gráfico de Exemplo (Diário)")
    data_exemplo = pd.DataFrame({
        'Dia': pd.to_datetime(['2025-01-01', '2025-01-02', '2025-01-03']),
        'Geração': [10.5, 12.1, 9.8],
        'Consumo': [8.0, 7.5, 8.5]
    })
    
    fig_daily, ax_daily = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=data_exemplo, x='Dia', y='Geração', label='Geração', ax=ax_daily)
    sns.lineplot(data=data_exemplo, x='Dia', y='Consumo', label='Consumo', ax=ax_daily)
    ax_daily.set_title('Consumo e Produção da Bateria (Dados Diários - Simulação)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig_daily)
    # --------------------------------------------------------


# --- ESTRUTURA PRINCIPAL COM OS EXPANDERS (O Layout do "V") ---

# 1. EXPANDER PRINCIPAL PARA O INVERSOR
with st.expander("Inversor"):
    # Espaço para o Inversor (você pode colocar relatórios Mensal/Diário aqui também)
    st.subheader("Dados do inversor aqui")
    st.info("Coloque a chamada para o relatório do Inversor aqui.")

st.markdown("---") 

# 2. EXPANDER PRINCIPAL PARA A BATERIA
with st.expander("Bateria", expanded=True): # Inicia ABERTO para a Bateria, como na imagem
    
    st.header("Relatórios Detalhados da Bateria")
    
    # EXPANDER ANINHADO 1: RELATÓRIO MENSAL
    with st.expander("Relatório Mensal", expanded=True): # Inicia ABERTO
        show_battery_data_monthly()

    st.markdown("---") # Linha divisória
    
    # EXPANDER ANINHADO 2: RELATÓRIO DIÁRIO
    with st.expander("Relatório Diário"): # Inicia FECHADO
        show_battery_data_daily()
    
    st.markdown("""  
  """)
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

    st.title("Converse com a IA sobre qualquer dúvida sobre energia ou sobre os equipamentos")

elif paginas == "⚙️ Configurações":

    st.title("⚙️ Ajustes do sistema")

