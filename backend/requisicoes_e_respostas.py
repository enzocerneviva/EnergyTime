import json
from datetime import datetime
from pathlib import Path

ARQUIVO = Path("bases_de_dados/infos_alexa/historico.json")

def salvar_dados(dados, resposta):
    historico = carregar_historico()

    registro = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "intent": dados.get("intent", "desconhecida"),
        "entrada": dados,
        "resposta": resposta
    }

    historico.append(registro)

    ARQUIVO.parent.mkdir(parents=True, exist_ok=True)
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=4)

def carregar_historico():
    if ARQUIVO.exists():
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []
