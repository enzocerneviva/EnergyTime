import streamlit as st

# --- Configuração da página ---
st.set_page_config(page_title="EnergyTime", page_icon="logo_energytime.png", layout="wide")

# --- Tema personalizado ---
custom_css = """
<style>
/* Fundo geral */
.stApp {
    background-color: #e4d4b4; /* bege artesão */
    color: #000000; /* texto preto para contraste */
    font-family: 'Segoe UI', sans-serif;
    font-size: 18px; /* texto maior */
}

/* Títulos */
h1, h2, h3 {
    color: #2e7d32; /* verde principal */
    font-weight: 800;
    text-align: center;
}

/* Texto centralizado */
.section-text {
    text-align: center;
    max-width: 800px;
    margin: auto;
    font-size: 1.2em;
    line-height: 1.8em;
    color: #000000;
}

/* Botões */
.stButton>button {
    background-color: #2e7d32;
    color: white;
    border-radius: 8px;
    padding: 0.8em 1.6em;
    border: none;
    font-weight: bold;
    font-size: 1em;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
}
.stButton>button:hover {
    background-color: #256428;
    color: #f1f1f1;
}

/* Chat bolhas */
.chat-bubble-user {
    background-color: #4A90E2;
    color: white;
    padding: 12px 16px;
    border-radius: 15px;
    margin: 10px auto;
    max-width: 70%;
    font-size: 1.05em;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}
.chat-bubble-bot {
    background-color: #2e7d32;
    color: white;
    padding: 12px 16px;
    border-radius: 15px;
    margin: 10px auto;
    max-width: 70%;
    font-size: 1.05em;
    font-style: italic;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- Barra superior (logo + login) ---
col1, col2 = st.columns([6,1])
with col1:
    st.image("logo_energytime.png", width=90)
with col2:
    st.markdown("<div style='text-align:right;'>", unsafe_allow_html=True)
    st.button("Login")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# --- Container central para apresentação ---
st.title("🌱 Bem-vindo à EnergyTime")

st.markdown(
    """
    <div class="section-text">
        <p>
        A <b>EnergyTime</b> conecta pessoas e tecnologia para transformar a forma como lidamos com energia.  
        Nosso objetivo é <b>simplificar o gerenciamento de energia solar</b> e integrar equipamentos inteligentes da GoodWe com assistentes virtuais como a Alexa.  
        </p>
        <p>
        Com a EnergyTime, você pode:
        </p>
        <ul style="text-align: left; display: inline-block; font-size: 1.1em; color: #000000;">
            <li>Receber recomendações personalizadas sobre uso eficiente de energia</li>
            <li>Monitorar seus equipamentos GoodWe em tempo real</li>
            <li>Obter previsões inteligentes para reduzir custos e evitar imprevistos</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# --- Chat da IA (visual de demonstração) ---
st.subheader("💬 Assistente Virtual (3 créditos grátis)")
st.info("Você possui **3 créditos gratuitos** para conversar com a IA sobre energia e equipamentos GoodWe.")

st.markdown("### Simulação de Conversa")

# Mensagens pré-carregadas
st.markdown('<div class="chat-bubble-user">👤 Usuário: Como posso melhorar o uso da minha bateria?</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-bubble-bot">🤖 EnergyTime IA: Recomendo manter a bateria entre 20% e 80% para maior vida útil.</div>', unsafe_allow_html=True)
st.markdown("\n")
st.markdown("<div style='color: #000000; font-size: 18px; font-weight: 500;'>Digite sua mensagem para a EnergyTime:</div>", unsafe_allow_html=True)

user_input = st.text_input("")

if user_input:
    st.markdown(f'<div class="chat-bubble-user">👤 Usuário: {user_input}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chat-bubble-bot">🤖 EnergyTime IA: (a resposta aparecerá aqui futuramente)</div>', unsafe_allow_html=True)
