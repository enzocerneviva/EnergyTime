import streamlit as st

def login_page():
    # Configurações da página (opcional, caso queira layout full width)
    st.set_page_config(page_title="Login - EnergyTime", layout="wide")

    # --- CSS personalizado (cores da EnergyTime) ---
    st.markdown("""
    <style>
    /* Fundo geral da página de login */
    .stApp {
        background-color: #e4d4b4; /* bege clarinho */
        color: #000000; /* texto preto */
    }

    /* Caixa de login */
    .login-box {
        background-color: #ffffff; /* branco para contraste */
        padding: 40px;
        border-radius: 15px;
        max-width: 400px;
        margin: 50px auto;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        text-align: center;
    }

    /* Título */
    .login-box h2 {
        color: #2e7d32;
        margin-bottom: 20px;
    }

    /* Botão */
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        border-radius: 8px;
        padding: 0.8em 1.6em;
        border: none;
        font-weight: bold;
        font-size: 1em;
    }
    .stButton>button:hover {
        background-color: #256428;
        color: #f1f1f1;
    }

    /* Campos de input */
    input[data-baseweb] {
        background-color: #f5f0e1 !important; /* bege clarinho */
        color: #000000 !important;             /* texto preto */
        border: 1px solid #444444 !important;
        border-radius: 8px !important;
        padding: 10px !important;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Caixa de login centralizada ---
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<h2>🌱 EnergyTime Login</h2>', unsafe_allow_html=True)

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    
    if st.button("Entrar"):
        # Aqui você adiciona a lógica de autenticação
        st.success(f"Bem-vindo(a), {username}!")
    
    st.markdown('</div>', unsafe_allow_html=True)
