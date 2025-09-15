import json
from datetime import datetime
from pathlib import Path

ARQUIVO = Path("bases_de_dados/infos_alexa/historico.json")

def carregar_historico():
    if ARQUIVO.exists():
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def salvar_dados(dados, resposta):
    historico = carregar_historico()

    # Extrair intent
    intent_name = (
        dados.get("request", {})
             .get("intent", {})
             .get("name", "desconhecida")
    )

    # Extrair slots de forma limpa
    slots = (
        dados.get("request", {})
             .get("intent", {})
             .get("slots", {})
    )
    slot_values = {k: v.get("value") for k, v in slots.items() if "value" in v}

    # Extrair locale (idioma configurado na Alexa)
    locale = dados.get("request", {}).get("locale", "pt-BR")

    # Extrair texto da resposta (o que a Alexa fala)
    speech = (
        resposta.get("response", {})
                .get("outputSpeech", {})
                .get("text", "")
    )

    registro = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "intent": intent_name,
        "locale": locale,
        "slots": slot_values,
        "entrada": intent_name if not slot_values else {intent_name: slot_values},
        "resposta": speech
    }

    historico.append(registro)

    ARQUIVO.parent.mkdir(parents=True, exist_ok=True)
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=4)
