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


elif paginas == "📊 Análises":

    st.title("📊 Visualização dos Dados")
    st.markdown("---")
    
    st.markdown("## Análise Mensal de Consumo e Geração Solar")
 
    # --- Carregar a planilha mensal ---
    try:
        df = pd.read_excel("content/BaseDeDados_BATERIA_MENSAL.xls", header=None)
    
        # Assuming the header is in the 21st row (index 20) based on previous cells
        df.columns = ["Monthly Report", "Plant", "Classification", "Capacity(kW)", "PV(kWh)", "Sell(kWh)", "Buy(kWh)", "Consumption(kWh)", "In-House(kWh)", "Self-Cons. Ratio(%)", "Contribution Ratio(%)", "Income(EUR)"]
    
        # Remove unnecessary rows (up to row 20 and the last row) and the row with 'Date'
        df = df.iloc[21:-1].copy()
    
        # Convert 'Monthly Report' to datetime
        df["Monthly Report"] = pd.to_datetime(df["Monthly Report"], format="%d.%m.%Y")
    
        # Garantindo que as colunas numéricas sejam float (substitui vírgula por ponto se necessário)
        df["PV(kWh)"] = df["PV(kWh)"].astype(str).str.replace(",", ".").astype(float)
        df["Consumption(kWh)"] = df["Consumption(kWh)"].astype(str).str.replace(",", ".").astype(float)
    
        # --- Gráfico comparando PV e Consumo com Streamlit ---
        st.subheader("Geração Solar x Consumo de Energia Mensal")
    
        # Para usar st.line_chart, o eixo x deve ser o índice ou uma coluna numérica/datetime
        df_indexed = df.set_index("Monthly Report")
    
        st.line_chart(df_indexed[["PV(kWh)", "Consumption(kWh)"]])
    
    
        # --- Exibindo Totais com Streamlit ---
        total_consumption = df['Consumption(kWh)'].sum()
        total_solar_production = df['PV(kWh)'].sum()
    
        st.subheader("Totais Mensais")
        st.write(f"Consumo Total do Local (Mensal): {total_consumption:.2f} kWh")
        st.write(f"Produção Solar Total (PV) (Mensal): {total_solar_production:.2f} kWh")
    
    except FileNotFoundError:
        st.error("Erro: O arquivo 'BaseDeDados_BATERIA_MENSAL.xls' não foi encontrado. Por favor, carregue o arquivo no ambiente do Colab.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

    st.markdown("## Análise de Consumo e Geração Solar Diária")
 
    # --- Carregando dados do arquivo Excel ---
    try:
        df = pd.read_excel("content/BaseDeDados_BATERIA_DIARIA.xls", header=1) # Assuming the header is in the second row
    
        # Renomeando as colunas para facilitar o acesso (ajuste conforme o nome exato no seu arquivo)
        df.columns = ["Time", "PV(W)", "SOC(%)", "Battery(W)", "Grid (W)", "Load(W)"]
    
        # Remover a primeira linha que contém os nomes das colunas originais
        df = df.iloc[1:].copy()
    
    
        # Convertendo a coluna Time para datetime
        df["Time"] = pd.to_datetime(df["Time"], format="%d.%m.%Y %H:%M:%S")
    
        # Garantindo que os números sejam float (substitui vírgula por ponto se necessário)
        df["PV(W)"] = df["PV(W)"].astype(str).str.replace(",", ".").astype(float)
        df["Load(W)"] = df["Load(W)"].astype(str).str.replace(",", ".").astype(float)

        # --- Plotando com Streamlit ---
        st.subheader("Consumo vs Geração Solar ao longo do dia")
    
        # Para usar st.line_chart, o eixo x deve ser o índice ou uma coluna numérica/datetime
        # Vamos definir 'Time' como índice para o gráfico
        df_indexed = df.set_index("Time")
    
        st.line_chart(df_indexed[["PV(W)", "Load(W)"]])
    
        # --- Exibindo Totais ---
        total_daily_consumption = df['Load(W)'].sum()
        total_daily_solar_production = df['PV(W)'].sum()
    
        st.subheader("Totais Diários")
        st.write(f"Consumo Total Diário do Local: {total_daily_consumption:.2f} W")
        st.write(f"Produção Solar Total Diária (PV): {total_daily_solar_production:.2f} W")
    
    except FileNotFoundError:
        st.error("Erro: O arquivo 'BaseDeDados_BATERIA_DIARIA.xls' não foi encontrado. Por favor, carregue o arquivo no ambiente do Colab.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

elif paginas == "🔌 Equipamentos GoodWe":
    st.title("🔌 Informações sobre os Equipamentos")
    st.markdown("---")

    # Primeira linha
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### INVERSOR DA CASA")
        st.metric(label="Potência", value="~68 kW", delta="Últimos 5 min")
        
    with col2:
        st.markdown("### BATERIA DA CASA")
        st.metric(label="Carga Atual", value="~72%", delta="No momento")

    st.markdown("")

    # Segunda linha
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### CRÉDITOS NO DIA")
        st.metric(label="Economia", value="~35 EUR", delta="Acumulado hoje")

    with col4:
        st.markdown("### CONSUMO DA CASA")
        st.metric(label="Potência", value="~50 kW", delta="Últimos 5 min")
    
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

