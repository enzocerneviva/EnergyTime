import pandas as pd # Manipulação e Análise de Dados
from sklearn.ensemble import RandomForestClassifier # Modelo de Classificação
from sklearn.model_selection import train_test_split # Função de separação de dados para treinamento do modelo
from sklearn.metrics import classification_report # Gera o resultado/acurácia do modelo
from weather import get_weather # Importa todas as funções do módulo weather.py (incluindo get_weather).
import os

# 1. Carrega base de dados
caminho_arquivo = os.path.join(os.path.dirname(__file__), 'bases_de_dados', 'modelo_queda_de_energia', 'base_final_ajustada_v2.csv')
df = pd.read_csv(caminho_arquivo, sep=",") 

# 2. Pré-processamento
df['data'] = pd.to_datetime(df['data'], format="%Y-%m-%d")

### CORREÇÃO 1: Tratar valores ausentes (NaN) ###
# Seu modelo falhará se encontrar 'NaN' (como no 'vento_m_s' da sua amostra).
# Vamos preencher com a mediana e salvar a mediana para usar na previsão.
colunas_features_numericas = ['precipitacao_total_mm', 'temperatura_media_c', 'umidade_relativa_%', 'vento_m_s']
MEDIANAS = {}
for col in colunas_features_numericas:
    mediana = df[col].median()
    df[col].fillna(mediana, inplace=True)
    MEDIANAS[col] = mediana

### CORREÇÃO 2: Tratar coluna de texto 'ESTADO' (One-Hot Encoding) ###
# Converte a coluna 'ESTADO' em colunas numéricas (ESTADO_RJ, ESTADO_MG, etc.)
# O 'df' original é substituído por este novo DataFrame processado.
df = pd.get_dummies(df, columns=['ESTADO'])

# Define as variáveis de entrada (features) e saída (target).
# 'y' é o seu gabarito, como você corretamente apontou.
y = df['queda_de_energia'] # Variável dependente (0 ou 1).

# 'X' são todas as colunas de features, *exceto* o gabarito ('y') e colunas
# que não usamos no modelo (como 'data' e 'ESTACAO' da sua amostra).
colunas_para_excluir_de_X = ['data', 'queda_de_energia', 'ESTACAO']
X = df.drop(columns=colunas_para_excluir_de_X, errors='ignore')

### CORREÇÃO 3: Salvar a lista exata de colunas do modelo ###
# Isso é VITAL para a função 'prever_risco' funcionar.
# Garante que a ordem e os nomes (ex: 'ESTADO_RJ') sejam idênticos.
COLUNAS_DO_MODELO = X.columns.tolist()

# Divide os dados em conjunto de treino e teste (80% treino, 20% teste).
# X e y agora estão limpos e prontos para o modelo.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Cria e treina o modelo de Random Forest.
print("Treinando o modelo com colunas numéricas e 'ESTADO' processado...")
modelo = RandomForestClassifier(random_state=42)
modelo.fit(X_train, y_train)
print("Modelo treinado com sucesso.")

# 3. Função de previsão de risco de queda de energia (AJUSTADA)

def prever_risco(precipitacao, temperatura, umidade, vento, estado):
    """
    Esta função agora recebe os dados brutos (incluindo a string 'estado')
    e os transforma EXATAMENTE no formato que o modelo foi treinado.
    """
    
    # Cria um DataFrame de 1 linha com os dados recebidos.
    dados_raw = pd.DataFrame([{
        'precipitacao_total_mm': precipitacao,
        'temperatura_media_c': temperatura,
        'umidade_relativa_%': umidade,
        'vento_m_s': vento,
        'ESTADO': estado # A string (ex: "SP")
    }])

    # Trata Nones/NaNs (caso 'get_weather' falhe) usando as medianas salvas.
    for col in colunas_features_numericas:
        dados_raw[col].fillna(MEDIANAS[col], inplace=True)

    # Aplica o MESMO One-Hot Encoding que fizemos no treino.
    dados_processados = pd.get_dummies(dados_raw, columns=['ESTADO'])
    
    # ALINHAMENTO DAS COLUNAS (O passo mais importante):
    # Garante que este DataFrame de 1 linha tenha as mesmas colunas
    # (ex: 'ESTADO_RJ', 'ESTADO_MG', 'ESTADO_SP') que o modelo espera,
    # na mesma ordem, preenchendo com 0 as que não correspondem.
    dados_finais = dados_processados.reindex(columns=COLUNAS_DO_MODELO, fill_value=0)

    # Faz a previsão e retorna 0 ou 1.
    return int(modelo.predict(dados_finais)[0]) 


# 4. Previsão com base nos dados climáticos de hoje e amanhã
# (Nenhuma mudança necessária aqui, pois ela chama a 'prever_risco' corrigida)
def prever_risco_com_previsao(lat, lon, estado):
    previsao = get_weather(lat, lon) 
    resultados = {}

    for dia in previsao:
        for chave, dados in dia.items():
            risco = prever_risco(
                precipitacao=dados['precipitacao'],
                temperatura=dados['temperatura'],
                umidade=dados['umidade'],
                vento=dados['vento'],
                estado=estado # Passa a string "SP", "RJ", etc.
            )

            resultados[chave] = {
                'dados_climaticos': dados,
                'queda_de_energia': risco
            }

    return resultados

# 5. Função para gerar texto de resposta para a Alexa.
# (Nenhuma mudança necessária aqui, apenas uma pequena correção na sua lógica 'if')
def previsaoQuedaDeEnergiaAlexa(lat, lon, estado):

    resultados = prever_risco_com_previsao(lat, lon, estado) 

    resultado_hoje = resultados["hoje"]["queda_de_energia"]
    resultado_amanha = resultados["amanhã"]["queda_de_energia"]
    
    saida = "De acordo com a análise climática esses foram os resultados obtidos. "

    # (Lógica 'if' corrigida para ser mais clara)
    if resultado_hoje == 0 and resultado_amanha == 0:
        saida += "Previsão para hoje: sem risco de queda de energia. Previsão para amanhã: sem risco de queda de energia."
    elif resultado_hoje == 0 and resultado_amanha == 1:
        saida += "Previsão para hoje: sem risco de queda de energia. Previsão para amanhã: risco de queda de energia." # 'energia' corrigido
    elif resultado_hoje == 1 and resultado_amanha == 0:
        saida += "Previsão para hoje: risco de queda de energia. Previsão para amanhã: sem risco de queda de energia." # 'energia' corrigido
    else: # Ambos são 1
        saida += "Previsão para hoje: risco de queda de energia. Previsão para amanhã: risco de queda de energia." # 'energia' corrigido

    return saida


# 6. Execução direta para teste (Descomentado para você ver)

print("\n---------- Dados Treinamento de Modelo de Previsão ----------")

# Faz a previsão no conjunto de teste e imprime um relatório de desempenho.
# X_test já foi processado (dummies e NaNs) junto com X_train.
y_pred = modelo.predict(X_test)
print("Relatório de Classificação:\n")
# 'zero_division=0' evita avisos caso uma classe nunca seja prevista no teste.
print(classification_report(y_test, y_pred, zero_division=0))