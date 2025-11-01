import streamlit as st
import requests 

# --- URLs DO BACKEND ---
URL_BACKEND_CHAT_LOCAL = "http://127.0.0.1:10000/chat_ia"
URL_BACKEND_CHAT_RENDER = "https://energytime-challenge-01.onrender.com/chat_ia"

def render_welcome_page():
    """
    Renderiza a página 'Bem-Vindo' (o chatbot público com 3 créditos).
    Esta função será chamada pelo app.py principal.
    """

    # --- Configuração da página ---
    # st.set_page_config(...) FOI REMOVIDO. O app.py (controlador) faz isto.

    # --- Tema personalizado (Mantido) ---
    custom_css = """
    <style>
    /* Fundo geral (Mantido) */
    .stApp {
        background-color: #e4d4b4; /* bege artesão */
        color: #000000; /* texto preto para contraste */
        font-family: 'Segoe UI', sans-serif;
        font-size: 18px; 
    }

    /* Títulos (Mantido) */
    h1, h2, h3 {
        color: #2e7d32; /* verde principal */
        font-weight: 800;
        text-align: center;
    }

    /* Texto centralizado (Mantido) */
    .section-text {
        text-align: center;
        max-width: 800px;
        margin: auto;
        font-size: 1.2em;
        line-height: 1.8em;
        color: #000000;
    }

    /* Botões (Mantido) */
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

    /* --- MUDANÇAS DE DESIGN NO CHAT --- */

    /* 1. Bolha do Utilizador (Mantido) */
    .chat-bubble-user {
        background-color: #6d604c;  /* Tom de marrom/terra (harmoniza com bege) */
        color: white;
        padding: 16px 20px;       /* Mais padding (maior) */
        border-radius: 15px;
        margin: 10px auto;
        max-width: 80%;           /* Mais largo */
        font-size: 1.1em;         /* Fonte maior */
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }

    /* 2. Bolha do Bot (Mantido) */
    .chat-bubble-bot {
        background-color: #2e7d32;
        color: white;
        padding: 16px 20px;       /* Mais padding (maior) */
        border-radius: 15px;
        margin: 10px auto;
        max-width: 80%;           /* Mais largo */
        font-size: 1.1em;         /* Fonte maior */
        font-style: italic;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }

    /* 3. Caixa de Créditos (Mantido) */
    .credits-box {
        background-color: #FFEBCD; /* Fundo "papel antigo" */
        border: 1px solid #d3c5a4;  /* Borda sutil */
        border-radius: 12px;
        color: #3d3d3d; /* Texto escuro e legível */
        padding: 1em 1.25em; /* Espaçamento interno */
        margin-bottom: 1em; /* Espaçamento externo */
    }
    .credits-box strong {
        color: #2e7d32; /* Verde principal para o número */
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # --- Barra superior (logo + login) (LÓGICA ATUALIZADA) ---
    col1, col2 = st.columns([6,1])
    with col1:
        st.image("logo_energytime.png", width=90)
    with col2:
        st.markdown("<div style='text-align:right;'>", unsafe_allow_html=True)
        
        # Lógica condicional: Mostra "Login" ou "Logout"
        if st.session_state.get("autenticado", False):
            if st.button(f"Sair ({st.session_state.get('user_id', 'User')})"):
                st.session_state.autenticado = False
                st.session_state.user_id = None
                st.session_state.pagina_atual = "bem_vindo" # Volta para esta página
                st.rerun()
        else:
            if st.button("Login"):
                st.session_state.pagina_atual = "login" # DIZ AO CONTROLADOR PARA MUDAR
                st.rerun() # FORÇA O CONTROLADOR A RE-LER O ESTADO
        
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ===================================================================
    # --- Título e Descrição de "Marketing" (Mantido) ---
    # ===================================================================

    st.title("🤖 Bem-vindo ao EnergyTime Bot")
    st.markdown(
        """
        <div class="section-text" style="font-size: 1.1em; max-width: 700px; margin-bottom: 20px;">
            <p>
            Este é o assistente virtual da EnergyTime. Faça uma pergunta sobre <b>energia solar</b>, 
            <b>equipamentos GoodWe</b>, ou <b>eficiência energética</b>. 
            Nossa IA está aqui para te ajudar a tirar o máximo proveito do seu sistema!
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ===================================================================
    # --- Chat da IA (Lógica funcional mantida) ---
    # ===================================================================

    # --- 1. Lógica de Créditos e Histórico (Mantida) ---
    if "creditos" not in st.session_state:
        st.session_state.creditos = 3
    if "messages_default" not in st.session_state:
        st.session_state.messages_default = [
            {"role": "assistant", "content": "Olá! Sou a IA da EnergyTime. Faça sua primeira pergunta."}
        ]

    # --- Caixa de Créditos (Mantida) ---
    st.markdown(f"""
    <div class="credits-box">
    Você possui <strong>{st.session_state.creditos} créditos gratuitos</strong> para testar a IA.
    </div>
    """, unsafe_allow_html=True)

    # --- 2. Exibição do Histórico de Chat (Mantido) ---
    with st.container(height=400): 
        for message in st.session_state.messages_default:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-bubble-user">👤 Utilizador: {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bubble-bot">🤖 EnergyTime IA: {message["content"]}</div>', unsafe_allow_html=True)

    # --- 3. Lógica de Input e API (Mantida) ---
    creditos_restantes = st.session_state.creditos
    input_desabilitado = (creditos_restantes <= 0)
    placeholder_texto = "Você esgotou seus créditos. Faça login para continuar." if input_desabilitado else "Digite sua pergunta..."

    if user_input := st.chat_input(placeholder_texto, disabled=input_desabilitado):
        
        st.session_state.messages_default.append({"role": "user", "content": user_input})
        st.session_state.creditos -= 1
        
        with st.spinner("EnergyTime IA está a pensar..."):
            try:
                response = requests.post(
                    URL_BACKEND_CHAT_RENDER,
                    json={"pergunta": user_input}
                )
                response.raise_for_status() 
                resposta_ia = response.json().get("resposta", "Erro ao decodificar resposta do servidor.")
                
            except requests.exceptions.ConnectionError:
                resposta_ia = "⚠️ **Erro de Conexão:** Não foi possível conectar ao servidor de IA. O backend (main.py) está a funcionar?"
            except requests.exceptions.RequestException as e:
                resposta_ia = f"⚠️ **Erro de API:** {e}"
            except Exception as e:
                resposta_ia = f"⚠️ **Erro Inesperado:** {e}"

        st.session_state.messages_default.append({"role": "assistant", "content": resposta_ia})
        st.rerun()

# Este bloco só é executado se você rodar este ficheiro DIRETAMENTE
# (bom para testar a página isoladamente)
if __name__ == "__main__":
    # Define o layout como "wide" QUANDO EXECUTADO DIRETAMENTE
    st.set_page_config(page_title="EnergyTime - Sobre", page_icon="logo_energytime.png", layout="wide")
    # Simula o estado inicial que o app.py (controlador) teria
    if "pagina_atual" not in st.session_state:
        st.session_state.pagina_atual = "bem_vindo"
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
        
    render_welcome_page()