import streamlit as st
import requests
import os

# --- Importa as FUNÇÕES das nossas páginas ---
# (Assumindo que estão na pasta 'views/')
from paginas.welcome import render_welcome_page
from paginas.login import render_login_page
from paginas.principal import render_principal_page
from paginas.sobre import render_sobre_page

# ===================================================================
# --- 1. CONFIGURAÇÃO DA PÁGINA (CHAMADA ÚNICA) ---
# ===================================================================
st.set_page_config(
    page_title="EnergyTime", 
    page_icon="logo_energytime.png", 
    layout="wide" # <-- REQUISITO: Layout WIDE
)

# ===================================================================
# --- 2. CSS GLOBAL (CARREGADO UMA ÚNICA VEZ) ---
# ===================================================================
# (Este é o seu CSS completo)
custom_css = """
<style>
/* Fundo geral */
.stApp {
    background-color: #e4d4b4; color: #000000; font-family: 'Segoe UI', sans-serif; font-size: 18px; 
}
h1, h2, h3 {
    color: #2e7d32; font-weight: 800; text-align: center;
}
.section-text {
    text-align: center; max-width: 800px; margin: auto; font-size: 1.2em; line-height: 1.8em; color: #000000;
}
.stButton>button {
    background-color: #2e7d32; color: white; border-radius: 8px; padding: 0.8em 1.6em; border: none; font-weight: bold; font-size: 1em; box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
}
.stButton>button:hover {
    background-color: #256428; color: #f1f1f1;
}
.chat-bubble-user {
    background-color: #6d604c; color: white; padding: 16px 20px; border-radius: 15px; margin: 10px auto; max-width: 80%; font-size: 1.1em; box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}
.chat-bubble-bot {
    background-color: #2e7d32; color: white; padding: 16px 20px; border-radius: 15px; margin: 10px auto; max-width: 80%; font-size: 1.1em; font-style: italic; box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}
.credits-box {
    background-color: #FFEBCD; border: 1px solid #d3c5a4; border-radius: 12px; color: #3d3d3d; padding: 1em 1.25em; margin-bottom: 1em;
}
.credits-box strong {
    color: #2e7d32;
</style>
"""
#st.markdown(custom_css, unsafe_allow_html=True)

# ===================================================================
# --- 3. INICIALIZAÇÃO DO ESTADO DA SESSÃO ---
# ===================================================================
if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = "bem_vindo" # Começa na página de boas-vindas
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None


# ===================================================================
# --- 5. O ROTEADOR ---
# ===================================================================
# (Decide qual função de página chamar)

if st.session_state.pagina_atual == "bem_vindo":
    render_welcome_page()
    
elif st.session_state.pagina_atual == "login":
    render_login_page()

elif st.session_state.pagina_atual == "sobre":
    render_sobre_page()
    
elif st.session_state.pagina_atual == "principal":
    # O guardião de login está DENTRO da função render_principal_page,
    # mas também podemos verificar aqui por segurança.
    if st.session_state.autenticado:
        render_principal_page()
    else:
        # Se tentar aceder à "principal" sem login, força o login
        st.error("Acesso negado. Por favor, faça o login.")
        st.session_state.pagina_atual = "login"
        st.rerun()
else:
    # Página 'Sobre' ou outra página pública
    # (Adicionaremos o 'sobre' aqui quando o criar)
    render_welcome_page()
