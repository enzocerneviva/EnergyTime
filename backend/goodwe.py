import pandas as pd
import os

caminho_inversor = os.path.join(os.path.dirname(__file__), 'base_de_dados', 'dados_inversor.json')
dados_inversor = pd.read_json(caminho_inversor)

def carregar_carro():
    print("Carregando Carro")

def analise_inversor():

    print("\nAnalisando dados do inversor...\n")
    result = "Dados obtidos: "
    for dado in dados_inversor:

        if dado in ["tensao_dc", "corrente_dc", "tensao_ac", "corrente_ac", "tempo_atividade_total"]:
            continue
        
        for info in dados_inversor[dado]:

            if "energia" in dado:
                result += f"{dado}: {info} quilowatt-hora, "
                continue

            if "potencia" in dado:
                result += f"{dado}: {info} watts, "
                continue
            
            if "percentual" in dado:
                result += f"{dado}: {info} %, "
                continue
                
            result += f"{dado}: {info}, "

    return result


print(analise_inversor(), "\n\n")