# scikit-learn
#? ia_engine.py — Módulo de IA para previsão de queda de energia

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os
from weather import *  #? Importa a função get_weather() existente

#? 1. Carrega base de dados
caminho_base = os.path.join(os.path.dirname(__file__), 'base_de_dados', 'ocorrencias_queda_de_energia.csv')
df = pd.read_csv(caminho_base)

#? 2. Pré-processamento
df['data'] = pd.to_datetime(df['data'], dayfirst=True)

X = df[['precipitacao_total_mm', 'temperatura_media_c', 'umidade_relativa_%', 'vento_m_s']]
y = df['queda_de_energia']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

modelo = RandomForestClassifier(random_state=42)
modelo.fit(X_train, y_train)

#? 3. Função de previsão de risco de queda de energia
def prever_risco(precipitacao, temperatura, umidade, vento):
    dados = pd.DataFrame([{
        'precipitacao_total_mm': precipitacao,
        'temperatura_media_c': temperatura,
        'umidade_relativa_%': umidade,
        'vento_m_s': vento
    }])
    return int(modelo.predict(dados)[0])  #? 0 = não, 1 = sim

#? 4. Previsão com base nos dados climáticos de hoje e amanhã
def prever_risco_com_previsao():
    previsao = get_weather()
    resultados = {}

    for dia in previsao:
        for chave, dados in dia.items():
            risco = prever_risco(
                precipitacao=dados['precipitacao'],
                temperatura=dados['temperatura'],
                umidade=dados['umidade'],
                vento=dados['vento']
            )

            resultados[chave] = {
                'dados_climaticos': dados,
                'queda_de_energia': risco
            }

    return resultados

def texto_alexa():

    resultados = prever_risco_com_previsao()

    resultado_hoje = resultados["hoje"]["queda_de_energia"]
    resultado_amanha = resultados["amanhã"]["queda_de_energia"]
    
    saida = "De acordo com a análise climática esses foram os resultados obtidos. "

    if (resultado_amanha and resultado_hoje) == 0:
        saida += "Previsão para hoje: sem risco de queda de energia. Previsão para amanhã: sem risco de queda de energia"
    elif resultado_hoje == 0 and resultado_amanha == 1:
        saida += "Previsão para hoje: sem risco de queda de energia. Previsão para amanhã: risco de queda de enegia"
    elif resultado_hoje == 1 and resultado_amanha == 0:
        saida += "Previsão para hoje: risco de queda de enegia. Previsão para amanhã: sem risco de queda de energia"
    else:
        saida += "Previsão para hoje: risco de queda de enegia. Previsão para amanhã: risco de queda de enegia"

    return saida

#? 5. Execução direta para teste

y_pred = modelo.predict(X_test)
print("Relatório de Classificação:\n")
print(classification_report(y_test, y_pred))

print(prever_risco_com_previsao())