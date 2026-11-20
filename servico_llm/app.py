"""
SERVIÇO 2 — LLM  (porta 5002)
=============================

O que este serviço faz:
  1. Recebe uma pergunta por HTTP.
  2. Envia essa pergunta ao Ollama (que está a correr em localhost:11434).
  3. Devolve a resposta do modelo "assistente" (criado com o nosso Modelfile).

Ou seja: este serviço é um "intermediário" entre a nossa aplicação e o Ollama.
Quando falas com o modelo no terminal (`ollama run`), por trás o Ollama está a
usar esta mesma API HTTP.

Tens de completar 1 TODO (procura por "TODO").
"""

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Endereço da API do Ollama (é sempre este, se o Ollama estiver ligado)
OLLAMA_URL = "http://localhost:11434/api/generate"

# Nome do modelo que criaste com `ollama create assistente -f ...`
MODELO = "assistente"


def perguntar_ao_modelo(pergunta):
    """Envia `pergunta` ao Ollama e devolve o texto da resposta."""

    # O "pedido" é um dicionário Python que vai ser enviado como JSON.
    #   model  -> qual o modelo a usar
    #   prompt -> o texto que o modelo vai receber
    #   stream -> False = esperamos pela resposta inteira de uma só vez
    pedido = {
        "model": MODELO,
        "prompt": pergunta,
        "stream": False,
    }

    # ----------------------------------------------------------------------
    # TODO 5: envia o pedido ao Ollama e devolve o texto da resposta.
    #
    # Passo a) Faz um POST para OLLAMA_URL com o pedido em JSON:
    #              resposta = requests.post(OLLAMA_URL, json=pedido, timeout=120)
    #
    # Passo b) O Ollama devolve um JSON parecido com isto:
    #              {"model": "assistente", "response": "Olá! ...", "done": true}
    #          Converte para dicionário com resposta.json() e devolve
    #          só o valor da chave "response".
    # ----------------------------------------------------------------------
    return "(ainda não implementado)"  # <- substitui esta linha


# --------------------------------------------------------------------------
# ROTAS HTTP (já estão feitas)
# --------------------------------------------------------------------------

@app.get("/saude")
def saude():
    return jsonify({"servico": "llm", "ok": True})


@app.get("/perguntar")
def rota_perguntar():
    """Exemplo: http://localhost:5002/perguntar?pergunta=O que é um bigrama?"""
    pergunta = request.args.get("pergunta", "").strip()
    if not pergunta:
        return jsonify({"erro": "Falta o parâmetro ?pergunta=..."}), 400

    try:
        texto = perguntar_ao_modelo(pergunta)
    except requests.exceptions.ConnectionError:
        return jsonify({"erro": "Não consegui ligar ao Ollama. Ele está a correr?"}), 503

    return jsonify({"pergunta": pergunta, "resposta": texto})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
