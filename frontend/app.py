import streamlit as st
import pandas as pd

# Configurações iniciais da página
st.set_page_config(page_title="EnergyTime", layout="wide")

colA, colB = st.columns([1, 5])  # logo pequeno, texto grande
with colA:
    st.image("logo_energytime.png", width=60)

with colB:
    st.markdown("<h2 style='margin-top: 15px;'>EnergyTime Dashboard</h2>", unsafe_allow_html=True)


st.markdown("---")

menu = st.sidebar.radio(
    "Navegacao",
    ["Graficos", "Assistente Alexa", "Status", "Conversa com IA", "Configuracoes"]
)

if menu == "Graficos":
    st.subheader("Dados do Inversor e Geracao de Energia")
    st.line_chart({"Geracao(Kwh)": [10, 20, 30, 25 , 40]})
    
if menu == "Assistente Alexa":
    st.subheader("Historico de Interacoes com a Alexa")
    st.write("Usuário: ")
    st.write("Alexa: ")

if menu == "Status":
    st.subheader("Status dos Equipamentos GoodWe")

if menu == "Conversa com IA":
    st.subheader("Chat com Inteligência Artificial Personalizada")

if menu == "Configuracoes":
    st.subheader("Configurações Personalizadas")