import streamlit as st

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

elif paginas == "💬 IA Personalizada":

    st.title("Converse com a IA sobre qualquer dúvida sobre energia ou sobre os equipamentos")

elif paginas == "⚙️ Configurações":

    st.title("⚙️ Ajustes do sistema")

