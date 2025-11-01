import streamlit as st
import requests

# URL DO BACKEND (ajuste se o backend não estiver a rodar localmente na porta 10000)
URL_BACKEND_LOGIN_LOCAL = "http://127.0.0.1:10000/login"
URL_BACKEND_LOGIN_RENDER = "https://energytime-challenge-01.onrender.com/login" # (Se o seu backend estiver no Render)


def render_login_page():
    """
    Renderiza a tela de login.
    Esta função será chamada pelo app.py se o utilizador não estiver logado.
    """

    # 1. Título e Descrição (Design "parecido com o welcome")
    st.title("🔑 Acesso ao EnergyTime")
    st.markdown(
        """
        <div class="section-text" style="font-size: 1.1em; max-width: 700px; margin-bottom: 20px;">
            <p>
            Por favor, insira as suas credenciais para aceder aos relatórios, 
            dashboard de gestão dos seus equipamentos e outras funcionalidades do nosso sistema.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. Centraliza o formulário
    _ , col_form, _ = st.columns([1, 2, 1])
    
    with col_form:
        # 3. Formulário de Login
        with st.form(key="login_form_main"):
            usuario = st.text_input("Utilizador")
            senha = st.text_input("Senha", type="password")
            
            if st.form_submit_button("Entrar", use_container_width=True, type="primary"):
                
                # --- 4. Lógica de Autenticação (Chama o Backend) ---
                try:
                    # Tenta fazer o post para a nova rota /login no Flask
                    # (Use a URL correta do seu backend)
                    response = requests.post(URL_BACKEND_LOGIN_LOCAL, json={"usuario": usuario, "senha": senha})
                    
                    if response.status_code == 200:
                        # Login OK!
                        dados_usuario = response.json()
                        st.session_state.autenticado = True # Define o estado como logado
                        st.session_state.user_id = dados_usuario.get("nome_completo", usuario)
                        st.session_state.pagina_atual = "principal" # Diz ao roteador para mudar
                        
                        st.success("Login bem-sucedido! A carregar página principal...")
                        st.rerun() # Recarrega o app.py, que agora vai chamar o dashboard
                    else:
                        # Login falhou (ex: 401 - Não autorizado)
                        st.error(f"Erro: {response.json().get('erro', 'Utilizador ou senha inválidos')}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("Erro ao conectar com o servidor de login. O backend (main.py) está a funcionar?")
                except requests.exceptions.RequestException as e:
                    st.error(f"Erro de API: {e}")

