# EnergyTime | Challenge

## 1. Título do Projeto  
**EnergyTime – Integração Inteligente de Dispositivos GoodWe com Alexa e Inteligência Artificial**

---

## 2. Equipa  
- Enzo Cerneviva  
- Gustavo Braga  
- Murilo Arcanjo  
- Rafael Costa  

---

## 3. Esquema de Integração dos Componentes  

O projeto é dividido em quatro grandes blocos:

**Interação com o utilizador (Alexa)** → recebe comandos de voz.  

**Backend (Python + Flask)** → API central que serve o frontend.  
Processa intents da Alexa, gere a lógica de negócio, autentica utilizadores (`/login`), serve o chatbot RAG (`/chat_ia`) e conecta-se aos módulos de hardware (GoodWe) e dados (OpenWeather).  

**Módulo de Inteligência Artificial (ia_engine.py, chatbot.py)** → Inclui o modelo de Random Forest para prever quedas de energia e o motor RAG (OpenAI) para o chatbot especialista.  

**Frontend (Streamlit)** → Interface web unificada (`app.py`) que atua como um *Single Page App (SPA)*.  
Controla o estado de autenticação (`st.session_state`) e renderiza diferentes *views* (páginas) para o utilizador, como o chatbot público (`paginas/welcome.py`), a tela de login (`paginas/login.py`) e o dashboard privado (`paginas/principal.py`).  

---

### 🔁 Fluxo Operacional (Exemplo Web)

1. Utilizador acede ao `app.py` (roteador) e vê a página pública (`paginas/welcome.py`).  
2. Utilizador testa o chatbot (com 3 créditos) ou clica em “Login”.  
3. Roteador muda o estado e renderiza a `paginas/login.py`.  
4. Utilizador submete o formulário; frontend envia um POST para a rota `/login` do backend.  
5. Backend (Flask) verifica as credenciais no `usuarios.json` e retorna sucesso.  
6. Frontend atualiza o `st.session_state.autenticado = True` e renderiza o dashboard privado (`paginas/principal.py`).  

---

### 🗣️ Fluxo Operacional (Exemplo Alexa)

1. Utilizador faz um pedido à Alexa.  
2. Alexa envia JSON para a rota `/alexa` do backend.  
3. Backend (Flask) identifica a intent, consulta os módulos (GoodWe, IA) e retorna a resposta de voz.  

---

## 4. Justificativa Técnica das Escolhas  

- **Python:** Pela sua ampla biblioteca em IA, APIs e facilidade de integração.  
- **Flask:** Utilizado como backend de API por ser leve, robusto e ideal para servir rotas JSON para o frontend e para a Alexa.  
- **Random Forest:** Modelo robusto para classificação binária, eficiente em datasets pequenos/médios e fácil de interpretar.  
- **Streamlit:** Escolhido para o frontend pela prototipagem rápida.  
  Foi implementado um padrão de Roteador (Controlador) para gerir o `st.session_state` e permitir um fluxo de autenticação seguro (página de login → dashboard privado), superando as limitações do “Multi-Page App” padrão do Streamlit.  
- **Alexa Skills Kit:** Garante automação via comandos de voz, ampliando acessibilidade.  
- **OpenWeather API:** Fonte confiável de dados meteorológicos para alimentar a IA.  

---

## 5. Resultados e Dados Funcionais  

- **Testes simulados** com base de dados GoodWe confirmaram o funcionamento dos módulos.  
- **Alexa totalmente integrada:** todos os comandos de consulta e controle retornam respostas funcionais.  
- **IA funcional:** O modelo de previsão (Random Forest) e o Chatbot RAG (OpenAI) estão funcionais e servidos pelo backend.  
- **Frontend (Streamlit):**  
  - Interface de “Bem-vindo” com chatbot público (limite de 3 créditos).  
  - Sistema de Login seguro com autenticação via API no backend.  
  - Dashboard privado (`principal.py`) que exibe as 3 funcionalidades principais (Relatórios, Histórico Alexa, IA).  

---

## 6. Conexão com os Conteúdos da Disciplina  

O projeto **EnergyTime** integra diversos conteúdos aprendidos na disciplina:

### Conceitos de Energia e Automação  
O sistema permite que o utilizador visualize e gere a geração e o consumo de energia, aproximando conceitos de eficiência energética do uso quotidiano.  

### Inteligência Artificial  
- O modelo de IA em `ia_engine.py` utiliza **Random Forest** para prever quedas de energia.  
- O **Energy Bot** (centralizado no backend em `chatbot.py` e `main.py`) usa **RAG (Retrieval-Augmented Generation)** com a API da OpenAI para responder perguntas específicas sobre os manuais da GoodWe.  

### Programação e Integração de Sistemas  
- O **Backend Flask (`main.py`)** atua como o cérebro, coordenando APIs externas (OpenWeather), o frontend (Streamlit), a Alexa e os módulos de IA.  
- O sistema de login (`/login`) demonstra autenticação simples baseada em JSON.  

### Prototipagem de Interfaces (Frontend)  
O frontend em Streamlit é estruturado como um **Single Page App (SPA)**.  
Um roteador central (`app.py`) gere o estado de autenticação (`st.session_state`) e renderiza condicionalmente as *views* (ex: `paginas/login.py`, `paginas/principal.py`), proporcionando uma experiência de utilizador segura e fluida que não seria possível com a estrutura de páginas padrão do Streamlit.  

---

## 7. 📂 Estrutura do Repositório

```
EnergyTime/
|
├── README.md                 ← Relatório do projeto
├── .env.example
├── .gitignore
├── requirements.txt          ← Dependências do projeto
|
├── backend/
│   ├── main.py               ← Roteador principal (API Flask) com rotas /login, /chat_ia, /alexa
│   ├── alexa_skill.py        ← Lógica para processar intents da Alexa
│   ├── weather.py
│   ├── goodwe.py
│   ├── ia_engine.py          ← Motor de decisão (Random Forest)
│   ├── chatbot.py            ← (NOVO) Lógica central do Chatbot (RAG, OpenAI)
│   ├── geocoding.py
│   ├── usuarios.json         ← (NOVO) Base de dados simples de utilizadores para login
│   │
│   └── bases_de_dados/
│       ├── ... (outras bases)
|
├── frontend/
│   ├── app.py                ← (NOVO) Roteador/Controlador principal do Streamlit
│   │
│   └── paginas/              ← (NOVO) Pasta com todas as "views" (páginas)
│       ├── __init__.py
│       ├── welcome.py        ← (NOVO) Página pública do chatbot (antiga default_page.py)
│       ├── login.py          ← (NOVO) Página de login
│       ├── principal.py      ← (NOVO) Dashboard privado (antiga app.py)
│       └── sobre.py          ← (NOVO) Página "Sobre o Projeto"
│
└── (default_page.py)         ← (REMOVIDO / Substituído por app.py e paginas/welcome.py)
```

---

## 8. ⚙️ Instruções de Execução

### 🔹 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/EnergyTime.git
cd EnergyTime
```

---

### 🔹 2. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto (ou copie o `.env.example`) e defina suas chaves de API:

```bash
OPENAI_API_KEY=coloque_sua_chave_aqui
GOODWE_API_KEY=sua_chave_goodwe
OPENWEATHER_API_KEY=sua_chave_openweather
```

> ⚠️ **Importante:** nunca envie o arquivo `.env` para o GitHub — ele está protegido pelo `.gitignore`.

---

### 🔹 3. Instale as dependências
```bash
pip install -r requirements.txt
```

---

### 🔹 4. Inicie o backend (API Flask)
Em um terminal:
```bash
python backend/main.py
```

---

### 🔹 5. Inicie o frontend (Interface Streamlit)
Em outro terminal:
```bash
streamlit run frontend/app.py
```

> O arquivo `app.py` agora funciona como **roteador principal**, controlando todas as páginas dentro da pasta `frontend/paginas`.

---

### 🔹 6. Configure a Alexa Skill

No painel da **Alexa Developer Console**, defina o endpoint da sua skill apontando para o backend hospedado:

```
https://seu-dominio.onrender.com/alexa
```

> Isso garante que todas as intents da Alexa sejam processadas pelo `alexa_skill.py` do EnergyTime.

---

✨ Após essas etapas, o EnergyTime estará pronto para uso — integrando **Alexa, IA, previsões climáticas, monitoramento de energia e um painel web completo.**
