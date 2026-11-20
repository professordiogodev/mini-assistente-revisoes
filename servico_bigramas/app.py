"""
SERVIÇO 1 — BIGRAMAS  (porta 5001)
==================================

O que este serviço faz:
  1. Lê o ficheiro corpus.txt (o nosso "texto de treino").
  2. Conta, para cada palavra, quais são as palavras que aparecem logo a seguir.
  3. Disponibiliza um endpoint HTTP que, dada uma palavra, devolve a palavra
     seguinte mais provável.

É exatamente a ideia da Tarefa 2 (Bigramas), mas agora "embrulhada" num
serviço web com Flask, para que outros programas a possam usar.

Tens de completar 2 TODOs (procura por "TODO").
"""

import re
from collections import Counter, defaultdict
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)

# Caminho para o corpus.txt (está na pasta acima desta)
CORPUS = Path(__file__).resolve().parent.parent / "corpus.txt"


def ler_palavras(caminho):
    """Lê o texto, passa tudo para minúsculas e devolve uma lista de palavras.

    Exemplo: "O modelo lê." -> ["o", "modelo", "lê"]
    (já está feito, não precisas de mexer)
    """
    texto = caminho.read_text(encoding="utf-8").lower()
    return re.findall(r"[a-záàâãéêíóôõúç-]+", texto)


def treinar_bigramas(palavras):
    """Conta quantas vezes cada palavra aparece a seguir a outra.

    O resultado é um "dicionário de contadores". Por exemplo, se o texto for
    "o modelo lê o modelo corre", ficamos com:

        contagens["o"]      -> Counter({"modelo": 2})
        contagens["modelo"] -> Counter({"lê": 1, "corre": 1})
        contagens["lê"]     -> Counter({"o": 1})
    """
    contagens = defaultdict(Counter)

    # Percorremos a lista e olhamos para cada PAR de palavras seguidas
    for i in range(len(palavras) - 1):
        atual = palavras[i]
        seguinte = palavras[i + 1]

        # ------------------------------------------------------------------
        # TODO 1: soma 1 à contagem de "seguinte" dentro de contagens[atual].
        #
        # Dica: um Counter funciona como um dicionário de números.
        #       contagens[atual] é um Counter, e queres aumentar a posição
        #       [seguinte] desse Counter em 1 (usa +=).
        # ------------------------------------------------------------------
        pass  # <- apaga esta linha e escreve aqui o teu código

    return contagens


# Isto corre UMA vez, quando o serviço arranca ("treino" do modelo)
PALAVRAS = ler_palavras(CORPUS)
BIGRAMAS = treinar_bigramas(PALAVRAS)
print(f"[bigramas] Corpus com {len(PALAVRAS)} palavras, "
      f"{len(BIGRAMAS)} palavras diferentes aprendidas.")


def prever(palavra):
    """Devolve a palavra que aparece MAIS vezes a seguir a `palavra`.

    Se a palavra não existir no corpus, devolve None.
    """
    opcoes = BIGRAMAS.get(palavra)
    if not opcoes:
        return None

    # ----------------------------------------------------------------------
    # TODO 2: devolve a palavra mais frequente dentro de `opcoes`.
    #
    # Dica: os Counter têm o método .most_common(n), que devolve uma lista
    #       de pares (palavra, contagem), do mais frequente para o menos.
    #       Exemplo: Counter({"modelo": 5, "texto": 2}).most_common(1)
    #                -> [("modelo", 5)]
    #       Queres só a palavra, ou seja, o primeiro elemento do primeiro par.
    # ----------------------------------------------------------------------
    return None  # <- substitui esta linha


# --------------------------------------------------------------------------
# ROTAS HTTP (já estão feitas)
# --------------------------------------------------------------------------

@app.get("/saude")
def saude():
    """Serve só para os outros serviços saberem que este está vivo."""
    return jsonify({"servico": "bigramas", "ok": True})


@app.get("/prever")
def rota_prever():
    """Exemplo: http://localhost:5001/prever?palavra=modelo"""
    palavra = request.args.get("palavra", "").lower().strip()
    opcoes = BIGRAMAS.get(palavra, Counter())
    return jsonify({
        "palavra": palavra,
        "seguinte": prever(palavra),
        "opcoes": dict(opcoes.most_common(5)),  # top 5, para veres as contagens
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
