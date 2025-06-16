
#? ==========================================
#? alexa_skill.py - Integração com Alexa
#? ==========================================

#? Este arquivo é responsável por lidar com as requisições vindas da Skill da Alexa.
#? A Skill envia comandos como "iniciar carregamento", "parar carregamento" etc.
#? Aqui processamos o JSON recebido, identificamos a intent e geramos a resposta de voz.

#? Estrutura básica da integração:
#? -------------------------------
#? 1. Receber uma requisição POST da Alexa (endpoint configurado no Developer Console)
#? 2. Verificar qual intent foi enviada (ex: IniciarCarregamentoIntent)
#? 3. Executar a ação correspondente (ex: chamar função que ativa carregamento)
#? 4. Retornar uma resposta JSON no formato aceito pela Alexa

#? Principais Intents Esperadas:
#? -----------------------------
#? - IniciarCarregamentoIntent: ativa o carregamento veicular
#? - PararCarregamentoIntent: desativa o carregamento
#? - StatusEnergiaIntent: informa ao usuário o estado atual (carregando ou não)

#? Exemplo de estrutura JSON recebida:
#? {
#?   "request": {
#?     "type": "IntentRequest",
#?     "intent": {
#?       "name": "IniciarCarregamentoIntent"
#?     }
#?   }
#? }

#? Exemplo de resposta esperada pela Alexa:
#? {
#?   "version": "1.0",
#?   "response": {
#?     "outputSpeech": {
#?       "type": "PlainText",
#?       "text": "Carregamento iniciado com energia limpa!"
#?     },
#?     "shouldEndSession": true
#?   }
#? }

#? Funções esperadas neste arquivo:
#? --------------------------------
#? - handle_intent(intent_name): interpreta a intent recebida e gera a resposta.
#? - build_response(text): cria o JSON de resposta no formato da Alexa.
#? - alexa_webhook(request): endpoint que lida com requisições HTTP da Alexa.

#? Observação:
#? -----------
#? - A autenticação e validação da requisição (signature, timestamp) são importantes em produção.
#? - Para testes, essas validações podem ser desativadas no Developer Console.

#? ==========================================
#? Fim da explicação sobre a integração Alexa
#? ==========================================
