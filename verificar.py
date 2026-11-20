"""
VERIFICADOR — corre com:   python verificar.py

Testa cada parte da atividade e diz o que está bem (✅) e o que falta (❌).
Podes correr isto as vezes que quiseres. Não precisas de mexer neste ficheiro.
"""

import requests

OK, MAL = "✅", "❌"


def get(url, **params):
    return requests.get(url, params=params, timeout=150)


def passo(titulo):
    print(f"\n── {titulo} " + "─" * (60 - len(titulo)))


def parte1():
    passo("Parte 1 — Serviço de bigramas (porta 5001)")
    try:
        get("http://localhost:5001/saude")
    except requests.exceptions.RequestException:
        print(f"{MAL} O serviço não está a correr. Arranca-o com:")
        print("     python servico_bigramas/app.py")
        return False
    print(f"{OK} O serviço está a correr")

    d = get("http://localhost:5001/prever", palavra="modelo").json()
    if not d["opcoes"]:
        print(f"{MAL} TODO 1: as contagens estão vazias. Estás a somar 1 em contagens[atual][seguinte]?")
        print("     (depois de mudar o código, tens de parar (Ctrl+C) e voltar a arrancar o serviço)")
        return False
    print(f"{OK} TODO 1: contagens feitas -> {d['opcoes']}")

    if d["seguinte"] is None:
        print(f"{MAL} TODO 2: prever() ainda devolve None. Usa .most_common(1)")
        return False
    print(f"{OK} TODO 2: depois de 'modelo' vem '{d['seguinte']}'")
    return True


def parte2():
    passo("Parte 2 — Ollama + Modelfile + serviço LLM (porta 5002)")
    try:
        modelos = get("http://localhost:11434/api/tags").json()["models"]
    except requests.exceptions.RequestException:
        print(f"{MAL} O Ollama não está a responder. Experimenta: ollama serve")
        return False
    print(f"{OK} O Ollama está a correr")

    nomes = [m["name"].split(":")[0] for m in modelos]
    if "assistente" not in nomes:
        print(f"{MAL} TODOs 3 e 4: o modelo 'assistente' não existe. Cria-o com:")
        print("     ollama create assistente -f servico_llm/Modelfile")
        return False
    print(f"{OK} TODOs 3 e 4: o modelo 'assistente' existe")

    try:
        get("http://localhost:5002/saude")
    except requests.exceptions.RequestException:
        print(f"{MAL} O serviço LLM não está a correr. Arranca-o com:")
        print("     python servico_llm/app.py")
        return False
    print(f"{OK} O serviço LLM está a correr")

    print("   (a perguntar ao modelo, pode demorar um bocadinho...)")
    d = get("http://localhost:5002/perguntar", pergunta="Diz olá numa frase.").json()
    resposta = d.get("resposta", d.get("erro"))
    if not resposta or "não implementado" in resposta:
        print(f"{MAL} TODO 5: o serviço ainda não fala com o Ollama -> {resposta}")
        return False
    print(f"{OK} TODO 5: o modelo respondeu -> {resposta.strip()[:80]}")
    return True


def parte3():
    passo("Parte 3 — Gateway (porta 8000)")
    try:
        get("http://localhost:8000/api/estado")
    except requests.exceptions.RequestException:
        print(f"{MAL} O gateway não está a correr. Arranca-o com:")
        print("     python gateway/app.py")
        return False
    print(f"{OK} O gateway está a correr")

    print("   (a perguntar através do gateway...)")
    d = get("http://localhost:8000/api/perguntar", texto="O que faz o modelo").json()
    print(f"   bigramas -> {d['sugestao_bigramas']}")
    if "não implementado" in d["resposta_llm"] or "em baixo" in d["resposta_llm"]:
        print(f"{MAL} TODO 6: o gateway ainda não chama o serviço LLM -> {d['resposta_llm']}")
        return False
    print(f"{OK} TODO 6: llm -> {d['resposta_llm'].strip()[:80]}")
    return True


if __name__ == "__main__":
    resultados = [parte1(), parte2(), parte3()]
    print()
    if all(resultados):
        print("🎉 Está tudo a funcionar! Segue para a Parte 4 (PM2) no README.")
    else:
        print("Ainda há coisas por fazer. Lê as mensagens ❌ acima.")
