# goodwe.py
import pandas as pd
import os
from datetime import datetime, timedelta

# -----------------------------
# Carregamento dos dados
# -----------------------------
# CSVs (ajuste caminhos se estiver no Colab)
dados_mensais_inversor = pd.read_csv('base_de_dados/equipamentos_e_plantas/dados_mensais_inversor.csv')
dados_mensais_bauner = pd.read_csv('base_de_dados/equipamentos_e_plantas/dados_mensais_bauner.csv')
dados_bateria_diario = pd.read_csv('base_de_dados/equipamentos_e_plantas/dados_bateria_diario.csv')
dados_inversor_diario = pd.read_csv('base_de_dados/equipamentos_e_plantas/dados_inversor_diario.csv')

# -----------------------------
# Tratamento de dados
# -----------------------------
# Mensais Inversor
dados_mensais_inversor.columns = ["Monthly Report", "Plant", "Classification", "Capacity(kW)", "Geração(kWh)", "Renda(EUR)"]
dados_mensais_inversor['Monthly Report'] = pd.to_datetime(dados_mensais_inversor['Monthly Report'], format='%d.%m.%Y', errors='coerce')
dados_mensais_inversor['Geração(kWh)'] = pd.to_numeric(dados_mensais_inversor['Geração(kWh)'], errors='coerce')
dados_mensais_inversor['Renda(EUR)'] = pd.to_numeric(dados_mensais_inversor['Renda(EUR)'], errors='coerce')
dados_mensais_inversor.dropna(subset=['Monthly Report', 'Geração(kWh)', 'Renda(EUR)'], inplace=True)

# Mensais Bauner
dados_mensais_bauner['Data(Dias)'] = pd.to_datetime(dados_mensais_bauner['Data(Dias)'], format='%d.%m.%Y', errors='coerce')
dados_mensais_bauner.dropna(subset=['Data(Dias)'], inplace=True)

# Diários — removendo fuso horário
dados_bateria_diario['Time (5 min)'] = pd.to_datetime(
    dados_bateria_diario['Time (5 min)'], format='%d.%m.%Y %H:%M:%S', errors='coerce'
).dt.tz_localize(None)

dados_inversor_diario['Time (5 min)'] = pd.to_datetime(
    dados_inversor_diario['Time (5 min)'], format='%d.%m.%Y %H:%M:%S', errors='coerce'
).dt.tz_localize(None)

dados_bateria_diario.dropna(subset=['Time (5 min)'], inplace=True)
dados_inversor_diario.dropna(subset=['Time (5 min)'], inplace=True)

# Hoje
today = datetime.now().date()
today_day = today.day
dados_inversor_hoje = dados_mensais_inversor[dados_mensais_inversor['Monthly Report'].dt.day == today_day]
dados_bauner_hoje = dados_mensais_bauner[dados_mensais_bauner['Data(Dias)'].dt.day == today_day]

# -----------------------------
# Funções de automação
# -----------------------------
def ligarCarregador(): return "Carregamento do carro iniciado com sucesso!"
def desligarCarregador(): return "Carregamento parado com segurança."
def ligarLuz(): return "As luzes foram acesas."
def desligarLuz(): return "As luzes foram apagadas."
def ligarArCondicionado(): return "O ar-condicionado foi ligado."
def desligarArCondicionado(): return "O ar-condicionado foi desligado."
def ligarTomada(): return "A tomada inteligente foi ativada."
def desligarTomada(): return "A tomada inteligente foi desligada."

# -----------------------------
# Funções auxiliares
# -----------------------------
def get_previous_time_entry_ignore_date(df, time_column, target_time):
    """Retorna a linha exata ou mais próxima para trás (<= target_time), ignorando a data."""
    if df.empty:
        return None

    df = df.copy()
    df['TimeOnly'] = df[time_column].dt.strftime('%H:%M')
    df['TimeParsed'] = pd.to_datetime(df['TimeOnly'], format='%H:%M')
    target_parsed = pd.to_datetime(target_time.strftime('%H:%M'), format='%H:%M')
    df_filtered = df[df['TimeParsed'] <= target_parsed]
    if df_filtered.empty:
        return None
    return df_filtered.iloc[-1]

# -----------------------------
# Funções de análise de energia
# -----------------------------
def _current_time_brasilia():
    """Retorna o datetime atual ajustado para horário de Brasília (UTC-3)."""
    return datetime.now() - timedelta(hours=3)

def analiseInversor_csv():
    if not dados_inversor_hoje.empty:
        total_daily_generation = dados_inversor_hoje['Geração(kWh)'].sum()
        total_daily_income = dados_inversor_hoje['Renda(EUR)'].sum()
        return f"Geração do dia {today_day} (Inversor): {total_daily_generation:.2f} kWh\nRenda do dia {today_day} (Inversor): {total_daily_income:.2f} EUR"
    return f"Dados do inversor para o dia {today_day} não encontrados nos dados mensais."

def getConsumoMensal():
    if not dados_bauner_hoje.empty:
        if "Consumo(kWh)" in dados_bauner_hoje.columns:
            consumo = dados_bauner_hoje["Consumo(kWh)"].sum()
            return f"O consumo total da casa no dia {today_day} foi de {consumo:.2f} kWh."
        return "Coluna 'Consumo(kWh)' não encontrada nos dados da Bauner."
    return f"Dados da Bauner para o dia {today_day} não encontrados nos dados mensais."

def getGeracaoDiaria():
    current_time = _current_time_brasilia()
    nearest_entry = get_previous_time_entry_ignore_date(dados_inversor_diario, 'Time (5 min)', current_time)
    if nearest_entry is not None and "PV(W)" in nearest_entry:
        return f"A geração solar às {nearest_entry['TimeOnly']} foi de {nearest_entry['PV(W)']:.2f} watts."
    return f"Não há dados disponíveis até {current_time.strftime('%H:%M')}."

def getStatusBateria():
    current_time = _current_time_brasilia()
    nearest_entry = get_previous_time_entry_ignore_date(dados_bateria_diario, 'Time (5 min)', current_time)
    if nearest_entry is not None and "Estado de Carga(%)" in nearest_entry:
        return f"O nível da bateria às {nearest_entry['TimeOnly']} é de {nearest_entry['Estado de Carga(%)']:.2f}%."
    return f"Não há dados disponíveis até {current_time.strftime('%H:%M')}."

def getEnergiaRede():
    current_time = _current_time_brasilia()
    nearest_entry = get_previous_time_entry_ignore_date(dados_bateria_diario, 'Time (5 min)', current_time)
    if nearest_entry is not None and "Grade(Rede Elétrica)(W)" in nearest_entry:
        return f"A energia consumida da rede às {nearest_entry['TimeOnly']} foi de {nearest_entry['Grade(Rede Elétrica)(W)']:.2f} watts."
    return f"Não há dados disponíveis até {current_time.strftime('%H:%M')}."

def get_daily_inverter_generation():
    if not dados_inversor_diario.empty and "PV(W)" in dados_inversor_diario.columns:
        total_generation_wh = dados_inversor_diario["PV(W)"].sum() * (5/60)
        total_generation_kwh = total_generation_wh / 1000
        return f"Geração solar total do dia (dados diários): {total_generation_kwh:.2f} kWh."
    return "Dados diários do inversor não encontrados ou coluna 'PV(W)' ausente."

def get_average_battery_level():
    if not dados_bateria_diario.empty and "Estado de Carga(%)" in dados_bateria_diario.columns:
        average_charge = dados_bateria_diario["Estado de Carga(%)"].mean()
        return f"Nível médio da bateria no dia (dados diários): {average_charge:.2f}%."
    return "Dados diários da bateria não encontrados ou coluna 'Estado de Carga(%)' ausente."

def get_daily_data_range():
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