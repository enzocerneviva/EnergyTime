# goodwe.py
import pandas as pd
import os
from datetime import datetime, timedelta

# -----------------------------
# Carregamento dos dados
# -----------------------------
# JSON do inversor (se ainda for necessário)
# caminho_inversor_json = os.path.join(os.path.dirname(__file__), 'bases_de_dados', 'equipamentos_e_plantas', 'solar_inverter_data.json')
# dados_inversor = pd.read_json(caminho_inversor_json)

# CSVs (ajuste caminhos se estiver no Colab)
dados_mensais_inversor = pd.read_csv('/content/dados_mensais_inversor.csv')
dados_mensais_bauner = pd.read_csv('/content/dados_mensais_bauner.csv')
dados_bateria_diario = pd.read_csv('/content/dados_bateria_diario.csv')
dados_inversor_diario = pd.read_csv('/content/dados_inversor_diario.csv')

# Renomear e tratar colunas para dados_mensais_inversor
dados_mensais_inversor.columns = ["Monthly Report", "Plant", "Classification", "Capacity(kW)", "Generação(kWh)", "Renda(EUR)"]
# Convert 'Monthly Report' to datetime for easier filtering
dados_mensais_inversor['Monthly Report'] = pd.to_datetime(dados_mensais_inversor['Monthly Report'], format='%d.%m.%Y', errors='coerce')
dados_mensais_inversor['Generação(kWh)'] = pd.to_numeric(dados_mensais_inversor['Generação(kWh)'], errors='coerce')
dados_mensais_inversor['Renda(EUR)'] = pd.to_numeric(dados_mensais_inversor['Renda(EUR)'], errors='coerce')
dados_mensais_inversor.dropna(subset=['Monthly Report', 'Generação(kWh)', 'Renda(EUR)'], inplace=True)

# Convert 'Data(Dias)' in dados_mensais_bauner to datetime for easier filtering
dados_mensais_bauner['Data(Dias)'] = pd.to_datetime(dados_mensais_bauner['Data(Dias)'], format='%d.%m.%Y', errors='coerce')
dados_mensais_bauner.dropna(subset=['Data(Dias)'], inplace=True)

# Convert 'Time (5 min)' in daily dataframes to datetime
dados_bateria_diario['Time (5 min)'] = pd.to_datetime(dados_bateria_diario['Time (5 min)'], format='%d.%m.%Y %H:%M:%S', errors='coerce')
dados_inversor_diario['Time (5 min)'] = pd.to_datetime(dados_inversor_diario['Time (5 min)'], format='%d.%m.%Y %H:%M:%S', errors='coerce')

# Drop rows with invalid dates
dados_bateria_diario.dropna(subset=['Time (5 min)'], inplace=True)
dados_inversor_diario.dropna(subset=['Time (5 min)'], inplace=True)


# Get today's date
today = datetime.now().date()
today_day = today.day

# Filter monthly dataframes for today's day
dados_inversor_hoje = dados_mensais_inversor[dados_mensais_inversor['Monthly Report'].dt.day == today_day]
dados_bauner_hoje = dados_mensais_bauner[dados_mensais_bauner['Data(Dias)'].dt.day == today_day]


# -----------------------------
# Funções de automação
# -----------------------------
def ligarCarregador():
    return "Carregamento do carro iniciado com sucesso!"

def desligarCarregador():
    return "Carregamento parado com segurança."

def ligarLuz():
    return "As luzes foram acesas."

def desligarLuz():
    return "As luzes foram apagadas."

def ligarArCondicionado():
    return "O ar-condicionado foi ligado."

def desligarArCondicionado():
    return "O ar-condicionado foi desligado."

def ligarTomada():
    return "A tomada inteligente foi ativada."

def desligarTomada():
    return "A tomada inteligente foi desligada."

# -----------------------------
# Funções de análise de energia
# -----------------------------
def get_nearest_time_entry(df, time_column, target_time):
    """Finds the row in a dataframe with the time closest to the target time."""
    if df.empty:
        return None
    # Calculate the absolute difference between the target time and the time in the dataframe
    time_diff = abs(df[time_column] - target_time)
    # Find the index of the minimum difference
    nearest_index = time_diff.idxmin()
    # Return the row at the nearest index
    return df.loc[nearest_index]


def analiseInversor_csv():
    # Use filtered data for today's day
    if not dados_inversor_hoje.empty:
        total_daily_generation = dados_inversor_hoje['Generação(kWh)'].sum()
        total_daily_income = dados_inversor_hoje['Renda(EUR)'].sum()
        result = f"Geração do dia {today_day} (Inversor): {total_daily_generation:.2f} kWh\n"
        result += f"Renda do dia {today_day} (Inversor): {total_daily_income:.2f} EUR"
        return result
    return f"Dados do inversor para o dia {today_day} não encontrados nos dados mensais."


def getConsumoMensal():
    # Use filtered data for today's day
    if not dados_bauner_hoje.empty:
        if "Consumo(kWh)" in dados_bauner_hoje.columns:
            consumo = dados_bauner_hoje["Consumo(kWh)"].sum()
            return f"O consumo total da casa no dia {today_day} foi de {consumo:.2f} kWh."
        return "Coluna 'Consumo(kWh)' não encontrada nos dados da Bauner."
    return f"Dados da Bauner para o dia {today_day} não encontrados nos dados mensais."


def getGeracaoDiaria():
    current_time = datetime.now()
    nearest_entry = get_nearest_time_entry(dados_inversor_diario, 'Time (5 min)', current_time)
    if nearest_entry is not None and "PV(W)" in nearest_entry:
        energia = nearest_entry["PV(W)"]
        # Format the time for the output message
        time_str = nearest_entry['Time (5 min)'].strftime('%H:%M')
        return f"A geração solar às {time_str} foi de {energia:.2f} watts."
    return "Dados diários do inversor para o horário atual não encontrados ou coluna 'PV(W)' ausente."


def getStatusBateria():
    current_time = datetime.now()
    nearest_entry = get_nearest_time_entry(dados_bateria_diario, 'Time (5 min)', current_time)
    if nearest_entry is not None and "Estado de Carga(%)" in nearest_entry:
        carga = nearest_entry["Estado de Carga(%)"]
        # Format the time for the output message
        time_str = nearest_entry['Time (5 min)'].strftime('%H:%M')
        return f"O nível da bateria às {time_str} é de {carga:.2f}%."
    return "Dados diários da bateria para o horário atual não encontrados ou coluna 'Estado de Carga(%)' ausente."

def getEnergiaRede():
    current_time = datetime.now()
    nearest_entry = get_nearest_time_entry(dados_bateria_diario, 'Time (5 min)', current_time)
    if nearest_entry is not None and "Grade(Rede Elétrica)(W)" in nearest_entry:
        rede = nearest_entry["Grade(Rede Elétrica)(W)"]
        # Format the time for the output message
        time_str = nearest_entry['Time (5 min)'].strftime('%H:%M')
        return f"A energia consumida da rede às {time_str} foi de {rede:.2f} watts."
    return "Dados diários da bateria para o horário atual não encontrados ou coluna 'Grade(Rede Elétrica)(W)' ausente."

def get_daily_inverter_generation():
    """Calculates the total daily solar generation from the daily inverter data."""
    if not dados_inversor_diario.empty and "PV(W)" in dados_inversor_diario.columns:
        # Assuming the data is in 5-minute intervals, convert W to kWh by summing and dividing by 12 (5-min intervals per hour) and 1000 (W to kW)
        total_generation_wh = dados_inversor_diario["PV(W)"].sum() * (5/60)
        total_generation_kwh = total_generation_wh / 1000
        return f"Geração solar total do dia (dados diários): {total_generation_kwh:.2f} kWh."
    return "Dados diários do inversor não encontrados ou coluna 'PV(W)' ausente."

def get_average_battery_level():
    """Calculates the average daily battery level from the daily battery data."""
    if not dados_bateria_diario.empty and "Estado de Carga(%)" in dados_bateria_diario.columns:
        average_charge = dados_bateria_diario["Estado de Carga(%)"].mean()
        return f"Nível médio da bateria no dia (dados diários): {average_charge:.2f}%."
    return "Dados diários da bateria não encontrados ou coluna 'Estado de Carga(%)' ausente."

def get_daily_data_range():
    """Gets the time range covered by the daily dataframes."""
    inverter_range = "Dados diários do inversor não encontrados."
    battery_range = "Dados diários da bateria não encontrados."

    if not dados_inversor_diario.empty:
        min_time = dados_inversor_diario['Time (5 min)'].min().strftime('%d.%m.%Y %H:%M')
        max_time = dados_inversor_diario['Time (5 min)'].max().strftime('%d.%m.%Y %H:%M')
        inverter_range = f"Dados diários do inversor cobrem o período de {min_time} a {max_time}."

    if not dados_bateria_diario.empty:
        min_time = dados_bateria_diario['Time (5 min)'].min().strftime('%d.%m.%Y %H:%M')
        max_time = dados_bateria_diario['Time (5 min)'].max().strftime('%d.%m.%Y %H:%M')
        battery_range = f"Dados diários da bateria cobrem o período de {min_time} a {max_time}."

    return f"{inverter_range}\n{battery_range}"

# -----------------------------
# Teste rápido
# -----------------------------
if __name__ == "__main__":
    print("=== Análise do Dia Atual (nos dados mensais) ===")
    print(analiseInversor_csv())
    print(getConsumoMensal())
    print("\n=== Análise dos Dados Diários (horário mais próximo) ===")
    print(getGeracaoDiaria())
    print(getStatusBateria())
    print(getEnergiaRede())
    print("\n=== Análise Diária Detalhada ===")
    print(get_daily_inverter_generation())
    print(get_average_battery_level())
    print(get_daily_data_range())
