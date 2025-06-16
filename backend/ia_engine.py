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
    print("Previsão climática recebida:", previsao)

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

#? 5. Execução direta para teste
if __name__ == '__main__':
    y_pred = modelo.predict(X_test)
    print("Relatório de Classificação:\n")
    print(classification_report(y_test, y_pred))

    resultados = prever_risco_com_previsao()

    print("\nPrevisão de risco com base no clima:")
    for dia, info in resultados.items():
        print(f"{dia.capitalize()}:")
        print(f"  → Dados climáticos: {info['dados_climaticos']}")
        print(f"  → Queda de energia prevista: {'Sim' if info['queda_de_energia'] == 1 else 'Não'}\n")


