import pandas as pd
!pip install xlrd

df = pd.read_excel('/content/BaseDeDados_INVERSOR_MENSAL.xls', engine="xlrd", header=None)

df.columns = ["Monthly Report", "Plant", "Classification", "Capacity(kW)", "Generation(kWh)", "Income(EUR)"] # renomeando as colunas
df = df.iloc[20:-1].copy() # removendo as linhas desnecessárias
display(df.head(33))

print(df.columns)

# Renomeando as colunas
df.columns = ["Monthly Report", "Plant", "Classification", "Capacity(kW)", "Generação(kWh)", "Renda(EUR)"]

# Converter colunas 'Generação(kWh)' e 'Renda(EUR)' para numérico, forçando erros
df['Generação(kWh)'] = pd.to_numeric(df['Generação(kWh)'], errors='coerce')
df['Renda(EUR)'] = pd.to_numeric(df['Renda(EUR)'], errors='coerce')

# Remover linhas com valores NaN que resultaram da coerção
df.dropna(subset=['Generação(kWh)', 'Renda(EUR)'], inplace=True)

# Calcular a geração mensal total (como consumo da perspectiva do inversor)
total_monthly_generation = df['Generação(kWh)'].sum()

# Calcular o número de dias nos dados
number_of_days = len(df)

# Calcular a geração média diária
daily_average_generation = total_monthly_generation / number_of_days

# Calcular a renda total
total_income = df['Renda(EUR)'].sum()

print(f"Geração Mensal Total (Dados do Inversor): {total_monthly_generation:.2f} kWh")
print(f"Geração Média Diária (Dados do Inversor): {daily_average_generation:.2f} kWh")
print(f"Renda Mensal Total (Dados do Inversor): {total_income:.2f} EUR")
