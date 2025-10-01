# EnergyTime | Challenge  

## 1. Título do Projeto  
**EnergyTime – Integração Inteligente de Dispositivos GoodWe com Alexa e Inteligência Artificial**  

## 2. Equipe  
- Enzo Cerneviva  
- Gustavo Braga  
- Murilo Arcanjo  
- Rafael Costa  

## 3. Esquema de Integração dos Componentes  
O projeto é dividido em **quatro grandes blocos**, integrados em fluxo contínuo:  

- **Interação com o usuário (Alexa)** → recebe comandos de voz.  
- **Backend (Python + FastAPI/Flask)** → roteia requisições, processa intents e conecta módulos.  
- **Módulos de integração**:  
  - *GoodWe*: leitura e envio de comandos (simulados via portal GoodWe).  
  - *OpenWeather*: coleta dados climáticos para alimentar a IA.  
- **Módulo de Inteligência Artificial (ia_engine.py)** → processa dados, classifica risco de queda de energia e ajusta estratégias.  
- **Frontend (Streamlit)** → interface web para:  
  - Visualização de dados climáticos.  
  - Resultados das previsões da IA.  
  - Simulação manual de comandos (complementando a Alexa).  

### Fluxo Operacional (descrição textual)  
1. Usuário faz um pedido à Alexa.  
2. Alexa envia JSON ao backend.  
3. Backend identifica a intent e consulta módulos internos (GoodWe, IA, clima).  
4. IA processa dados e retorna classificação de risco (0/1).  
5. Backend responde à Alexa ou atualiza o Streamlit com os dados.  
6. Usuário recebe feedback por voz e/ou visual.  

## 4. Justificativa Técnica das Escolhas  
- **Python**: por sua ampla biblioteca em IA, APIs e facilidade de integração.  
- **Random Forest**: modelo robusto para classificação binária, eficiente em datasets pequenos/médios e fácil de interpretar.  
- **Streamlit**: escolhido para o frontend por permitir prototipagem rápida, visualização clara e integração direta com Python.  
- **Alexa Skills Kit**: garante automação via comandos de voz, ampliando acessibilidade e praticidade.  
- **OpenWeather API**: fonte confiável e gratuita de dados meteorológicos para treinar e alimentar a IA.  

## 5. Resultados e Dados Funcionais  
- **Testes simulados com base de dados GoodWe** confirmaram o funcionamento dos módulos.  
- **Alexa totalmente integrada**: todos os comandos de consulta e controle retornam respostas funcionais.  
- **IA funcional em ambiente de simulação**: previsões retornam “0” (sem risco) ou “1” (risco alto), orientando decisões.  
- **Frontend em desenvolvimento (Streamlit)**:  
  - Visualização dos dados climáticos tratados.  
  - Exibição da previsão da IA.  
  - Interface para testes manuais de comandos.  
- A simulação real do uso (Alexa + IA + protótipo) será exibida no vídeo de apresentação.  

## 6. Conexão com os Conteúdos da Disciplina  
O projeto aplica conteúdos das disciplinas de:  
- **Inteligência Artificial**: uso de Random Forest para previsão de quedas de energia.  
- **Programação e Integração de Sistemas**: backend com Python, APIs externas e assistente virtual.  
- **Automação e Energias Renováveis**: integração com inversores GoodWe e aproveitamento da geração solar.  
- **Prototipagem de Interfaces**: uso de Streamlit para simulação e interação.  

## 7. Estrutura do Repositório  

```bash
EnergyTime/
|
├── README.md           ← Relatório do projeto
├── .env.example        ← Exemplo de variáveis de ambiente
├── .gitignore          ← Ignora arquivos não versionados
├── requirements.txt    ← Dependências do projeto
|
├── backend/
│   ├── main.py         ← Roteador principal (API Flask/FastAPI)
│   ├── alexa_skill.py  ← Integração com Alexa
│   ├── weather.py      ← Consumo da API OpenWeather
│   ├── goodwe.py       ← Simulação de controle dos dispositivos GoodWe
│   └── ia_engine.py    ← Motor de decisão com IA
|
├── frontend/
│   └── app.py          ← Interface web em Streamlit
|
└── docs/
    └── fluxos.md       ← Descrição textual dos fluxos de integração
```
## 8. Instruções de Execução  

1. Clone o repositório:  
   git clone https://github.com/seu-usuario/EnergyTime.git  
   cd EnergyTime  

2. Configure as variáveis de ambiente no arquivo `.env`.  

3. Instale as dependências:  
   pip install -r requirements.txt  

4. Inicie o backend:  
   python backend/main.py  

5. Inicie o frontend (em outra aba):  
   streamlit run frontend/app.py  

6. Configure a Alexa Skill apontando para o backend.  
