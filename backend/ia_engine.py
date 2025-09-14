import pandas as pd # Manipulação e Análise de Dados
from sklearn.ensemble import RandomForestClassifier # Modelo de Classificação
from sklearn.model_selection import train_test_split # Função de separação de dados para treinamento do modelo
from sklearn.metrics import classification_report # Gera o resultado/acurácia do modelo
from weather import get_weather  # Importa todas as funções do módulo weather.py (incluindo get_weather).
import os

# 1. Carrega base de dados
caminho_arquivo = os.path.join(os.path.dirname(__file__), 'bases_de_dados', 'modelo_queda_de_energia', 'power_outages.csv')
df = pd.read_csv(caminho_arquivo, sep=",") 

# 2. Pré-processamento
df['data'] = pd.to_datetime(df['data'], dayfirst=True)

# Define as variáveis de entrada (features) e saída (target).
X = df[['precipitacao_total_mm', 'temperatura_media_c', 'umidade_relativa_%', 'vento_m_s']] # Variáveis independentes.
y = df['queda_de_energia'] # Variável dependente (0 ou 1, indicando queda de energia).

# Divide os dados em conjunto de treino e teste (80% treino, 20% teste).
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Cria e treina o modelo de Random Forest.
modelo = RandomForestClassifier(random_state=42)
modelo.fit(X_train, y_train)

# 3. Função de previsão de risco de queda de energia

def prever_risco(precipitacao, temperatura, umidade, vento):
    # Cria um DataFrame com os dados recebidos como entrada para o modelo.
    dados = pd.DataFrame([{
        'precipitacao_total_mm': precipitacao,
        'temperatura_media_c': temperatura,
        'umidade_relativa_%': umidade,
        'vento_m_s': vento
    }])
    return int(modelo.predict(dados)[0])  # Faz a previsão e retorna 0 (não) ou 1 (sim).


# 4. Previsão com base nos dados climáticos de hoje e amanhã

def prever_risco_com_previsao(lat, lon):
    previsao = get_weather(lat, lon) # Obtém a previsão do tempo usando a função importada do módulo weather.
    resultados = {}

    # Itera sobre os dias da previsão (hoje e amanhã).
    for dia in previsao:
        for chave, dados in dia.items():
            # Calcula o risco de queda de energia para cada dia.
            risco = prever_risco(
                precipitacao=dados['precipitacao'],
                temperatura=dados['temperatura'],
                umidade=dados['umidade'],
                vento=dados['vento']
            )

            # Armazena o resultado em um dicionário.
            resultados[chave] = {
                'dados_climaticos': dados,
                'queda_de_energia': risco
            }

    return resultados

# Função para gerar texto de resposta para a Alexa.
def previsaoQuedaDeEnergiaAlexa(lat, lon, estado):

    resultados = prever_risco_com_previsao(lat, lon) # Chama a função que faz a previsão baseada no clima.

    resultado_hoje = resultados["hoje"]["queda_de_energia"]
    resultado_amanha = resultados["amanhã"]["queda_de_energia"]
    
    saida = "De acordo com a análise climática esses foram os resultados obtidos. "

    # Gera o texto conforme as combinações possíveis dos resultados de hoje e amanhã.
    if (resultado_amanha and resultado_hoje) == 0:
        saida += "Previsão para hoje: sem risco de queda de energia. Previsão para amanhã: sem risco de queda de energia"
    elif resultado_hoje == 0 and resultado_amanha == 1:
        saida += "Previsão para hoje: sem risco de queda de energia. Previsão para amanhã: risco de queda de enegia"
    elif resultado_hoje == 1 and resultado_amanha == 0:
        saida += "Previsão para hoje: risco de queda de enegia. Previsão para amanhã: sem risco de queda de energia"
    else:
        saida += "Previsão para hoje: risco de queda de enegia. Previsão para amanhã: risco de queda de enegia"

    return saida


# 5. Execução direta para teste

# print("---------- Dados Treinamento de Modelo de Previsão ----------")

# # Faz a previsão no conjunto de teste e imprime um relatório de desempenho do modelo.
# y_pred = modelo.predict(X_test)
# print("Relatório de Classificação:\n")
# print(classification_report(y_test, y_pred))