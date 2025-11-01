import streamlit as st
import requests 
# import textwrap # <-- REMOVIDO

# --- Tema personalizado (CSS para teste) ---
custom_css_para_teste = """
<style>
.stApp { background-color: #e4d4b4; color: #000000; font-family: 'Segoe UI', sans-serif; font-size: 18px; }
h1, h2, h3 { color: #2e7d32; font-weight: 800; text-align: center; }
.section-text { text-align: center; max-width: 800px; margin: auto; font-size: 1.2em; line-height: 1.8em; color: #000000; }
.stButton>button { background-color: #2e7d32; color: white; border-radius: 8px; padding: 0.8em 1.6em; border: none; font-weight: bold; font-size: 1em; box-shadow: 0px 2px 6px rgba(0,0,0,0.15); }
.stButton>button:hover { background-color: #256428; color: #f1f1f1; }
</style>
"""

def render_sobre_page():
    """
    Renderiza a página 'Sobre o Projeto'.
    Esta função será chamada pelo app.py principal.
    """
    
    # --- Barra superior (logo + login) ---
    col1, col2 = st.columns([6,1])
    with col1:
        st.image("logo_energytime.png", width=90)
    with col2:
        st.markdown("<div style='text-align:right;'>", unsafe_allow_html=True)
        
        if st.session_state.get("autenticado", False):
            if st.button(f"Sair ({st.session_state.get('user_id', 'User')})"):
                st.session_state.autenticado = False
                st.session_state.user_id = None
                st.session_state.pagina_atual = "bem_vindo" 
                st.rerun()
        else:
            if st.button("Login"):
                st.session_state.pagina_atual = "login" 
                st.rerun() 
        
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ===================================================================
    # --- Conteúdo da Página 'Sobre' (TEXTO ATUALIZADO) ---
    # ===================================================================

    st.title("💡 Sobre o Projeto EnergyTime")
    
    # --- ATUALIZAÇÃO DO TEXTO ---
    # O HTML foi substituído pelo seu novo conteúdo, 
    # mantendo a estrutura e o alinhamento à esquerda.
    st.markdown(
        """
<div style="font-size: 1.1em; max-width: 700px; margin: auto; margin-bottom: 20px; text-align: left;">
<p>
A <b>EnergyTime</b> nasceu do desejo de aproximar as pessoas do consumo de energia. A ideia surgiu da percepção de que, embora muitos brasileiros acreditem que o consumo consciente pode mudar o mundo, poucos realmente colocam isso em prática.
</p>
<p>
Essa diferença entre intenção e ação inspirou-nos a criar uma solução que tornasse a energia limpa mais acessível, compreensível e presente no dia a dia.
</p>

<h3 style="text-align: left;">Parceria Estratégica com a GoodWe</h3>
<p>
Desenvolvido em parceria com a <b>GoodWe</b>, referência mundial em soluções de energia solar, o EnergyTime integra tecnologia e conscientização com o propósito de transformar a relação das pessoas com a energia — de forma simples, interativa e sustentável.
</p>

<h3 style="text-align: left;">O Que Fazemos</h3>
<ul style="text-align: left; display: block; margin-left: 20px;">
<li><b>Integração com Alexa:</b> Permite que o utilizador interaja diretamente com os seus equipamentos de energia solar por voz. Pode consultar dados, receber orientações e até antecipar possíveis quedas de energia.</li>
<li><b>Inteligência Conversacional (IA):</b> Além da Alexa, um Chatbot especialista tira dúvidas sobre equipamentos, eficiência energética e o funcionamento dos inversores.</li>
<li><b>Portal de Acompanhamento:</b> Um site com acesso a gráficos interativos, dados de consumo e geração solar, histórico de comunicações e previsões personalizadas com base em dados climáticos.</li>
<li><b>IA Preditiva:</b> Modelos que usam a previsão do tempo local para antecipar riscos de queda de energia, permitindo que o sistema seja proativo.</li>
</ul>

<h3 style="text-align: left;">Conectando o Futuro</h3>
<p>
O EnergyTime é, acima de tudo, uma ponte entre tecnologia e consciência ambiental. Ele convida cada pessoa a fazer parte de uma mudança global, começando pelo uso inteligente da energia em sua própria casa.
</p>
</div>
        """,
        unsafe_allow_html=True
    )

# Este bloco só é executado se você rodar este ficheiro DIRETAMENTE
if __name__ == "__main__":
    
    st.set_page_config(page_title="EnergyTime - Sobre", page_icon="logo_energytime.png", layout="wide")
    
    st.markdown(custom_css_para_teste, unsafe_allow_html=True)
    
    if "pagina_atual" not in st.session_state:
        st.session_state.pagina_atual = "sobre"
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
        
    render_sobre_page()

