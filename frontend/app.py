import streamlit as st
import requests

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
    st.header("Análise de dados de energia da casa no último mês")
    st.header("Análise de dados de energia da casa no último dia")

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

    st.title("Histórico de Interações com a Alexa")
    st.markdown("---")

    URL_BACKEND = "https://energytime-challenge-01.onrender.com/historico"  # ajustar no deploy

    # Container principal com estilo (imitando border-radius e fundo claro)
    st.markdown(
        """
        <style>
        .chat-container {
            border: 1px solid #ddd;
            border-radius: 15px;
            padding: 20px;
            background-color: #f9f9f9;
            max-height: 500px;
            overflow-y: auto;
        }
        .mensagem {
            margin: 10px 0;
            padding: 10px 15px;
            border-radius: 15px;
            max-width: 70%;
            word-wrap: break-word;
        }
        .entrada {
            background-color: #DCF8C6;  /* verde claro estilo WhatsApp */
            margin-left: auto;
            text-align: right;
        }
        .resposta {
            background-color: #ffffff;
            border: 1px solid #ddd;
            margin-right: auto;
            text-align: left;
        }
        .timestamp {
            font-size: 0.8em;
            color: #888;
            margin: 2px 5px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    try:
        historico = requests.get(URL_BACKEND).json()
    except Exception:
        historico = []

    if historico:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)

        for item in historico[::-1]:  # mais recentes primeiro
            st.markdown(f'<div class="timestamp">{item["timestamp"]} | Intent: {item["intent"]}</div>', unsafe_allow_html=True)

            # Entrada (usuário/Alexa) - lado direito
            st.markdown(f'<div class="mensagem entrada">{item["entrada"]}</div>', unsafe_allow_html=True)

            # Resposta (nosso sistema) - lado esquerdo
            st.markdown(f'<div class="mensagem resposta">{item["resposta"]}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("⚠️ Não há nenhum histórico de informações no momento.")
        
elif paginas == "💬 IA Personalizada":

    st.title("Converse com a IA sobre qualquer dúvida sobre energia ou sobre os equipamentos")

elif paginas == "⚙️ Configurações":

    st.title("⚙️ Ajustes do sistema")

