# EnergyTime | Challenge

## Sobre o Projeto

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

### Benefícios do EnergyTime
- **Redução da emissão de CO₂**: incentivo ao uso de tecnologias que facilitam o aproveitamento da energia solar.  
- **Eficiência energética**: permite direcionar a energia para onde ela é mais necessária, seja armazenada ou consumida.  
- **Automação residencial**: integração com assistentes virtuais e controle inteligente de dispositivos.  

## 2. Organização da Aplicação

A estrutura do projeto **EnergyTime** é a seguinte:

```bash
EnergyTime/
|
├── README.md           ← Documento explicativo do projeto (você está lendo agora)
├── .env.example        ← Arquivo de exemplo com variáveis de ambiente, senhas e acessos
├── .gitignore          ← Arquivo para ignorar arquivos não versionados
├── requirements.txt    ← Arquivo com informações de ferramentas e bibliotecas utilizadas para importação
|
└── backend/
    ├── main.py         ← Roteador principal - cria o servidor com rotas HTTPS para comunicação com a Alexa

    ├── alexa_skill.py  ← Integração com Alexa - processa requisições (Intents) em JSON e retorna respostas JSON

    ├── weather.py      ← Dados climáticos - importa e trata previsões do OpenWeather para uso na IA

    ├── goodwe.py       ← Simulação de leitura de dados e envio de comandos para equipamentos GoodWe

    └── ia_engine.py    ← Motor de decisão com IA - treina modelo RandomForest para prever quedas de energia
                          com base em dados climáticos históricos 
```

## 3. Funcionamento

O fluxo pode ser dividido em 5 etapas principais:

1. **Interação com o usuário (Alexa)**  
   - O usuário faz um pedido de informação ou comando por voz.  
   - A Alexa envia essa requisição em formato **JSON** para a aplicação.  

2. **Roteamento e processamento inicial (`main.py` + `alexa_skill.py`)**  
   - O `main.py` recebe a requisição e direciona para o módulo responsável.  
   - O `alexa_skill.py` interpreta a *intent* da Alexa e prepara a resposta adequada.  

3. **Coleta de dados externos**  
   - O módulo `weather.py` acessa a API do **OpenWeather** para obter dados climáticos atualizados.  
   - O módulo `goodwe.py` simula a leitura e o controle de dispositivos GoodWe.  

4. **Decisão com Inteligência Artificial (`ia_engine.py`)**  
   - O motor de IA processa os dados climáticos.  
   - O modelo de **Random Forest** classifica se existe risco de queda de energia (0 = sem risco / 1 = risco alto).  
   - A decisão influencia como o carregamento será gerenciado (imediato, agendado ou interrompido).  

5. **Resposta ao usuário e execução de ações**  
   - O sistema retorna um JSON de resposta à Alexa.  
   - O usuário recebe feedback por voz.  
   - Se necessário, comandos são enviados para os dispositivos GoodWe.  
