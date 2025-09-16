import pandas as pd
from datetime import datetime, timedelta

# Substitua pelo caminho do seu arquivo CSV
arquivo_csv = '/content/dados_mensais_bauner.csv'

# Lê o CSV
df = pd.read_csv(arquivo_csv)

# Remove a última linha que contém o total, pois não é uma data válida
df = df.iloc[:-1]

# Mostra as colunas para conferir - Removed as requested
# print("Colunas encontradas no CSV:", df.columns)

# Ajusta o nome da coluna de tempo (troque conforme necessário)
coluna_tempo = None
for nome in df.columns:
    if "time" in nome.lower() or "data" in nome.lower():
        coluna_tempo = nome
        break

if coluna_tempo is None:
    raise ValueError("❌ Nenhuma coluna de tempo encontrada no CSV!")

# Converte a coluna escolhida para datetime
df[coluna_tempo] = pd.to_datetime(df[coluna_tempo], dayfirst=True)

# Add a column for Renda in Brazilian Real
EXCHANGE_RATE_EUR_BRL = 6.28
if 'Renda(EUR)' in df.columns:
    df['Renda(BRL)'] = df['Renda(EUR)'] * EXCHANGE_RATE_EUR_BRL


def mostrar_registro(data_base):
    """Mostra o registro do dia escolhido (sem horário)"""
    # Compare only the date part
    registros = df[df[coluna_tempo].dt.date == data_base.date()]

    if not registros.empty:
        # Pega o último registro do dia
        row = registros.iloc[-1]


        print("\n==========================")
        print(f"Registro do dia {data_base.strftime('%d/%m/%Y')}")
        print("==========================")

        # Show key values from available columns
        if 'PV(kWh)' in df.columns:
            print(f"Geração Solar (PV): {row['PV(kWh)']:.2f} kWh")
        if 'Consumo(kWh)' in df.columns:
            print(f"Consumo Total: {row['Consumo(kWh)']:.2f} kWh")
        if 'Compra(kWh)' in df.columns:
            print(f"Compra da Rede Elétrica: {row['Compra(kWh)']:.2f} kWh")
        if 'Venda(kWh)' in df.columns:
            print(f"Venda para Rede Elétrica: {row['Venda(kWh)']:.2f} kWh")
        if 'In-house(kWh)' in df.columns:
            print(f"Autoconsumo (In-house): {row['In-house(kWh)']:.2f} kWh")
        if 'Renda(EUR)' in df.columns:
            print(f"Renda Gerada: {row['Renda(EUR)']:.2f} EUR")
        if 'Renda(BRL)' in df.columns:
            print(f"Renda Gerada: {row['Renda(BRL)']:.2f} BRL")


        # Explanation about battery usage based on available data
        # We cannot determine exact battery charge/discharge from this daily data,
        # but we can show related metrics.
        print("\nInformações Adicional (Diária Total):")
        if 'Compra(kWh)' in df.columns and row['Compra(kWh)'] > 0:
            print(f"⚡ Energia comprada da rede elétrica: {row['Compra(kWh)']:.2f} kWh")
        elif 'Compra(kWh)' in df.columns:
             print("⚡ Nenhuma energia comprada da rede elétrica neste dia.")

        # We cannot directly report battery usage 'from' the battery with this data.
        # The 'In-house(kWh)' might represent energy used directly from PV or potentially battery,
        # but it's not explicit battery discharge.
        # We will report In-house consumption as it's the closest available metric for self-consumption.
        if 'In-house(kWh)' in df.columns:
            print(f"🏠 Autoconsumo (energia usada diretamente): {row['In-house(kWh)']:.2f} kWh")


        # Display all available columns for the last row (optional, for debugging/details)
        # print("\nInformações completas do último registro:")
        # for col in df.columns:
        #     print(f"{col}: {row[col]}")


    else:
        print(f"⚠️ Nenhum registro encontrado para {data_base.strftime('%d/%m/%Y')}.")


# Get the range of dates in the dataframe
primeira_data = df[coluna_tempo].min()
ultima_data = df[coluna_tempo].max()

# Start a loop to ask the user if they want to analyze a specific day
while True:
    analisar_outro_dia = input(f"Quer analisar um dia específico entre {primeira_data.strftime('%d/%m/%Y')} e {ultima_data.strftime('%d/%m/%Y')}? (s/n/sair): ").lower()

    if analisar_outro_dia == 'sair':
        print("Saindo do programa.")
        break
    elif analisar_outro_dia == 's':
        while True:
            data_str = input(f"Digite a data que deseja analisar no formato DD/MM/AAAA: ")
            try:
                data_analise = datetime.strptime(data_str, '%d/%m/%Y')

                # Check if the entered date is within the available range (compare only dates)
                if primeira_data.date() <= data_analise.date() <= ultima_data.date():
                    mostrar_registro(data_analise)
                    break # Exit the inner loop after showing the record
                else:
                    print(f"❌ Data fora do intervalo disponível. Por favor, digite uma data entre {primeira_data.strftime('%d/%m/%Y')} e {ultima_data.strftime('%d/%m/%Y')}.")
            except ValueError:
                print("❌ Formato de data inválido. Por favor, use o formato DD/MM/AAAA.")
    elif analisar_outro_dia == 'n':
        # Always gets the most recent day if the user doesn't want to analyze a specific day
        mostrar_registro(ultima_data)
        break # Exit the outer loop after showing the most recent day
    else:
        print("Opção inválida. Por favor, digite 's' para sim, 'n' para não, ou 'sair' para sair.")
