# Importações e leitura dos dados
import pandas as pd
import os

# Caminho para o arquivo JSON com dados do inversor, relativo ao arquivo atual
caminho_inversor = os.path.join(os.path.dirname(__file__), 'base_de_dados', 'solat_inverter_data.json')
dados_inversor = pd.read_json(caminho_inversor)  # Lê os dados do inversor em um DataFrame

# Função simulada para carregar o carro (placeholder)
def ligarCarregador():
    text = "Carregamento do carro iniciado com sucesso!"
    return text

def desligarCarregador():
    text = "Carregamento parado com segurança."
    return text

# Função para analisar e formatar os dados do inversor
def analiseInversor():
    print("\nAnalisando dados do inversor...\n")
    result = "Dados obtidos: "

    # Itera pelas colunas do DataFrame
    for dado in dados_inversor:
        # Ignora algumas colunas específicas
        if dado in ["tensao_dc", "corrente_dc", "tensao_ac", "corrente_ac", "tempo_atividade_total"]:
            continue
        
        # Itera pelos valores da coluna atual
        for info in dados_inversor[dado]:
            # Formata a saída de acordo com o tipo do dado
            if "energia" in dado:
                result += f"{dado.replace('_', ' ')}: {info} quilowatt-hora, "
                continue

            if "potencia" in dado:
                result += f"{dado.replace('_', ' ')}: {info} watts, "
                continue
            
            if "percentual" in dado:
                result += f"{dado.replace('_', ' ')}: {info} %, "
                continue
                
            # Caso geral para outros dados
            result += f"{dado.replace('_', ' ')}: {info}, "

    return result

# Executa a análise e imprime o resultado formatado
print(analise_inversor())
