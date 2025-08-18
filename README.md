# EnergyTime | Challenge

# 📌 EnergyTime

## 🚀 Sobre o Projeto

O **EnergyTime** é um projeto acadêmico desenvolvido como desafio da **GoodWe** em parceria com a **FIAP**.  
O objetivo é criar uma aplicação que integre os equipamentos da GoodWe — como inversores, carregadores elétricos e baterias — com um assistente virtual, oferecendo controle inteligente e previsões baseadas em dados.  

O projeto **está em desenvolvimento**, e o planejamento é implementar as seguintes funcionalidades na aplicação:

1. **Integração com dispositivos GoodWe**  
   O usuário poderá se comunicar com os equipamentos da GoodWe por comandos de voz via **Alexa**. Entre as ações previstas estão:  
   - Consultar informações do inversor.  
   - Ligar ou desligar dispositivos.  
   - Executar outras funcionalidades do sistema integrado.  

2. **Informações sobre horários de maior incidência solar**  
   Com base na **localização geográfica** e no **ângulo das placas solares**, o sistema determinará os horários de maior incidência solar e, portanto, maior geração de energia. A Alexa poderá:  
   - Informar esses horários ao usuário.  
   - Direcionar a energia gerada para equipamentos específicos durante o pico de produção.  

3. **Previsão de quedas de energia via Inteligência Artificial**  
   O projeto inclui um modelo de IA capaz de prever possíveis quedas de energia com base em dados meteorológicos, como:  
   - Data  
   - Umidade relativa do ar  
   - Volume de chuva (mm)  
   - Velocidade do vento  
   - Temperatura  

   Com base em padrões históricos, o sistema alertará o usuário para se preparar — seja armazenando energia ou carregando equipamentos com antecedência.  

### 🌱 Benefícios do EnergyTime
- **Redução da emissão de CO₂**: incentivo ao uso de tecnologias que facilitam o aproveitamento da energia solar.  
- **Eficiência energética**: permite direcionar a energia para onde ela é mais necessária, seja armazenada ou consumida.  
- **Automação residencial**: integração com assistentes virtuais e controle inteligente de dispositivos.  


## 2. Organização Github

projeto-alexa-carregador/
- README.md
- .env.example
- .gitignore
- backend/
  - main.py ← Roteador principal
  - alexa_skill.py ← Integração Alexa
  - weather.py ← Dados climáticos
  - goodwe.py ← Comunicação com API da GoodWe
  - ia_engine.py ← Motor de decisão com IA
  - hardware_interface/
    - __init__.py ← Escolhe dinamicamente o adaptador (ESP32 ou API)
    - esp32_adapter.py ← Comunicação via MQTT com ESP32 (opcional)
    - api_adapter.py ← Comunicação via API ou simulação local
- esp32/ ← (Opcional: código embarcado para ESP32)
  - main.ino ← Código do ESP32 com controle via MQTT

