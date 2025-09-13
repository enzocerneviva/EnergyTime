import pandas as pd
!pip install xlrd

df = pd.read_excel('/content/BaseDeDados_BATERIA_MENSAL.xls', engine="xlrd", header=None)

df.columns = ["Monthly Report", "Plant", "Classification", "Capacity(kW)", "PV(kWh)", "Sell(kWh)", "Buy(kWh)", "Consumption(kWh)", "In-House(kWh)", "Self-Cons. Ratio(%)", "Contribution Ratio(%)", "Income(EUR)"]
df = df.iloc[20:-1].copy()
display(df.head(33))

# Converter colunas relevantes para numérico, forçando erros
df['Consumption(kWh)'] = pd.to_numeric(df['Consumption(kWh)'], errors='coerce')
df['Income(EUR)'] = pd.to_numeric(df['Income(EUR)'], errors='coerce')

# Remover linhas com valores NaN que resultaram da coerção
df.dropna(subset=['Consumption(kWh)', 'Income(EUR)'], inplace=True)


# Calcular o consumo mensal total
total_monthly_consumption_bat = df['Consumption(kWh)'].sum()

# Calcular o número de dias nos dados
number_of_days_bat = len(df)

# Calcular o consumo médio diário
daily_average_consumption_bat = total_monthly_consumption_bat / number_of_days_bat

# Calcular a renda total
total_income_bat = df['Income(EUR)'].sum()

print(f"Consumo Mensal Total (Dados da Bateria): {total_monthly_consumption_bat:.2f} kWh")
print(f"Consumo Médio Diário (Dados da Bateria): {daily_average_consumption_bat:.2f} kWh")
print(f"Renda Mensal Total (Dados da Bateria): {total_income_bat:.2f} EUR")
