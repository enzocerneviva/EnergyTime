# EnergyTime | Challenge

## 1. Sobre o Projeto
O EnergyTime é um projeto acadêmico desenvolvido como desafio da GoodWe em parceria com a FIAP.  
O objetivo é criar uma aplicação que integre os equipamentos da GoodWe — como inversores, carregadores elétricos e baterias — com um assistente virtual, oferecendo controle inteligente, automação e previsões baseadas em dados climáticos.

---

## 2. Equipe Envolvida
- Enzo Cardilli Cerneviva - RM: 563480  
- Gustavo Cordeiro Braga – RM: 562247  
- Murilo Justino Arcanjo – RM: 565470  
- Rafael Quattrer Dalla Costa – RM: 562052  

---

## 3. Esquema de Integração dos Componentes

### Fluxo de Funcionamento
1. O usuário faz um comando por voz via Alexa.  
2. A Alexa converte o comando em uma requisição JSON.  
3. O arquivo `main.py` recebe a requisição.  
4. O arquivo `alexa_skill.py` interpreta a intent e prepara a resposta.  
5. O arquivo `weather.py` consulta a API OpenWeather.  
6. O arquivo `goodwe.py` consulta ou simula dispositivos GoodWe.  
7. O arquivo `ia_engine.py` processa dados climáticos e aplica o modelo de IA.  
8. O modelo Random Forest classifica se há risco de queda de energia.  
9. A decisão é enviada para a Alexa e/ou para os dispositivos GoodWe.  
10. O usuário recebe a resposta final por voz.  

---

## 4. Justificativa Técnica das Escolhas
- Python: simplicidade, comunidade ativa e suporte robusto para IA e APIs.  
- Flask / FastAPI: frameworks leves para criação de APIs que se comunicam com Alexa.  
- scikit-learn (Random Forest): modelo confiável para classificação binária e robusto contra overfitting.  
- OpenWeather API: dados climáticos em tempo real.  
- Alexa Skills Kit: integração simples de comandos de voz.  
- Render (deploy): hospedagem escalável e prática em nuvem.  

---

## 5. Resultados Obtidos
- Integração com Alexa configurada.  
- Estrutura modular do backend pronta (main.py, alexa_skill.py, weather.py, goodwe.py, ia_engine.py).  
- Modelo Random Forest treinado para prever quedas de energia com base em dados meteorológicos.  
- Simulação de comandos GoodWe concluída (ligar, desligar, consultar status).  

### Exemplo de saída do modelo de IA
- Input: Temperatura = 28°C, Umidade = 80 %, Vento = 25 km/h, Chuva = 15 mm  
- Output: 1 (Risco de queda de energia)  

### Próximos passos
- Implementar comunicação em tempo real com dispositivos reais GoodWe.  
- Ampliar base de treinamento da IA com dados históricos (INMET / NASA POWER).  
- Criar dashboards de monitoramento em tempo real.  

---

## 6. Conexão com os Conteúdos da Disciplina
- IoT e Automação → integração com dispositivos físicos e simulação em código.  
- Inteligência Artificial → aplicação prática do modelo Random Forest.  
- Cloud & APIs → uso do OpenWeather e deploy no Render.  
- Interação Homem-Máquina → comandos por voz via Alexa.  
- Engenharia de Software → modularização, versionamento no GitHub e boas práticas de desenvolvimento.  

---

## 7. Organização da Aplicação
EnergyTime/  
│  
├── README.md           ← Documento explicativo do projeto  
├── .env.example        ← Variáveis de ambiente (exemplo)  
├── .gitignore          ← Arquivos ignorados no versionamento  
├── requirements.txt    ← Dependências do projeto  
│  
└── backend/  
    ├── main.py         ← Roteador principal (servidor HTTPS)  
    ├── alexa_skill.py  ← Integração com Alexa  
    ├── weather.py      ← Coleta e tratamento de dados climáticos  
    ├── goodwe.py       ← Simulação de dispositivos GoodWe  
    └── ia_engine.py    ← Inteligência Artificial (Random Forest)  

---

## 8. Como Executar o Projeto

### 1. Clone o repositório
git clone https://github.com/enzocerneviva/EnergyTime.git  
cd EnergyTime/backend  

### 2. Instale as dependências
pip install -r requirements.txt  

### 3. Configure variáveis de ambiente (.env)
OPENWEATHER_KEY = bd0575d8f212404126c33b80be9ea9d2  

### 4. Execute a aplicação
python main.py  
