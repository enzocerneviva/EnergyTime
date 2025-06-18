from base_de_dados import dados_inversor

inversor = dados_inversor
lista_dados_inversor = inversor.json()



def carregar_carro():
    print("Carregando Carro")

def analise_inversor():
    print("Analisando dados do inversor...")
    print("Dados obtidos: ", lista_dados_inversor)

analise_inversor()