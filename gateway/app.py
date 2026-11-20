"""
SERVIÇO 3 — GATEWAY  (porta 8000)
=================================

O gateway é a "porta de entrada" da aplicação. O utilizador só fala com ele,
e é ele que chama os outros dois serviços:

    Browser  --->  GATEWAY (8000)  --->  BIGRAMAS (5001)
                                   --->  LLM      (5002)  --->  Ollama (11434)

Isto é a ideia dos micro-serviços: cada serviço faz UMA coisa, e falam
entre si por HTTP (pedidos GET, respostas em JSON).

Tens de completar 1 TODO (procura por "TODO").
"""

import re
from pathlib import Path

import requests
from flask import Flask, jsonify, request, send_file

app = Flask(__name__)

URL_BIGRAMAS = "http://localhost:5001"
URL_LLM = "http://localhost:5002"

PAGINA = Path(__file__).resolve().parent / "index.html"


def ultima_palavra(texto):
    """'O que é um modelo?' -> 'modelo'  (já está feito)"""
    palavras = re.findall(r"[a-záàâãéêíóôõúç-]+", texto.lower())
    return palavras[-1] if palavras else ""


@app.get("/")
def pagina():
    """Mostra a página web (index.html)."""
    return send_file(PAGINA)


@app.get("/api/estado")
def estado():
    """Verifica se os outros serviços estão vivos (já está feito)."""
    resultado = {}
    for nome, url in [("bigramas", URL_BIGRAMAS), ("llm", URL_LLM)]:
        try:
            requests.get(f"{url}/saude", timeout=2)
            resultado[nome] = True
        except requests.exceptions.RequestException:
            resultado[nome] = False
    return jsonify(resultado)


@app.get("/api/perguntar")
def perguntar():
    """Recebe o texto do utilizador e junta as respostas dos 2 serviços."""
    texto = request.args.get("texto", "").strip()

    # ---- 1) Chamar o serviço de BIGRAMAS  (EXEMPLO — já está feito) -------
    # Pedimos a palavra que vem a seguir à última palavra do texto.
    try:
        r = requests.get(
            f"{URL_BIGRAMAS}/prever",
            params={"palavra": ultima_palavra(texto)},
            timeout=5,
        )
        sugestao = r.json()["seguinte"]
    except requests.exceptions.RequestException:
        sugestao = "(serviço de bigramas em baixo)"

    # ---- 2) Chamar o serviço LLM  ------------------------------------------
    # ----------------------------------------------------------------------
    # TODO 6: faz o mesmo que no exemplo acima, mas para o serviço LLM.
    #
    #   - o endereço é f"{URL_LLM}/perguntar"
    #   - o parâmetro chama-se "pergunta" e o valor é o `texto` todo
    #   - usa timeout=120 (os modelos podem demorar a responder!)
    #   - a resposta JSON tem a chave "resposta" -> guarda-a em resposta_llm
    #   - se der erro (except), põe resposta_llm = "(serviço LLM em baixo)"
    #
    # Dica: copia o bloco try/except de cima e adapta-o.
    # ----------------------------------------------------------------------
    resposta_llm = "(ainda não implementado)"  # <- substitui esta linha

    return jsonify({
        "texto": texto,
        "sugestao_bigramas": sugestao,
        "resposta_llm": resposta_llm,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
