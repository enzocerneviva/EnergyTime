# EnergyTime | Challenge 1° Semestre

## 🎯 1. Objetivo Geral

Desenvolver uma solução automatizada que permita ao usuário configurar e monitorar o carregamento de veículos elétricos via comandos na Alexa, com base em:

- Dados preditivos como clima e possíveis quedas de energia.
- Preferências personalizadas salvas em banco de dados.
- **Leitura e análise em tempo real dos dados do inversor solar**, permitindo estimar a melhor janela de carregamento com base na eficiência da geração solar e nos dados de consumo.

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

## 🔋 3. Aplicações de Energia Renovável e Tecnologias Inteligentes

### Sustentabilidade Ambiental

- Redução direta de emissões de CO₂ com uso de energia solar
- Adoção de práticas mais conscientes com uso automatizado

### Independência Energética

- Geração própria reduz dependência da rede
- Energia armazenada pode ser usada em situações emergenciais

### Eficiência Energética

- Com a leitura do inversor, é possível:
    - Otimizar horários de carregamento com base na geração solar
    - Evitar sobrecargas e desperdícios
    - Detectar falhas no sistema de geração
- Decisões inteligentes com IA permitem reduzir perdas

### Automação Residencial/Industrial

- Controle por comandos de voz com Alexa
- Monitoramento contínuo do desempenho dos equipamentos

---

## ⚠️ 4. Possíveis Desafios

- Limitações no acesso à API oficial da GoodWe (conta corporativa exigida)
- Restrições de segurança da Alexa em comandos automatizados
- Precisão das previsões climáticas
- Segurança e criptografia dos dados sensíveis
- Treinamento eficaz da IA com bases realistas

---

## ✅ 5. Conclusão

A integração entre os equipamentos da GoodWe, a assistente Alexa e sistemas inteligentes abre novas possibilidades para automação sustentável e consciente. Utilizar dados climáticos, informações do inversor e IA para otimizar o carregamento veicular pode tornar o consumo energético mais eficiente, econômico e ecológico.

Com uma equipe organizada, acesso à documentação técnica e boas práticas de programação, este projeto tem potencial real de aplicação em residências inteligentes e, futuramente, até em ambientes corporativos ou industriais, contribuindo para a transição energética global.
