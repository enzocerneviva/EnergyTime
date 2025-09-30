# EnergyTime | Challenge  

## 1. Sobre o Projeto  
O **EnergyTime** é um projeto acadêmico desenvolvido como desafio da **GoodWe** em parceria com a **FIAP**.  
O objetivo é criar uma aplicação que integre os equipamentos da GoodWe — como inversores, carregadores elétricos e baterias — com um **assistente virtual**, oferecendo **controle inteligente**, **automação** e **previsões baseadas em dados climáticos**.  

---

## 2. Equipe Envolvida  
- **Enzo Cardilli Cerneviva**  
- **Gustavo Cordeiro Braga** – RM: 562247  
- **Murilo Justino Arcanjo** – RM: 565470  
- **Rafael Quattrer Dalla Costa** – RM: 562052  

---

## 3. Esquema de Integração dos Componentes  

### 📌 Fluxo de Funcionamento
1. **Interação com o usuário (Alexa)**  
   - O usuário emite comandos por voz.  
   - A Alexa converte o comando em uma requisição JSON.  

2. **Roteamento da requisição**  
   - O `main.py` recebe a requisição.  
   - O `alexa_skill.py` interpreta a intent e prepara a resposta.  

3. **Coleta de dados externos**  
   - O `weather.py` consulta a API **OpenWeather**.  
   - O `goodwe.py` simula ou acessa dispositivos GoodWe.  

4. **Decisão com Inteligência Artificial**  
   - O `ia_engine.py` processa dados climáticos.  
   - Modelo **Random Forest** prevê quedas de energia.  

5. **Resposta e execução**  
   - Alexa retorna feedback ao usuário.  
   - Se necessário, comandos são enviados aos dispositivos GoodWe.  

### 📌 Diagrama de Blocos  
```mermaid
flowchart LR
    User["Usuário (voz)"] --> Alexa["Alexa Skill"]
    Alexa --> Main["main.py (Roteamento)"]
    Main --> Skill["alexa_skill.py (Processamento de intents)"]
    Skill --> Weather["weather.py (Dados climáticos)"]
    Skill --> GoodWe["goodwe.py (Simulação de dispositivos)"]
    Weather --> IA["ia_engine.py (Random Forest)"]
    GoodWe --> IA
    IA --> Skill
    Skill --> Alexa
    Alexa --> User
